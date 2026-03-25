FROM nvcr.io/nvidia/deepstream:8.0-triton-multiarch

WORKDIR /workspace

# 1. Install system and development dependencies
# Added python3-dev and gstreamer dev headers required for building pyds
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    cmake \
    dos2unix \
    gir1.2-gst-rtsp-server-1.0 \
    python3-pip \
    python3-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Symlink existing CUDA 12.8 to 12.2 path
# This keeps your specific Makefile and environment requirements intact
RUN mkdir -p /usr/local/cuda-12.2 \
    && ln -sfn /usr/local/cuda-12.8/bin /usr/local/cuda-12.2/bin \
    && ln -sfn /usr/local/cuda-12.8/include /usr/local/cuda-12.2/include \
    && ln -sfn /usr/local/cuda-12.8/lib64 /usr/local/cuda-12.2/lib64 \
    && ln -sfn /usr/local/cuda-12.8/extras /usr/local/cuda-12.2/extras \
    && ln -sfn /usr/local/cuda-12.8/nvvm /usr/local/cuda-12.2/nvvm

# 3. Build DeepStream-Yolo Custom Parser
RUN git clone https://github.com/marcoslucianops/DeepStream-Yolo.git /opt/DeepStream-Yolo
ENV CUDA_VER=12.2

RUN dos2unix /opt/DeepStream-Yolo/nvdsinfer_custom_impl_Yolo/Makefile && \
    CUDA_HOME=/usr/local/cuda-12.2 make -C /opt/DeepStream-Yolo/nvdsinfer_custom_impl_Yolo clean && \
    CUDA_HOME=/usr/local/cuda-12.2 make -C /opt/DeepStream-Yolo/nvdsinfer_custom_impl_Yolo

# 4. Build pyds (Python Bindings) from source
# We initialize submodules and point CMAKE to our 12.2 symlinks
RUN pip3 install --no-cache-dir pybind11 && \
    git clone --depth 1 https://github.com/NVIDIA-AI-IOT/deepstream_python_apps.git /opt/deepstream_python_apps && \
    cd /opt/deepstream_python_apps && \
    git submodule update --init && \
    cd bindings && \
    CUDA_PATH=/usr/local/cuda-12.2 \
    CUDACXX=/usr/local/cuda-12.2/bin/nvcc \
    python3 setup.py build && \
    cp build/lib*/pyds*.so /usr/local/lib/python3.12/dist-packages/pyds.so && \
    cd / && rm -rf /opt/deepstream_python_apps

# 5. Install Python Kafka client
RUN pip3 install --no-cache-dir kafka-python

# 6. Cleanup unused Audio Gstreamer libraries to reduce logs/bloat
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

# 7. Final setup
COPY . /workspace
ENV NVIDIA_DRIVER_CAPABILITIES=all

CMD ["python3", "/workspace/app.py", "--input", "file:///workspace/videos/test.mp4"]