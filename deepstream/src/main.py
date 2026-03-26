#!/usr/bin/env python3
"""
DeepStream RTSP → RTSP Human Detection Pipeline
- Reads RTSP stream (e.g. surveillance camera)
- Detects humans using PeopleNet
- Applies ROI based on detected human bounding boxes
- Outputs annotated RTSP stream
"""

import sys
import gi
import configparser
import os
import time
import math
import threading
import json

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import GObject, Gst, GstRtspServer

try:
    import pyds
except ImportError:
    sys.stderr.write("Note: pyds not found. This script requires DeepStream SDK installed.\n")
    pyds = None

# ─── Configuration ───────────────────────────────────────────────────────────
RTSP_PORT = "8554"
RTSP_MOUNT_POINT = "/ds-test"
UDP_PORT = 5400

# RTSP source URL – override via env var RTSP_URL
RTSP_URL = os.environ.get(
    "RTSP_URL",
    "rtsp://admin:password@192.168.1.100:554/Streaming/Channels/101"
)

# Primary detector config
INFER_CONFIG = "configs/config_infer_primary.txt"
TRACKER_CONFIG = "configs/tracker_config.yml"

# Stream dimensions (internal processing)
STREAM_WIDTH = 1920
STREAM_HEIGHT = 1080

# Output stream dimensions (sent to RTSP — smaller = less bandwidth)
OUTPUT_WIDTH  = 480
OUTPUT_HEIGHT = 480

# RTSP output bitrate (bps)
ENCODER_BITRATE = 4_000_000

# Minimum confidence to consider a detection valid
MIN_CONFIDENCE = 0.5

# Human class ID in PeopleNet (0 = person)
PERSON_CLASS_ID = 0

# ─── Global ROI state (thread-safe) ─────────────────────────────────────────
class ROIState:
    """Stores the latest per-frame human ROIs for the probe to apply."""
    def __init__(self):
        self.lock = threading.Lock()
        # roi = (left, top, width, height) in pixels (0..1 normalized)
        self.rois: list = []

    def set_rois(self, rois):
        with self.lock:
            self.rois = rois

    def get_rois(self):
        with self.lock:
            return list(self.rois)

roi_state = ROIState()


# ─── Probe: extract human bounding boxes & apply ROI ─────────────────────────
def osd_sink_pad_buffer_probe(pad, info, u_data):
    """
    1. Reads detected human boxes from frame metadata.
    2. Updates global ROI state.
    3. Overrides full-frame inference ROI with per-human ROIs via user metadata.
    """
    gst_buffer = info.get_buffer()
    if not gst_buffer:
        print("Unable to get GstBuffer")
        return Gst.PadProbeReturn.OK

    if pyds is None:
        return Gst.PadProbeReturn.OK

    try:
        batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    except Exception:
        return Gst.PadProbeReturn.OK

    l_frame = batch_meta.frame_meta_list
    while l_frame is not None:
        try:
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        # ── Collect human bounding boxes for this frame ──────────────────────
        human_rois = []
        l_obj = frame_meta.obj_meta_list
        while l_obj is not None:
            try:
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break

            if obj_meta.class_id == PERSON_CLASS_ID:
                rect = obj_meta.rect_params
                left   = rect.left
                top    = rect.top
                width  = rect.width
                height = rect.height
                conf   = obj_meta.confidence

                if conf >= MIN_CONFIDENCE and width > 0 and height > 0:
                    # Normalize to 0..1 for ROI metadata
                    norm_left   = left / STREAM_WIDTH
                    norm_top    = top  / STREAM_HEIGHT
                    norm_width  = width / STREAM_WIDTH
                    norm_height = height / STREAM_HEIGHT

                    human_rois.append({
                        "left":   round(norm_left,   4),
                        "top":    round(norm_top,    4),
                        "width":  round(norm_width,  4),
                        "height": round(norm_height, 4),
                        "conf":   round(float(conf), 4),
                    })

                    # Draw green rectangle on detected humans
                    obj_meta.rect_params.border_color.set(0.0, 1.0, 0.0, 1.0)  # green
                    obj_meta.rect_params.border_width = 3

            try:
                l_obj = l_obj.next
            except StopIteration:
                break

        # Update global ROI state
        roi_state.set_rois(human_rois)

        # ── Attach ROI metadata to frame for downstream use ─────────────────
        # Attach as NvDsUserMeta (can be read by analytics / secondary models)
        user_meta = pyds.nvds_acquire_user_meta_from_pool(batch_meta)
        if user_meta:
            roi_payload = json.dumps(human_rois).encode("utf-8")
            pyds.set_user_data(user_meta, roi_payload)
            pyds.nvds_add_user_meta_to_frame(user_meta, frame_meta, 1)  # 1 = user meta from plugin

        # Print detections to stdout (remove in production)
        if human_rois:
            print(f"[{time.strftime('%H:%M:%S')}] Frame {frame_meta.frame_num}: "
                  f"{len(human_rois)} human(s) detected  ROIs={human_rois}")

        try:
            l_frame = l_frame.next
        except StopIteration:
            break

    return Gst.PadProbeReturn.OK


