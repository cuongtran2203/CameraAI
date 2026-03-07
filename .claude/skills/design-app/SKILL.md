# DeepStream Application Design Skill

## Description
This skill provides architectural and implementation guidance for building a full-stack AI Video Analytics application on top of NVIDIA DeepStream. It covers user management, dynamic camera provisioning, and interactive ROI (Region of Interest) configuration.

## Core Modules

### 1. User Authentication & Authorization
- **Login System**: Secure JWT (JSON Web Token) or Session-based authentication.
- **Role-Based Access Control (RBAC)**: Admin (system config), Operator (view/acknowledge alerts), Viewer (read-only).
- **Security**: Password hashing (Argon2/Bcrypt), HTTPS/TLS enforcement.

### 2. Camera Management System
- **Dynamic Source Addition**:
  - APIs to add/edit/remove RTSP, USB, or File sources without restarting the entire application (using `nvmultiurisrcbin` or dynamic pad linking).
- **Health Monitoring**:
  - Detect stream loss/reconnection logic.
  - Snapshot generation for thumbnails.
- **Database Schema**:
  - `Camera` table: ID, Name, RTSP URL, Location, Status, Resolution.

### 3. ROI (Region of Interest) Configuration
- **Interactive Frontend**:
  - Web-based canvas (React/Vue + Konva/Fabric.js) to draw Polygons (Zones) and Lines (Tripwires).
  - Coordinate scaling (Frontend Canvas resolution -> Video Stream resolution).
- **Backend Integration**:
  - API to save ROI coordinates (JSON) to database.
  - Conversion of coordinates to DeepStream configuration formats (e.g., `nvdsanalytics` config file generation).
- **DeepStream Mapping**:
  - Mapping ROI IDs to analytics metadata (e.g., "Zone 1" entry/exit counts).

## Architecture Patterns

### Backend
- **Framework**: Python (FastAPI/Flask) or Go/Node.js.
- **Database**: PostgreSQL (relational data) + Redis (hot state/stream cache).
- **Communication**: REST API for management; WebSocket/gRPC for real-time alerts/metadata.

### Frontend
- **Video Player**: WebRTC (via WHIP/WHEP or KVS) or HLS/MSE for low-latency live view.
- **Overlays**: Drawing ROI zones directly over the live video element.

### DeepStream Integration
- **Config Hot-Reloading**: seamless updates of ROI configs.
- **Metadata Handling**: Extracting object metadata (bounding boxes) and analytics events (line crossing) from GStreamer buffers to send to the backend.

## Example Prompts
- "Design a database schema for storing RTSP camera details and their associated ROI polygons."
- "How do I implement a React component to draw a tripwire over a video stream?"
- "Show me how to update the `nvdsanalytics` config file dynamically when a user saves a new zone."
- "Create a FastAPI endpoint to authenticate a user and return a JWT."

## Technical Constraints
- **Coordinate Systems**: Ensure translation between UI coordinates (0-1 float or pixel) and DeepStream source resolution.
- **Concurrency**: Handle multiple users configuring cameras simultaneously.
- **Performance**: Ensure the ROI overlay does not lag behind the video stream.
