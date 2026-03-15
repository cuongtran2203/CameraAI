# Camera Data Flow - Luồng dữ liệu Camera

## Tổng quan luồng dữ liệu

```mermaid
flowchart TB
    subgraph Camera["📹 Camera Physical"]
        direction TB
        C1["IP Camera<br/>Hikvision"]
        C2["RTSP Stream<br/>Video Feed"]
    end

    subgraph EdgeServer["🖥️ Edge AI Server"]
        direction TB
        DS["DeepStream<br/>Pipeline"]

        subgraph AI_Processing["🤖 AI Processing"]
            FD["Face Detection<br/>YOLO-Face"]
            FR["Face Recognition<br/>ArcFace"]
            HAR["Human Action<br/>Recognition"]
            OD["Object Detection<br/>YOLOv8"]
            REID["Re-ID<br/>Person Tracking"]
        end

        DB[( "Database<br/>PostgreSQL" )]
        KAFKA["Kafka<br/>Message Queue"]
    end

    subgraph Backend["🐍 Python Backend"]
        API["FastAPI<br/>REST API"]
    end

    subgraph Frontend["🎨 Vue 3 Frontend"]
        FE["Web Dashboard<br/>Real-time"]
    end

    Camera --> C2 --> DS
    DS --> AI_Processing
    AI_Processing --> DB
    AI_Processing --> KAFKA
    KAFKA --> API
    DB --> API
    API --> FE
```

---

## Chi tiết từng Module

### 1. 📹 Camera Input (Đầu vào từ Camera)

| Thông tin | Mô tả | Ví dụ |
|-----------|-------|-------|
| **RTSP URL** | Đường dẫn stream video | `rtsp://192.168.1.100:554/stream1` |
| **Resolution** | Độ phân giải | 1920x1080 (1080p) |
| **FPS** | Số khung hình/giây | 30 fps |
| **Location** | Vị trí lắp đặt | `kitchen_entrance`, `counter` |

### 2. 🤖 AI Processing (Xử lý AI - Edge Server)

Khi video stream đi qua DeepStream pipeline, hệ thống sẽ **trích xuất** các thông tin sau:

#### A. Nhận diện khuôn mặt (Face Recognition)

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "camera_id": "cam_001",
  "detections": [
    {
      "face_id": "face_abc123",
      "bounding_box": {
        "x": 450,
        "y": 120,
        "width": 80,
        "height": 100
      },
      "embedding": [0.123, -0.456, 0.789, ...],  // 512 dimensions
      "staff_id": "staff_001",
      "confidence": 0.95,
      "liveness": true,
      "action": "check_in"
    }
  ]
}
```

#### B. Phân tích hành động (Human Action Recognition)

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "camera_id": "cam_001",
  "actions": [
    {
      "track_id": "person_001",
      "staff_id": "staff_001",
      "action_type": "cooking",
      "action_label": "chopping_vegetables",
      "confidence": 0.92,
      "duration_seconds": 180,
      "is_productive": true,
      "pose_keypoints": {
        "nose": [450, 120],
        "left_hand": [420, 200],
        "right_hand": [480, 200]
      }
    },
    {
      "track_id": "person_002",
      "action_type": "idle",
      "action_label": "using_phone",
      "confidence": 0.88,
      "duration_seconds": 45,
      "is_productive": false
    }
  ]
}
```

#### C. Kiểm tra chất lượng món ăn (Food QC)

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "camera_id": "cam_kitchen",
  "food_detection": {
    "food_id": "food_001",
    "bounding_box": {
      "x": 300,
      "y": 400,
      "width": 200,
      "height": 150
    },
    "matched_master_image": "master_pho_001",
    "similarity_score": 0.87,
    "result": "warning",
    "details": {
      "color_match": true,
      "portion_match": true,
      "topping_present": false,
      "missing_toppings": ["bean_sprouts", "lime"]
    },
    "staff_id": "staff_003",
    "proof_image_url": "/images/proof/food_qc_001.jpg"
  }
}
```

#### D. Phân tích khách hàng (Customer Flow)

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "camera_id": "cam_entrance",
  "customer_event": {
    "session_id": "cust_session_xyz789",
    "event_type": "entry",
    "zone": "entrance",
    "detected_at": "2024-01-15T10:30:00Z",
    "body_embedding": [0.111, -0.222, 0.333, ...],  // 512 dims for Re-ID
    "clothing_color": "dark_blue",
    "is_staff": false,
    "dwell_time_seconds": null  // null khi mới vào
  }
}
```

