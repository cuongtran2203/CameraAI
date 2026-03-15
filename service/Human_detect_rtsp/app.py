#!/usr/bin/env python3
import sys
import argparse
import warnings
import gi
import pyds
import json
import os
import time
from datetime import datetime, timezone

gi.require_version("Gst", "1.0")
gi.require_version("GstRtspServer", "1.0")

from gi.repository import Gst, GLib, GstRtspServer

warnings.filterwarnings("ignore", message=".*g_object_get_is_valid_property.*")

try:
    from kafka import KafkaProducer
except ImportError:
    KafkaProducer = None


ROI_FILE = "/workspace/roi.json"
last_roi_mtime = 0
current_roi = None

PERSON_CLASS_ID = 0
MUXER_OUTPUT_WIDTH = 640
MUXER_OUTPUT_HEIGHT = 640
MUXER_BATCH_TIMEOUT_USEC = 40000
RTSP_PORT = 8554
UDP_PORT = 5400
RTSP_PATH = "/ds-test"

MIN_PERSON_HEIGHT = 60
MIN_PERSON_WIDTH = 20
MIN_ASPECT_RATIO = 0.3
MAX_ASPECT_RATIO = 1.5

# Tracker paths thật từ DeepStream 8.0 image của bạn
TRACKER_LIB_FILE = "/opt/nvidia/deepstream/deepstream-8.0/lib/libnvds_nvmultiobjecttracker.so"
TRACKER_CONFIG_FILE = "/opt/nvidia/deepstream/deepstream-8.0/samples/configs/deepstream-app/config_tracker_NvDCF_perf.yml"

kafka_producer = None
kafka_topic = None
last_kafka_sent_ts = 0.0
kafka_interval_sec = 1.0


def get_roi():
    global last_roi_mtime, current_roi
    try:
        mtime = os.path.getmtime(ROI_FILE)
        if mtime != last_roi_mtime:
            with open(ROI_FILE, "r") as f:
                data = json.load(f)
                current_roi = data.get("roi")
            last_roi_mtime = mtime
    except Exception:
        pass
    return current_roi


def init_kafka(bootstrap_servers: str, topic: str):
    global kafka_producer, kafka_topic

    kafka_topic = topic

    if KafkaProducer is None:
        print(
            "WARNING: kafka-python chưa được cài. Chạy: pip install kafka-python",
            file=sys.stderr,
        )
        kafka_producer = None
        return

    try:
        kafka_producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
            linger_ms=10,
            retries=3,
        )
        print(f"Kafka producer ready: bootstrap_servers={bootstrap_servers}, topic={topic}")
    except Exception as e:
        print(f"WARNING: Không khởi tạo được Kafka producer: {e}", file=sys.stderr)
        kafka_producer = None


def publish_tracking_count(number_of_human: int):
    global last_kafka_sent_ts

    now = time.time()
    if now - last_kafka_sent_ts < kafka_interval_sec:
        return

    last_kafka_sent_ts = now

    payload = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "number_of_human": int(number_of_human),
        "type": "tracking",
    }

    if kafka_producer is None or kafka_topic is None:
        print(f"[Kafka disabled] {payload}")
        return

    try:
        kafka_producer.send(kafka_topic, payload)
        kafka_producer.flush(timeout=1.0)
        print(f"[Kafka sent] {payload}")
    except Exception as e:
        print(f"WARNING: Gửi Kafka thất bại: {e}", file=sys.stderr)


def streammux_src_pad_buffer_probe(pad, info, user_data):
    gst_buffer = info.get_buffer()
    if not gst_buffer:
        return Gst.PadProbeReturn.OK

    batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    if not batch_meta:
        return Gst.PadProbeReturn.OK

    roi = get_roi()
    if not roi:
        return Gst.PadProbeReturn.OK

    l_frame = batch_meta.frame_meta_list
    while l_frame:
        try:
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        obj_meta = pyds.nvds_acquire_obj_meta_from_pool(batch_meta)
        obj_meta.class_id = 99
        obj_meta.unique_component_id = 1
        obj_meta.confidence = 1.0
        obj_meta.rect_params.left = float(roi["left"])
        obj_meta.rect_params.top = float(roi["top"])
        obj_meta.rect_params.width = float(roi["width"])
        obj_meta.rect_params.height = float(roi["height"])
        obj_meta.rect_params.border_width = 0
        obj_meta.text_params.font_params.font_size = 0

        pyds.nvds_add_obj_meta_to_frame(frame_meta, obj_meta, None)

        try:
            l_frame = l_frame.next
        except StopIteration:
            break

    return Gst.PadProbeReturn.OK


