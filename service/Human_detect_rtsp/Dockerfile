FROM nvcr.io/nvidia/deepstream:8.0-triton-multiarch
# convert

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    cmake \
    dos2unix \
    gir1.2-gst-rtsp-server-1.0 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/marcoslucianops/DeepStream-Yolo.git /opt/DeepStream-Yolo

ENV CUDA_VER=12.8 
# 12.2

RUN dos2unix /opt/DeepStream-Yolo/nvdsinfer_custom_impl_Yolo/Makefile && \
    make -C /opt/DeepStream-Yolo/nvdsinfer_custom_impl_Yolo clean && \
    make -C /opt/DeepStream-Yolo/nvdsinfer_custom_impl_Yolo

# Cài pyds Python bindings cho DeepStream 8.0 (Python 3.12, x86_64)
RUN pip3 install --no-cache-dir \
    https://github.com/NVIDIA-AI-IOT/deepstream_python_apps/releases/download/v1.2.2/pyds-1.2.2-cp312-cp312-linux_x86_64.whl

# Cài Kafka client cho Python
RUN pip3 install --no-cache-dir kafka-python

# Xoá các thư viện Audio Gstreamer không dùng để tránh log rác
RUN rm -f \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstresindvd.so \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstdvdread.so \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstmpg123.so \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/deepstream/libnvdsgst_udp.so \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstpulseaudio.so \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstdtsdec.so \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstlame.so \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstmplex.so \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstopenmpt.so \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstsndfile.so \
    /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstfluidsynthmidi.so

COPY . /workspace

ENV NVIDIA_DRIVER_CAPABILITIES=all

CMD ["python3", "/workspace/app.py", "--input", "file:///workspace/videos/test.mp4"]