---

## 3. 📡 Backend API Response (Frontend nhận gì)

Dưới đây là các API endpoints và data mà **Frontend Vue 3** sẽ nhận được:

### A. Danh sách Camera

**GET** `/api/v1/cameras`

```json
{
  "success": true,
  "data": [
    {
      "id": "cam_001",
      "name": "Camera Quầy Thu Ngân",
      "code": "CAM_COUNTER_01",
      "location": "counter",
      "rtsp_url": "rtsp://192.168.1.100:554/stream1",
      "is_active": true,
      "status": "online",
      "ai_enabled": {
        "face_recognition": true,
        "har": true,
        "food_qc": false,
        "customer_flow": true
      },
      "last_online": "2024-01-15T10:35:00Z"
    },
    {
      "id": "cam_002",
      "name": "Camera Kitchen Exit",
      "code": "CAM_KITCHEN_02",
      "location": "kitchen_exit",
      "is_active": true,
      "status": "online",
      "ai_enabled": {
        "face_recognition": false,
        "har": true,
        "food_qc": true,
        "customer_flow": false
      }
    }
  ],
  "total": 6
}
```

### B. Live Camera Stream

**GET** `/api/v1/cameras/{id}/stream`

```json
{
  "camera_id": "cam_001",
  "stream_url": "ws://192.168.1.50:8000/stream/cam_001",
  "overlay_data": {
    "detections": [
      {
        "type": "person",
        "track_id": 1,
        "staff_id": "staff_001",
        "staff_name": "Nguyễn Văn A",
        "current_action": "cooking",
        "bounding_box": [450, 120, 530, 380]
      },
      {
        "type": "face",
        "staff_id": "staff_002",
        "staff_name": "Trần Thị B",
        "bounding_box": [200, 150, 260, 220],
        "confidence": 0.95
      }
    ]
  }
}
```

### C. Dashboard Statistics

**GET** `/api/v1/dashboard/today`

```json
{
  "success": true,
  "data": {
    "timestamp": "2024-01-15T10:30:00Z",
    "staff": {
      "total_online": 8,
      "total_scheduled": 10,
      "attendance_rate": 0.80,
      "recent_checkins": [
        {
          "staff_id": "staff_001",
          "staff_name": "Nguyễn Văn A",
          "time": "10:15:00",
          "type": "check_in"
        }
      ]
    },
    "actions": {
      "productive_count": 45,
      "idle_count": 12,
      "top_actions": [
        {"action": "cooking", "count": 25},
        {"action": "washing", "count": 15},
        {"action": "idle", "count": 12}
      ]
    },
    "food_qc": {
      "total_checked": 50,
      "pass_count": 45,
      "fail_count": 3,
      "warning_count": 2,
      "pass_rate": 0.90
    },
    "customers": {
      "current_in_store": 15,
      "entry_today": 120,
      "avg_dwell_time_minutes": 25,
      "peak_hour": "12:00"
    }
  }
}
```

### D. Staff Performance

**GET** `/api/v1/staff/performance?date=2024-01-15`

```json
{
  "success": true,
  "data": [
    {
      "staff_id": "staff_001",
      "staff_name": "Nguyễn Văn A",
      "department": "kitchen",
      "check_in": "08:00",
      "check_out": "16:00",
      "total_hours": 8.0,
      "actions_summary": {
        "cooking": 7200,      // seconds
        "washing": 1800,
        "idle": 900,
        "phone_usage": 300
      },
      "productive_time": 15000,
      "idle_time": 1200,
      "productivity_rate": 0.926,
      "earnings": {
        "theoretical": 240000,
        "actual": 222240,
        "saved": 17760
      }
    }
  ]
}
```