def is_valid_person(obj_meta) -> bool:
    if obj_meta.class_id != PERSON_CLASS_ID:
        return False

    rect = obj_meta.rect_params
    w = rect.width
    h = rect.height

    if h < MIN_PERSON_HEIGHT or w < MIN_PERSON_WIDTH:
        return False

    if h <= 0:
        return False

    ratio = w / h
    if ratio < MIN_ASPECT_RATIO or ratio > MAX_ASPECT_RATIO:
        return False

    return True


def add_count_text(batch_meta, frame_meta, person_count: int):
    display_meta = pyds.nvds_acquire_display_meta_from_pool(batch_meta)
    display_meta.num_labels = 1

    text_params = display_meta.text_params[0]
    text_params.display_text = f"Persons: {person_count}"
    text_params.x_offset = 20
    text_params.y_offset = 40
    text_params.font_params.font_name = "Serif"
    text_params.font_params.font_size = 18
    text_params.font_params.font_color.set(1.0, 1.0, 1.0, 1.0)
    text_params.set_bg_clr = 1
    text_params.text_bg_clr.set(0.0, 0.0, 0.0, 0.7)

    pyds.nvds_add_display_meta_to_frame(frame_meta, display_meta)


def osd_sink_pad_buffer_probe(pad, info, user_data):
    gst_buffer = info.get_buffer()
    if not gst_buffer:
        return Gst.PadProbeReturn.OK

    batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    if not batch_meta:
        return Gst.PadProbeReturn.OK

    roi = get_roi()

    l_frame = batch_meta.frame_meta_list
    while l_frame:
        try:
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        if roi:
            display_meta = pyds.nvds_acquire_display_meta_from_pool(batch_meta)
            display_meta.num_rects = 1
            rect_params = display_meta.rect_params[0]
            rect_params.left = roi["left"]
            rect_params.top = roi["top"]
            rect_params.width = roi["width"]
            rect_params.height = roi["height"]
            rect_params.border_width = 3
            rect_params.border_color.red = 0.0
            rect_params.border_color.green = 1.0
            rect_params.border_color.blue = 0.0
            rect_params.border_color.alpha = 1.0
            pyds.nvds_add_display_meta_to_frame(frame_meta, display_meta)

        to_remove = []
        person_count = 0

        l_obj = frame_meta.obj_meta_list
        while l_obj:
            try:
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break

            keep = True

            if obj_meta.class_id == 99:
                keep = False
            elif not is_valid_person(obj_meta):
                keep = False
            else:
                person_count += 1
                try:
                    track_id = int(obj_meta.object_id)
                    obj_meta.text_params.display_text = f"person:{track_id}"
                except Exception:
                    obj_meta.text_params.display_text = "person"

            if not keep:
                to_remove.append(obj_meta)

            try:
                l_obj = l_obj.next
            except StopIteration:
                break

        for obj_meta in to_remove:
            pyds.nvds_remove_obj_meta_from_frame(frame_meta, obj_meta)

        add_count_text(batch_meta, frame_meta, person_count)
        publish_tracking_count(person_count)

        try:
            l_frame = l_frame.next
        except StopIteration:
            break

    return Gst.PadProbeReturn.OK


def cb_newpad(decodebin, decoder_src_pad, data):
    caps = decoder_src_pad.get_current_caps()
    if not caps:
        caps = decoder_src_pad.query_caps(None)
    if not caps:
        return

    gststruct = caps.get_structure(0)
    name = gststruct.get_name()
    if not name.startswith("video"):
        return

    source_bin = data
    ghost_pad = source_bin.get_static_pad("src")
    if ghost_pad.set_target(decoder_src_pad):
        print("Linked decoder pad to source bin")
    else:
        print("Failed to link decoder pad to source bin", file=sys.stderr)


def decodebin_child_added(child_proxy, obj, name, user_data):
    if name.find("decodebin") != -1:
        obj.connect("child-added", decodebin_child_added, user_data)


