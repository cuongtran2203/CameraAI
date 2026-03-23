# Base image: NVIDIA DeepStream with CUDA 12.2 for dGPU
# Use DS 7.0 which ships with CUDA 12.2
FROM nvcr.io/nvidia/deepstream:7.0-gc-triton-devel

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
# Force CUDA 12.2 runtime
ENV CUDA_HOME=/usr/local/cuda-12.2
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# Install system dependencies and Python tools
RUN apt-get update && apt-get install -y \
    python3-gi \
    python3-dev \
    python3-gst-1.0 \
    python3-numpy \
    python3-opencv \
    python3-pip \
    libgstrtspserver-1.0-0 \
    gstreamer1.0-rtsp \
    libgirepository1.0-dev \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pyds (DeepStream Python Bindings) compatible with DS 7.0 / CUDA 12.2
# Try pip first (works for DS 6.4+)
RUN pip3 install --no-cache-dir pyds || true

# If pyds not available via pip, build from source (DS 7.0 compatible)
RUN if ! python3 -c "import pyds" 2>/dev/null; then \
    apt-get update && apt-get install -y git cmake && \
    cd /opt/nvidia/deepstream/deepstream && \
    git clone https://github.com/NVIDIA-AI-IOT/deepstream_python_apps.git && \
    cd deepstream_python_apps && \
    git checkout v1.1.10 && \
    cd bindings && \
    mkdir -p build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make -j$(nproc) && \
    pip3 install pyds-*.whl || true; \
    fi

# Create app directory
WORKDIR /app

# Copy application code
COPY configs/ ./configs/
COPY src/ ./src/

# Expose RTSP port
EXPOSE 8554

# Set entrypoint
CMD ["python3", "src/main.py"]