### E. Customer Analytics

**GET** `/api/v1/customers/analytics?date=2024-01-15`

```json
{
  "success": true,
  "data": {
    "date": "2024-01-15",
    "total_entry": 156,
    "total_exit": 148,
    "peak_concurrent": 32,
    "avg_dwell_time_minutes": 28,
    "hourly_distribution": [
      {"hour": 10, "entry": 5, "exit": 2, "concurrent": 3},
      {"hour": 11, "entry": 15, "exit": 8, "concurrent": 10},
      {"hour": 12, "entry": 45, "exit": 20, "concurrent": 32},
      {"hour": 13, "entry": 38, "exit": 40, "concurrent": 30}
    ]
  }
}
```

### F. Food QC Results

**GET** `/api/v1/food/qc?date=2024-01-15`

```json
{
  "success": true,
  "data": {
    "date": "2024-01-15",
    "total_checked": 85,
    "pass_rate": 0.92,
    "failed_items": [
      {
        "food_name": "Phở Bò",
        "count": 3,
        "reasons": ["missing_bean_sprouts", "portion_small"]
      }
    ],
    "recent_checks": [
      {
        "id": "qc_001",
        "food_name": "Bún Chả",
        "status": "pass",
        "similarity": 0.94,
        "staff": "Nguyễn Văn A",
        "time": "10:30:15"
      }
    ]
  }
}
```

---

## 4. 🎨 Frontend sẽ hiển thị gì?

### Dashboard View
- Tổng quan KPIs: Số nhân viên online, pass rate, lượng khách
- Biểu đồ thời gian thực
- Thông báo cảnh báo

### Live View
- Video stream với bounding boxes overlay
- Hiển thị tên nhân viên + hành động đang làm
- Real-time updates mỗi 100-500ms

### Staff Performance
- Bảng danh sách nhân viên
- Biểu đồ phân bổ thời gian (pie chart)
- So sánh lương lý thuyết vs thực tế

### Food QC Monitor
- Ảnh món ăn + ảnh mẫu so sánh
- Kết quả Pass/Fail/Warning
- Thống kê theo món

### Customer Analytics
- Biểu đồ lưu lượng theo giờ
- Heat map khu vực
- Thời gian chờ trung bình

---

## 5. 📊 Tóm tắt Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAMERA INPUT                                  │
│  RTSP Stream: rtsp://192.168.1.100:554/stream1                  │
│  Resolution: 1920x1080 @ 30fps                                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                 EDGE AI SERVER (DeepStream)                     │
│                                                                  │
│   Video Frame ──► Detection ──► Tracking ──► Classification    │
│                           │                                      │
│           ┌───────────────┼───────────────┐                     │
│           ▼               ▼               ▼                     │
│      Face Recog      HAR (Action)     Food QC                  │
│           │               │               │                      │
│           ▼               ▼               ▼                     │
│      staff_id        action_type      similarity              │
│      embedding       duration         result                   │
│      confidence     is_productive     proof_image             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    POSTGRES DATABASE                             │
│                                                                  │
│   Tables: cameras, staff, staff_actions, food_qc_results,       │
│           customer_events, daily_reports...                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                              │
│                                                                  │
│   /api/v1/cameras        ──► List cameras                       │
│   /api/v1/dashboard      ──► Dashboard stats                   │
│   /api/v1/staff/actions  ──► Staff actions                      │
│   /api/v1/food/qc       ──► Food QC results                    │
│   /api/v1/customers      ──► Customer analytics                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     VUE 3 FRONTEND                               │
│                                                                  │
│   Views: Dashboard, LiveView, StaffPerformance, FoodQC,         │
│          CustomerAnalytics, CameraConfig...                     │
└─────────────────────────────────────────────────────────────────┘
```

---

Bạn thấy rõ hơn chưa? Cần mình giải thích thêm phần nào không?

Ví dụ:
- Chi tiết hơn về AI model
- Cách setup RTSP stream
- API endpoints cụ thể
