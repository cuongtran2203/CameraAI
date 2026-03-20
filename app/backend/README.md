# Camera AI - Hướng Dẫn Cài Đặt Toàn Diện

> **Mục tiêu:** Hướng dẫn đầy đủ để developer mới có thể setup và chạy toàn bộ hệ thống (BE + FE) trong 10 phút.

---

## 📋 Mục Lục

1. [Yêu Cầu Hệ Thống](#-yêu-cầu-hệ-thống)
2. [Cài Đặt Nhanh](#-cài-đặt-nhanh)
3. [Chạy Backend](#-chạy-backend)
4. [Chạy Frontend](#-chạy-frontend)
5. [Seed Data (Mock Data)](#-seed-data-mock-data)
6. [API Endpoints](#-api-endpoints)
7. [WebSocket](#-websocket)
8. [Mock Data cho AI](#-mock-data-cho-ai)
9. [Xử Lý Sự Cố](#-xử-lý-sự-cố)

---

## 🖥️ Yêu Cầu Hệ Thống

| Phần mềm | Phiên bản | Ghi chú |
|----------|-----------|---------|
| macOS / Linux | - | Windows cần điều chỉnh đường dẫn |
| Python | 3.9+ | Khuyến nghị Python 3.11 |
| Node.js | 18+ | Cho Frontend |
| Docker Desktop | 4.0+ | Cho PostgreSQL, Redis, Kafka |

### Kiểm tra cài đặt:

```bash
# Python
python3 --version

# Node.js
node --version

# Docker (trên macOS cần đường dẫn đầy đủ)
/Applications/Docker.app/Contents/Resources/bin/docker --version
```

---

## 🚀 Cài Đặt Nhanh

### 1. Clone code và di chuyển vào thư mục

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app
```

### 2. Cài đặt Backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Cài đặt Frontend dependencies

```bash
cd ../frontend
npm install
```

---

## 🔧 Chạy Backend

### Bước 1: Khởi động Docker Services

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend

# Trên macOS, sử dụng:
/Applications/Docker.app/Contents/Resources/bin/docker compose up -d

# Kiểm tra containers đang chạy:
/Applications/Docker.app/Contents/Resources/bin/docker compose ps
```

**Kết quả mong đợi:**

| Service | Status | Port |
|---------|--------|------|
| postgres | healthy | 5432 |
| redis | healthy | 6379 |
| zookeeper | healthy | 2181 |
| kafka | running | 9092, 29092 |
| kafka-ui | running | 8082 |

### Bước 2: Chạy Backend

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend

# Chạy với hot reload
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

**Backend chạy tại:** http://localhost:8080

---

## 🎨 Chạy Frontend

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/frontend

# Chạy development server
npm run dev
```

**Frontend chạy tại:** http://localhost:5173

---

## 📊 Seed Data (Mock Data)

### Seed Users & Initial Data

```bash
cd /home/cuongtdm/Documents/tructt/service/CameraAI/app/backend

# Chạy seed script để tạo:
# - Tài khoản mặc định
# - Company & Branch
# - Food Items mẫu
# - Cameras
python3 seed_users.py
```

### Tài khoản mặc định

| Email | Password | Role |
|-------|----------|------|
| admin@cameraai.com | admin123 | admin |
| manager@cameraai.com | manager123 | manager |
| staff@cameraai.com | staff123 | staff |

### Tạo Camera thủ công (nếu cần)

```bash
# Kết nối PostgreSQL
psql -h localhost -p 5432 -U ngohongnguyen -d camera_analyst

# Insert camera
INSERT INTO cameras (id, branch_id, name, code, rtsp_url, location, ai_enabled, is_active)
VALUES (
  'cam-001',
  'branch-main-001',
  'Kitchen Camera',
  'CAM001',
  'rtsp://example.com',
  'Kitchen',
  '{"face": true, "action": true, "food": true}'::json,
  true
);
```

---

## 📡 API Endpoints

### Base URL
```
http://localhost:8080/api/v1
```

### Authentication

#### Login
```bash
# Request
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@cameraai.com&password=admin123

# Response
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": "usr-admin-admin",
    "email": "admin@cameraai.com",
    "full_name": "Admin User",
    "role": "admin"
  }
}
```

### Dashboard

#### Get Stats
```bash
GET /dashboard/stats?branch_id=branch-main-001
Authorization: Bearer <token>

# Response
{
  "timestamp": "2026-03-19T10:30:00Z",
  "staff": {
    "total_online": 0,
    "total_scheduled": 5,
    "attendance_rate": 0.0
  },
  "actions": {
    "productive_count": 0,
    "idle_count": 0,
    "top_actions": []
  },
  "food_qc": {
    "total_checked": 0,
    "pass_count": 0,
    "fail_count": 0,
    "warning_count": 0,
    "pass_rate": 0
  },
  "customers": {
    "current_in_store": 0,
    "entry_today": 0,
    "avg_dwell_time_minutes": 0,
    "peak_hour": null
  }
}
```

### Food QC

#### Get QC Results
```bash
GET /food/qc-results?page=1&page_size=10
Authorization: Bearer <token>

# Response
[
  {
    "id": "qc-result-001",
    "camera_id": "cam-001",
    "food_item_id": "food-001",
    "result_status": "passed",
    "similarity_score": 0.942,
    "color_match": true,
    "portion_match": true,
    "topping_present": true,
    "proof_image_url": null,
    "checked_by": "ai",
    "checked_at": "2026-03-19T10:30:00Z"
  }
]
```

#### Get Food Items
```bash
GET /food/items?branch_id=branch-main-001
Authorization: Bearer <token>
```

---

## 🔌 WebSocket

### Kết nối

```javascript
// Frontend
const ws = new WebSocket('ws://localhost:8080/ws/dashboard');

// Listen for messages
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

### Message Types

| Type | Mô tả |
|------|--------|
| `food_qc_result` | Kết quả QC món ăn mới |
| `food_qc_stats` | Thống kê QC |
| `ai_stream_data` | Dữ liệu AI stream |

### Ví dụ Message

```json
{
  "type": "food_qc_result",
  "data": {
    "food_item": "Phở Bò",
    "result_status": "pass",
    "similarity_score": 0.92,
    "color_score": 95.2,
    "portion_score": 90.0
  },
  "timestamp": "2026-03-19T10:30:00Z"
}
```

---

## 🤖 Mock Data cho AI

### Simulation đang chạy

Backend tự động chạy **Food QC Simulation** mỗi 3 giây:
- Sinh data mock giống như AI thật
- Lưu vào database
- Broadcast qua WebSocket

### Mock Data Format

#### Food QC Result (từ AI simulation)

```json
{
  "message_id": "uuid-here",
  "timestamp": "2026-03-19T10:30:00Z",
  "camera_id": "NODE-02",
  "food_item": "Phở Bò",
  "food_category": "main",
  "result_status": "pass",
  "similarity_score": 0.95,
  "color_score": 95.2,
  "portion_score": 92.0,
  "topping_score": 90.5,
  "proof_image_url": "/api/v1/images/proof/abc123.jpg"
}
```

### Tắt/Mở Simulation

Để tắt simulation, sửa `app/main.py`:

```python
# Tắt simulation
async_task = asyncio.create_task(simulate_food_qc_updates(interval_seconds=0))  # 0 = disabled

# Hoặc bật lại
async_task = asyncio.create_task(simulate_food_qc_updates(interval_seconds=3))
```

---

## 📁 Cấu Trúc Project

```
CameraAI/
├── app/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── api/           # API routes
│   │   │   │   ├── auth.py
│   │   │   │   ├── cameras.py
│   │   │   │   ├── dashboard.py
│   │   │   │   ├── food.py
│   │   │   │   ├── staff.py
│   │   │   │   └── websocket.py
│   │   │   ├── db/
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   ├── services/
│   │   │   │   ├── food_qc_service.py  # Food QC simulation
│   │   │   │   └── kafka_service.py    # Kafka handlers
│   │   │   └── main.py
│   │   ├── docker-compose.yml
│   │   ├── seed_users.py
│   │   └── requirements.txt
│   │
│   └── frontend/
│       ├── src/
│       │   ├── views/
│       │   │   ├── DashboardView.vue
│       │   │   ├── FoodQCView.vue
│       │   │   └── RTSPSetupView.vue
│       │   └── services/
│       └── package.json
```

---

## 🔗 Các URLs quan trọng

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8080 |
| **API Docs** | http://localhost:8080/docs |
| **Health Check** | http://localhost:8080/health |
| **Kafka UI** | http://localhost:8082 |

---

## 🔧 Xử Lý Sự Cố

### Lỗi "Connection refused" PostgreSQL

```bash
# Kiểm tra PostgreSQL container
/Applications/Docker.app/Contents/Resources/bin/docker compose ps postgres

# Restart PostgreSQL
/Applications/Docker.app/Contents/Resources/bin/docker compose restart postgres
```

### Lỗi "password authentication failed"

Kiểm tra file `.env`:

```env
DATABASE_URL=postgresql+asyncpg://ngohongnguyen:postgres@localhost:5432/camera_analyst
```

### Lỗi CORS

Backend đã cấu hình `allow_origins=["*"]`. Kiểm tra Frontend gọi đúng URL:

```env
# frontend/.env
VITE_API_URL=http://localhost:8080/api
```

### Docker command not found (macOS)

```bash
# Thêm alias vào ~/.zshrc
echo 'alias docker="/Applications/Docker.app/Contents/Resources/bin/docker"' >> ~/.zshrc
source ~/.zshrc

# Hoặc sử dụng đường dẫn đầy đủ
/Applications/Docker.app/Contents/Resources/bin/docker compose up -d
```

### Không thấy data trên Dashboard

1. Kiểm tra đã đăng nhập chưa
2. Kiểm tra `branch_id` đúng: `branch-main-001`
3. Kiểm tra Backend logs có lỗi không

---

## 📞 Hỗ Trợ

Nếu gặp lỗi không có trong danh sách, kiểm tra:

1. Docker Desktop đang chạy
2. Ports 5432, 6379, 8080, 8082, 9092 không bị chiếm
3. Python và Node.js đúng phiên bản
