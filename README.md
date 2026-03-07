# Camera Analyst - AI-Powered F&B Management System

## Overview

**Camera Analyst** is an advanced Artificial Intelligence system designed for the Food & Beverage (F&B) industry. It transforms traditional surveillance cameras into active business intelligence tools. By analyzing video feeds in real-time, the system provides actionable insights regarding staff performance, food quality control, and customer behavior, helping restaurant owners optimize operations and reduce costs.

## Key Features

The system consists of several core AI modules:

1.  **AI Biometric Attendance**: Automated staff check-in/check-out using facial recognition, capable of adapting to appearance changes over time.
2.  **Human Action Recognition (HAR)**: Analyzes staff movements to distinguish between active working time and idle time, providing a true measure of labor efficiency.
3.  **Food Quality Matching**: "Digital Chef" that compares outgoing dishes against master images to ensure consistency in presentation and portioning before they reach the customer.
4.  **Customer Flow Analytics**: Counts customers, tracks dwell time, and analyzes service speed to improve customer experience.
5.  **Automated Reporting**: Consolidates data into actionable financial and operational reports.

## Web Interface Modules

The application includes the following dashboards and interfaces (located in `app_s/`):

*   **Authentication**: `login.html`, `admin_login`
*   **Executive Dashboard**: `dashboard.html`, `executive_dashboard_desktop`
*   **Live Monitoring**: `live-view.html`, `live_camera_streaming_grid_view`
*   **Staff Management**:
    *   Attendance: `staff-attendance.html`, `staff_attendance_report_desktop`
    *   Performance: `staff-performance.html`, `staff_performance_desktop`
    *   Receptionist: `receptionist-dashboard.html`, `receptionist_performance_dashboard`
*   **Operational Analytics**:
    *   Kitchen Traffic: `kitchen-analytics.html`, `kitchen_traffic_analytics`
    *   Food QC: `food-qc.html`, `food_qc_monitor_desktop`
    *   Customer Flow: `customer-analytics.html`, `customer_flow_analytics_desktop`
*   **System Configuration**:
    *   Camera/RTSP Setup: `rtsp-setup.html`, `camera_configuration_rtsp_setup`
    *   AI Configuration: `camera_ai_configuration`

## Getting Started

### Prerequisites

*   Python 3.x

### Installation & Running

1.  Clone the repository or download the project files.
2.  Navigate to the project root directory.
3.  Run the included server script:

    ```bash
    python3 run_server.py
    ```

4.  Open your web browser and navigate to:
    *   **Login**: http://localhost:8000/login.html
    *   **Dashboard**: http://localhost:8000/dashboard.html

## Project Structure

```
AI_camera/
├── app/                  # Web application source files (HTML, assets)
│   ├── admin_login/
│   ├── camera_ai_configuration/
│   ├── customer_flow_analytics_desktop/
│   ├── ... (other modules)
│   ├── *.html              # Main interface pages
├── run_server.py           # Python script to host the web app locally
├── camera_analyst.md       # Detailed project documentation and specs
├── skills.md               # Technical skills and architecture notes
└── README.md               # This file
```

## Security & Privacy

*   **Edge Processing**: Video data is processed locally at the restaurant (Edge Server) to ensure privacy.
*   **Data Minimization**: Only metadata and statistical reports are sent to the cloud.
*   **Face Vectorization**: Facial data is stored as mathematical vectors, not images.

## Contact

**DSC-Labs** - [Contact Information]
