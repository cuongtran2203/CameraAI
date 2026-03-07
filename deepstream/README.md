# DeepStream Project Structure

This directory contains the template for a DeepStream AI application.

## Directory Structure

*   `configs/`: Configuration files for DeepStream elements (GIE, Tracker, Sources).
    *   `deepstream_config.txt`: Main application configuration file.
*   `src/`: Source code for the application.
    *   `main.py`: Main entry point for the Python application.
    *   `api/`: API endpoints for controlling the application (FastAPI/Flask).
    *   `core/`: Core logic for pipeline management and inference handling.
*   `scripts/`: Helper scripts for deployment and management.

## Prerequisites

*   NVIDIA Jetson or dGPU system
*   DeepStream SDK installed (version 6.x or later recommended)
*   Python 3.x
*   GStreamer plugins

## Usage

1.  Navigate to `src/`.
2.  Run the main application:
    ```bash
    python3 main.py
    ```

## Customization

*   Edit `configs/deepstream_config.txt` to add/remove sources or change model paths.
*   Modify `src/main.py` to implement custom logic for metadata processing or integration with external systems.
