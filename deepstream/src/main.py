#!/usr/bin/env python3

import sys
import gi
import configparser
import os
import time
import math

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import GObject, Gst, GstRtspServer

# Attempt to import pyds (DeepStream Python Bindings)
try:
    import pyds
except ImportError:
    sys.stderr.write("Note: pyds not found. This script requires DeepStream SDK installed.\n")

# Configuration for RTSP Server
RTSP_PORT = "8554"
RTSP_MOUNT_POINT = "/ds-test"
UDP_PORT = 5400

def osd_sink_pad_buffer_probe(pad, info, u_data):
    """
    Probe function to extract metadata from the GStreamer buffer.
    Based on the reference documentation.
    """
    gst_buffer = info.get_buffer()
    if not gst_buffer:
        print("Unable to get GstBuffer")
        return Gst.PadProbeReturn.OK

    # Retrieve Batch Metadata from pyds
    # Note: Requires pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    try:
        batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    except NameError:
        # pyds not installed/imported
        return Gst.PadProbeReturn.OK

    l_frame = batch_meta.frame_meta_list
    while l_frame is not None:
        try:
            # Cast data to NvDsFrameMeta
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        # print(f"Frame Number: {frame_meta.frame_num}, Stream: {frame_meta.pad_index}, Objects: {frame_meta.num_obj_meta}")

        l_obj = frame_meta.obj_meta_list
        while l_obj is not None:
            try:
                # Cast data to NvDsObjectMeta
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break

            # Example: Accessing object data
            # print(f"Object Class: {obj_meta.class_id}, Label: {obj_meta.obj_label}")

            # Example: Modifying OSD color (Red) for specific class
            # obj_meta.rect_params.border_color.set(1.0, 0.0, 0.0, 1.0)

            try:
                l_obj = l_obj.next
            except StopIteration:
                break

        try:
            l_frame = l_frame.next
        except StopIteration:
            break

    return Gst.PadProbeReturn.OK

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End of stream\n")
        loop.quit()
    elif t == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        sys.stderr.write("Warning: %s: %s\n" % (err, debug))
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()
    return True

def main(args):
    # Standard GStreamer initialization
    GObject.threads_init()
    Gst.init(None)

    # Create Pipeline
    print("Creating Pipeline \n ")
    pipeline = Gst.Pipeline()
    if not pipeline:
        sys.stderr.write(" Unable to create Pipeline \n")

    # 1. Source & Muxer
    # For template, using a simple URI source (e.g., file or RTSP)
    # In production, use nvmultiurisrcbin or create multiple sources dynamically
    source = Gst.ElementFactory.make("uridecodebin", "uri-source")
    source.set_property("uri", "file:///opt/nvidia/deepstream/deepstream/samples/streams/sample_720p.mp4") # Default sample

    streammux = Gst.ElementFactory.make("nvstreammux", "Stream-muxer")
    streammux.set_property('width', 1920)
    streammux.set_property('height', 1080)
    streammux.set_property('batch-size', 1)

    # 2. Inference & Tracking
    pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
    pgie.set_property('config-file-path', "configs/config_infer_primary.txt")

    tracker = Gst.ElementFactory.make("nvtracker", "tracker")
    # Note: detailed tracker config is usually in a separate file

    # 3. Visualization & Converter
    nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "convertor")

    nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay")

    # 4. RTSP Output Chain
    # OSD -> Convert -> Enc -> Pay -> UDP Sink
    nvvidconv_post = Gst.ElementFactory.make("nvvideoconvert", "convertor_post")
    caps = Gst.ElementFactory.make("capsfilter", "filter")
    caps.set_property("caps", Gst.Caps.from_string("video/x-raw(memory:NVMM), format=I420"))

    encoder = Gst.ElementFactory.make("nvv4l2h264enc", "encoder")
    encoder.set_property('bitrate', 4000000)

    # rtppay
    rtppay = Gst.ElementFactory.make("rtph264pay", "rtppay")

    # UDP Sink
    updsink_port_num = 5400
    sink = Gst.ElementFactory.make("udpsink", "udpsink")
    sink.set_property('host', '224.224.255.255')
    sink.set_property('port', updsink_port_num)
    sink.set_property('async', False)
    sink.set_property('sync', 1)

    # Add elements to pipeline
    pipeline.add(source)
    pipeline.add(streammux)
    pipeline.add(pgie)
    pipeline.add(tracker)
    pipeline.add(nvvidconv)
    pipeline.add(nvosd)
    pipeline.add(nvvidconv_post)
    pipeline.add(caps)
    pipeline.add(encoder)
    pipeline.add(rtppay)
    pipeline.add(sink)

    # Linking
    # Note: uridecodebin uses dynamic pads, need to link manually
    def decodebin_pad_added(decodebin, pad):
        print("Pad added to decodebin")
        sink_pad = streammux.get_request_pad("sink_0")
        if not sink_pad:
            sys.stderr.write("Unable to get the sink pad of streammux \n")
        pad.link(sink_pad)

    source.connect("pad-added", decodebin_pad_added)

    streammux.link(pgie)
    pgie.link(tracker)
    tracker.link(nvvidconv)
    nvvidconv.link(nvosd)

    # Link OSD to Output Chain
    nvosd.link(nvvidconv_post)
    nvvidconv_post.link(caps)
    caps.link(encoder)
    encoder.link(rtppay)
    rtppay.link(sink)

    # Add Probe
    osdsinkpad = nvosd.get_static_pad("sink")
    if not osdsinkpad:
        sys.stderr.write(" Unable to get sink pad of nvosd \n")
    else:
        osdsinkpad.add_probe(Gst.PadProbeType.BUFFER, osd_sink_pad_buffer_probe, 0)

    # Start RTSP Server
    server = GstRtspServer.RTSPServer.new()
    server.props.service = RTSP_PORT
    server.attach(None)

    factory = GstRtspServer.RTSPMediaFactory.new()
    factory.set_launch(
        f"( udpsrc name=pay0 port={updsink_port_num} caps=\"application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96\" )"
    )
    factory.set_shared(True)
    server.get_mount_points().add_factory(RTSP_MOUNT_POINT, factory)

    print(f"\n *** RTSP Streaming at rtsp://localhost:{RTSP_PORT}{RTSP_MOUNT_POINT} *** \n")

    # Start Pipeline
    loop = GObject.MainLoop()
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)

    print("Starting pipeline \n")
    pipeline.set_state(Gst.State.PLAYING)

    try:
        loop.run()
    except:
        pass

    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