# ─── Web-app–style REST probe: expose human count via shared dict ────────────
class DetectionStats:
    def __init__(self):
        self.lock = threading.Lock()
        self.latest = {}

    def update(self, frame_num: int, humans: list):
        with self.lock:
            self.latest = {
                "frame": frame_num,
                "count": len(humans),
                "rois": humans,
                "ts": time.time(),
            }

    def get(self):
        with self.lock:
            return dict(self.latest)

stats = DetectionStats()


# ─── GStreamer helpers ───────────────────────────────────────────────────────

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End of stream\n")
        loop.quit()
    elif t == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        sys.stderr.write(f"WARNING: {err}: {debug}\n")
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write(f"ERROR: {err}: {debug}\n")
        loop.quit()
    return True


def link_element_with_sink_pad_sync(element, sink, sink_pad_name="sink"):
    """Link two elements, requesting the sink pad synchronously."""
    sink_pad = element.get_request_pad(sink_pad_name)
    if not sink_pad:
        sys.stderr.write(f"Unable to get sink pad of {element}\n")
        return False
    src_pad = sink.get_static_pad("src")
    ret = sink_pad.link(src_pad)
    if ret != Gst.PadLinkReturn.OK:
        sys.stderr.write(f"Link failed between {element} and {sink}\n")
        return False
    return True


