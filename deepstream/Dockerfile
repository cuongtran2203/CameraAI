# Base image: NVIDIA DeepStream 6.3 for dGPU (change to 'triton' or 'jetson' if needed)
# For Jetson, use: nvcr.io/nvidia/deepstream-l4t:6.3-samples
FROM nvcr.io/nvidia/deepstream:8.0-gc-triton-devel

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

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

# Install pyds (DeepStream Python Bindings)
# Note: In DeepStream 6.3+, pyds is often available via pip or pre-installed scripts.
# We will download and install the bindings from the official repo compatible with DS 6.3.
WORKDIR /opt/nvidia/deepstream/deepstream
RUN apt-get update && apt-get install -y git cmake && \
    git clone https://github.com/NVIDIA-AI-IOT/deepstream_python_apps.git && \
    cd deepstream_python_apps && \
    git checkout v1.1.8 && \
    cd bindings && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j$(nproc) && \
    pip3 install pyds-*.whl

# Create app directory
WORKDIR /app

# Copy application code
COPY configs/ ./configs/
COPY src/ ./src/
COPY scripts/ ./scripts/

# Expose RTSP port
EXPOSE 8554

# Set entrypoint
CMD ["python3", "src/main.py"]