def create_source_bin(index: int, uri: str):
    bin_name = f"source-bin-{index:02d}"
    nbin = Gst.Bin.new(bin_name)
    if not nbin:
        raise RuntimeError("Unable to create source bin")

    uri_decode_bin = Gst.ElementFactory.make("uridecodebin", f"uri-decode-bin-{index}")
    if not uri_decode_bin:
        raise RuntimeError("Unable to create uridecodebin")

    uri_decode_bin.set_property("uri", uri)
    uri_decode_bin.connect("pad-added", cb_newpad, nbin)
    uri_decode_bin.connect("child-added", decodebin_child_added, nbin)

    nbin.add(uri_decode_bin)

    ghost_pad = Gst.GhostPad.new_no_target("src", Gst.PadDirection.SRC)
    if not ghost_pad:
        raise RuntimeError("Failed to add ghost pad in source bin")
    nbin.add_pad(ghost_pad)

    return nbin


def create_rtsp_server():
    server = GstRtspServer.RTSPServer.new()
    server.set_service(str(RTSP_PORT))

    factory = GstRtspServer.RTSPMediaFactory.new()
    factory.set_shared(True)
    factory.set_suspend_mode(GstRtspServer.RTSPSuspendMode.NONE)

    launch_desc = (
        f'( udpsrc name=pay0 port={UDP_PORT} buffer-size=524288 '
        'caps="application/x-rtp,media=video,clock-rate=90000,'
        'encoding-name=H264,payload=96" )'
    )
    factory.set_launch(launch_desc)

    mounts = server.get_mount_points()
    mounts.add_factory(RTSP_PATH, factory)
    server.attach(None)

    print(f"RTSP ready at rtsp://127.0.0.1:{RTSP_PORT}{RTSP_PATH}")
    return server


def on_bus_message(bus, message, loop, pipeline):
    msg_type = message.type

    if msg_type == Gst.MessageType.EOS:
        print("EOS reached, looping file input...")
        success = pipeline.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0,
        )
        if not success:
            print("Seek failed on EOS, stopping.", file=sys.stderr)
            loop.quit()

    elif msg_type == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"ERROR: {err}", file=sys.stderr)
        if debug:
            print(f"DEBUG: {debug}", file=sys.stderr)
        loop.quit()

    elif msg_type == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        print(f"WARNING: {err}", file=sys.stderr)
        if debug:
            print(f"DEBUG: {debug}", file=sys.stderr)

    return True


def setup_tracker(tracker):
    if not os.path.exists(TRACKER_LIB_FILE):
        raise RuntimeError(f"Tracker lib not found: {TRACKER_LIB_FILE}")

    if not os.path.exists(TRACKER_CONFIG_FILE):
        raise RuntimeError(f"Tracker config not found: {TRACKER_CONFIG_FILE}")

    tracker.set_property("tracker-width", 640)
    tracker.set_property("tracker-height", 384)
    tracker.set_property("gpu-id", 0)
    tracker.set_property("ll-lib-file", TRACKER_LIB_FILE)
    tracker.set_property("ll-config-file", TRACKER_CONFIG_FILE)


