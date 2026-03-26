FROM nvcr.io/nvidia/deepstream:7.0-gc-triton-devel

WORKDIR /workspace

# 1. Cài đặt các thư viện hệ thống cần thiết
RUN rm -f /etc/apt/sources.list.d/librealsense*.list \
 && sed -i '/librealsense\.intel\.com/d' /etc/apt/sources.list \
 && apt-get update --allow-insecure-repositories \
 && apt-get install -y --allow-unauthenticated --no-install-recommends \
    git build-essential cmake dos2unix \
    gir1.2-gst-rtsp-server-1.0 python3-pip python3-dev \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libglib2.0-dev \
    libmpg123-0 libmpeg2-4 libmpeg2encpp-2.1-0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 2. Thiết lập biến môi trường CUDA cho RTX 3050 (DeepStream 7.0)
ENV CUDA_VER=12.2
ENV CUDA_HOME=/usr/local/cuda-12.2
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# 3. Build DeepStream-Yolo Parser (Bắt buộc để parse output YOLOv26)
RUN git clone --depth=1 https://github.com/marcoslucianops/DeepStream-Yolo.git /opt/DeepStream-Yolo && \
    make -C /opt/DeepStream-Yolo/nvdsinfer_custom_impl_Yolo clean && \
    make -C /opt/DeepStream-Yolo/nvdsinfer_custom_impl_Yolo

# 4. Copy toàn bộ project (bao gồm file yolo26s.onnx mới ở thư mục models/)
COPY . /workspace

# 5. Build pyds (Bindings Python cho DeepStream)
RUN pip3 install --no-cache-dir pybind11 && \
    git clone https://github.com/NVIDIA-AI-IOT/deepstream_python_apps.git /opt/deepstream_python_apps && \
    cd /opt/deepstream_python_apps && git checkout v1.1.11 && \
    git submodule update --init && cd bindings && \
    mkdir -p build && cd build && cmake .. && make -j$(nproc) && \
    pip3 install pyds-*.whl && rm -rf /opt/deepstream_python_apps

# 6. Cài đặt Kafka và OpenCV cho ứng dụng
RUN pip3 install --no-cache-dir kafka-python opencv-python

# 7. Dọn dẹp để tránh xung đột driver âm thanh
RUN rm -f /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstpulseaudio.so

ENV NVIDIA_DRIVER_CAPABILITIES=all

# 8. Chạy ứng dụng
CMD ["python3", "app.py", "--input", "file:///workspace/videos/test.mp4"]