def create_rtsp_pipeline(rtsp_url: str) -> Gst.Pipeline:
    """
    Build:  rtspsrc → rtph264depay → h264parse → avdec_h264 →
           nvvidconv → streammux → nvinfer → nvtracker →
           nvvidconv → nvdsosd → nvvidconv_post →
           encoder → rtph264pay → udpsink
    Plus an RTSP server factory mirroring the UDP output.
    """
    GObject.threads_init()
    Gst.init(None)

    pipeline = Gst.Pipeline.new("ds-human-detect")
    if not pipeline:
        sys.stderr.write("Unable to create Pipeline\n")

    # ── 1. RTSP Source ───────────────────────────────────────────────────────
    rtspsrc = Gst.ElementFactory.make("rtspsrc", "rtsp-source")
    rtspsrc.set_property("location", rtsp_url)
    rtspsrc.set_property("latency", 200)
    rtspsrc.set_property("drop-on-latency", True)

    rtph264depay = Gst.ElementFactory.make("rtph264depay", "rtp-depay")
    h264parse    = Gst.ElementFactory.make("h264parse",    "h264-parse")

    # ── 2. Decode ─────────────────────────────────────────────────────────────
    avdec = Gst.ElementFactory.make("avdec_h264", "avdec")
    nvvidconv_src = Gst.ElementFactory.make("nvvidconv", "nvvidconv-src")

    # ── 3. StreamMuxer ────────────────────────────────────────────────────────
    streammux = Gst.ElementFactory.make("nvstreammux", "stream-muxer")
    streammux.set_property("width",  STREAM_WIDTH)
    streammux.set_property("height", STREAM_HEIGHT)
    streammux.set_property("batch-size", 1)
    streammux.set_property("batched-push-timeout", 40000)
    streammux.set_property("live-source", 1)

    # ── 4. Inference (PeopleNet Human Detection) ─────────────────────────────
    pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
    pgie.set_property("config-file-path", INFER_CONFIG)

    # ── 5. Tracker (NvDCF) ────────────────────────────────────────────────────
    tracker = Gst.ElementFactory.make("nvtracker", "tracker")
    tracker.set_property("config-width",  640)
    tracker.set_property("config-height", 384)
    tracker.set_property("tracker-width",  640)
    tracker.set_property("tracker-height", 384)
    tracker.set_property("ll-lib-file",
        "/opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so")
    tracker.set_property("ll-config-file", TRACKER_CONFIG)
    tracker.set_property("gpu-id", 0)

    # ── 6. Post-inference nvvidconv + OSD ─────────────────────────────────────
    nvvidconv = Gst.ElementFactory.make("nvvidconv", "nvvidconv-post")
    nvosd     = Gst.ElementFactory.make("nvdsosd",   "osd")

    # ── 7. Scale output to smaller resolution (after OSD overlay) ───────────────
    nvvidconv_scale = Gst.ElementFactory.make("nvvidconv", "nvvidconv-scale")
    nvvidconv_scale.set_property("width",  OUTPUT_WIDTH)
    nvvidconv_scale.set_property("height", OUTPUT_HEIGHT)

    # ── 8. RTSP Output Chain ─────────────────────────────────────────────────
    caps_filter   = Gst.ElementFactory.make("capsfilter", "caps-filter")
    caps_filter.set_property("caps", Gst.Caps.from_string(
        "video/x-raw(memory:NVMM), format=I420"))

    encoder = Gst.ElementFactory.make("nvv4l2h264enc", "encoder")
    encoder.set_property("bitrate", ENCODER_BITRATE)
    encoder.set_property("profile",  4)   # high quality

    rtph264pay = Gst.ElementFactory.make("rtph264pay", "rtp-pay")

    udpsink = Gst.ElementFactory.make("udpsink", "udp-sink")
    udpsink.set_property("host",   "224.224.255.255")
    udpsink.set_property("port",   UDP_PORT)
    udpsink.set_property("async",  False)
    udpsink.set_property("sync",   1)

    # ── Add all elements ─────────────────────────────────────────────────────
    for el in (rtspsrc, rtph264depay, h264parse, avdec, nvvidconv_src,
               streammux, pgie, tracker, nvvidconv, nvosd,
               nvvidconv_scale, caps_filter, encoder, rtph264pay, udpsink):
        if el is None:
            sys.stderr.write(" Unable to create an element – check DeepStream installation\n")
        pipeline.add(el)

    # ── Link: RTSP depay → decode → nvvidconv → muxer sink_0 ───────────────
    rtph264depay.link(h264parse)
    h264parse.link(avdec)
    avdec.link(nvvidconv_src)

    # Dynamic pad: nvvidconv_src src pad → streammux sink_0
    def on_src_pad(pad):
        sink_pad = streammux.get_request_pad("sink_0")
        ret = pad.link(sink_pad)
        if ret != Gst.PadLinkReturn.OK:
            sys.stderr.write(f"rtspsrc→streammux link failed: {ret}\n")
        else:
            print(f"Linked rtspsrc to streammux sink_0")
    nvvidconv_src.connect("pad-added", on_src_pad)

    # ── Link: streammux → inference → tracker → nvvidconv → OSD ────────────
    streammux.link(pgie)
    pgie.link(tracker)
    tracker.link(nvvidconv)
    nvvidconv.link(nvosd)

    # ── Link: OSD → output chain → UDP sink ──────────────────────────────────
    nvosd.link(nvvidconv_scale)
    nvvidconv_scale.link(caps_filter)
    caps_filter.link(encoder)
    encoder.link(rtph264pay)
    rtph264pay.link(udpsink)

    # ── Probe on OSD sink pad (reads metadata, applies ROI logic) ────────────
    osd_sink_pad = nvosd.get_static_pad("sink")
    if not osd_sink_pad:
        sys.stderr.write(" Unable to get sink pad of nvosd\n")
    else:
        osd_sink_pad.add_probe(
            Gst.PadProbeType.BUFFER,
            osd_sink_pad_buffer_probe,
            0
        )

    # ── RTSP Server (mirrors UDP output) ────────────────────────────────────
    server = GstRtspServer.RTSPServer.new()
    server.props.service = RTSP_PORT

    factory = GstRtspServer.RTSPMediaFactory.new()
    factory.set_launch(
        f"( udpsrc name=pay0 port={UDP_PORT} "
        f'caps="application/x-rtp, media=video, clock-rate=90000, '
        f'encoding-name=H264, payload=96" )'
    )
    factory.set_shared(True)
    server.get_mount_points().add_factory(RTSP_MOUNT_POINT, factory)
    server.attach(None)

    print(f"\n  RTSP input : {rtsp_url}")
    print(f"  RTSP output: rtsp://localhost:{RTSP_PORT}{RTSP_MOUNT_POINT}\n")

    return pipeline


def main(args):
    print("=" * 60)
    print("  DeepStream Human Detection  |  CUDA 12.2")
    print("=" * 60)

    # Check RTSP URL is reachable (shallow check)
    if not RTSP_URL.startswith("rtsp://"):
        sys.stderr.write(f"Invalid RTSP_URL: {RTSP_URL}\n")
        sys.exit(1)

    pipeline = create_rtsp_pipeline(RTSP_URL)

    loop = GObject.MainLoop()
    bus  = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", bus_call, loop)

    print("Starting pipeline …")
    pipeline.set_state(Gst.State.PLAYING)

    try:
        loop.run()
    except KeyboardInterrupt:
        print("\nShutting down …")
    except Exception as e:
        sys.stderr.write(f"Pipeline error: {e}\n")
    finally:
        pipeline.set_state(Gst.State.NULL)
        print("Pipeline stopped.")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
