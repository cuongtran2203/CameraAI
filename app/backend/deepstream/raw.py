#!/usr/bin/env python3
import sys
import argparse
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/workspace/videos/test.mp4", help="Path to input mp4 file")
    parser.add_argument("--port", default="8555", help="Port for RTSP server")
    args = parser.parse_args()

    input_path = args.input
    if input_path.startswith("file://"):
        input_path = input_path[7:]

    # Khởi tạo GStreamer
    Gst.init(None)

    # Khởi tạo RTSP Server
    server = GstRtspServer.RTSPServer.new()
    server.set_service(args.port)

    # Pipeline đọc file dạng passthrough
    factory = GstRtspServer.RTSPMediaFactory.new()
    pipeline_str = f'( filesrc location={input_path} ! qtdemux ! h264parse ! rtph264pay pt=96 name=pay0 )'
    factory.set_launch(pipeline_str)
    factory.set_shared(True)

    # Đăng ký endpoint
    server.get_mount_points().add_factory("/ds-raw", factory)

    # Khởi chạy main loop
    server.attach(None)
    print(f"RAW pass-through RTSP server is running at rtsp://0.0.0.0:{args.port}/ds-raw")
    print(f"Streaming file: {args.input}")

    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()