def build_pipeline(input_uri: str, infer_config_path: str):
    pipeline = Gst.Pipeline.new("person-filter-rtsp-pipeline")
    if not pipeline:
        raise RuntimeError("Unable to create pipeline")

    streammux = Gst.ElementFactory.make("nvstreammux", "streammux")
    pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
    tracker = Gst.ElementFactory.make("nvtracker", "tracker")
    nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "convertor")
    nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay")
    encoder = Gst.ElementFactory.make("nvv4l2h264enc", "h264-encoder")
    rtppay = Gst.ElementFactory.make("rtph264pay", "rtp-payloader")
    udpsink = Gst.ElementFactory.make("udpsink", "udp-sink")
    nvvidconv2 = Gst.ElementFactory.make("nvvideoconvert", "convertor2")
    capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")

    elems = {
        "streammux": streammux,
        "pgie": pgie,
        "tracker": tracker,
        "nvvidconv": nvvidconv,
        "nvosd": nvosd,
        "nvvidconv2": nvvidconv2,
        "capsfilter": capsfilter,
        "encoder": encoder,
        "rtppay": rtppay,
        "udpsink": udpsink,
    }
    for name, elem in elems.items():
        if not elem:
            raise RuntimeError(f"Unable to create element: {name}")

    streammux.set_property("width", MUXER_OUTPUT_WIDTH)
    streammux.set_property("height", MUXER_OUTPUT_HEIGHT)
    streammux.set_property("batch-size", 1)
    streammux.set_property("batched-push-timeout", MUXER_BATCH_TIMEOUT_USEC)
    streammux.set_property("live-source", 0)

    pgie.set_property("config-file-path", infer_config_path)
    setup_tracker(tracker)

    encoder.set_property("bitrate", 4000000)
    encoder.set_property("iframeinterval", 30)

    rtppay.set_property("pt", 96)
    rtppay.set_property("config-interval", -1)

    udpsink.set_property("host", "127.0.0.1")
    udpsink.set_property("port", UDP_PORT)
    udpsink.set_property("async", False)
    udpsink.set_property("sync", 1)

    caps = Gst.Caps.from_string("video/x-raw(memory:NVMM), format=I420")
    capsfilter.set_property("caps", caps)

    source_bin = create_source_bin(0, input_uri)

    pipeline.add(source_bin)
    pipeline.add(streammux)
    pipeline.add(pgie)
    pipeline.add(tracker)
    pipeline.add(nvvidconv)
    pipeline.add(nvosd)
    pipeline.add(nvvidconv2)
    pipeline.add(capsfilter)
    pipeline.add(encoder)
    pipeline.add(rtppay)
    pipeline.add(udpsink)

    sinkpad = streammux.request_pad_simple("sink_0")
    if not sinkpad:
        raise RuntimeError("Unable to get streammux sink pad")

    srcpad = source_bin.get_static_pad("src")
    if not srcpad:
        raise RuntimeError("Unable to get source bin src pad")

    if srcpad.link(sinkpad) != Gst.PadLinkReturn.OK:
        raise RuntimeError("Failed to link source bin to streammux")

    if not streammux.link(pgie):
        raise RuntimeError("Failed to link streammux -> pgie")
    if not pgie.link(tracker):
        raise RuntimeError("Failed to link pgie -> tracker")
    if not tracker.link(nvvidconv):
        raise RuntimeError("Failed to link tracker -> nvvideoconvert")
    if not nvvidconv.link(nvosd):
        raise RuntimeError("Failed to link nvvideoconvert -> nvdsosd")
    if not nvosd.link(nvvidconv2):
        raise RuntimeError("Failed to link nvosd -> nvvidconv2")
    if not nvvidconv2.link(capsfilter):
        raise RuntimeError("Failed to link nvvidconv2 -> capsfilter")
    if not capsfilter.link(encoder):
        raise RuntimeError("Failed to link capsfilter -> encoder")
    if not encoder.link(rtppay):
        raise RuntimeError("Failed to link encoder -> rtppay")
    if not rtppay.link(udpsink):
        raise RuntimeError("Failed to link rtppay -> udpsink")

    streammux_src_pad = streammux.get_static_pad("src")
    if not streammux_src_pad:
        raise RuntimeError("Unable to get streammux src pad")

    osd_sink_pad = nvosd.get_static_pad("sink")
    if not osd_sink_pad:
        raise RuntimeError("Unable to get nvdsosd sink pad")

    streammux_src_pad.add_probe(
        Gst.PadProbeType.BUFFER,
        streammux_src_pad_buffer_probe,
        None,
    )

    osd_sink_pad.add_probe(
        Gst.PadProbeType.BUFFER,
        osd_sink_pad_buffer_probe,
        None,
    )

    return pipeline


def main():
    global kafka_interval_sec

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="file:///workspace/videos/test.mp4",
        help="Input URI, vd: file:///workspace/videos/test.mp4 hoặc rtsp://...",
    )
    parser.add_argument(
        "--infer-config",
        default="/workspace/config/config_infer_primary_yolo.txt",
        help="Path tới config nvinfer",
    )
    parser.add_argument(
        "--kafka-bootstrap",
        default="127.0.0.1:9092",
        help="Kafka bootstrap servers",
    )
    parser.add_argument(
        "--kafka-topic",
        default="human_tracking",
        help="Kafka topic",
    )
    parser.add_argument(
        "--kafka-interval-ms",
        type=int,
        default=1000,
        help="Chu kỳ gửi Kafka (ms)",
    )
    args = parser.parse_args()

    kafka_interval_sec = max(args.kafka_interval_ms / 1000.0, 0.1)

    Gst.init(None)

    init_kafka(args.kafka_bootstrap, args.kafka_topic)

    loop = GLib.MainLoop()

    create_rtsp_server()
    pipeline = build_pipeline(args.input, args.infer_config)

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_bus_message, loop, pipeline)

    print("Starting pipeline...")
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        raise RuntimeError("Unable to set pipeline to PLAYING")

    try:
        loop.run()
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping pipeline...")
        pipeline.set_state(Gst.State.NULL)
        if kafka_producer is not None:
            try:
                kafka_producer.flush(timeout=1.0)
                kafka_producer.close()
            except Exception:
                pass


if __name__ == "__main__":
    sys.exit(main())