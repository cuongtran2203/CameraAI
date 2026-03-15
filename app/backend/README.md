# Camera AI Backend - Hướng Dẫn Cài Đặt

> ⚠️ **Lưu ý quan trọng:** Docker command trên macOS cần sử dụng đường dẫn đầy đủ:
> ```bash
> /Applications/Docker.app/Contents/Resources/bin/docker
> ```
> Hoặc thêm alias vào `~/.zshrc`:
> ```bash
> echo 'alias docker="/Applications/Docker.app/Contents/Resources/bin/docker"' >> ~/.zshrc
> source ~/.zshrc
> ```

---

## 🚀 Các Bước Chạy Nhanh

### Terminal 1: Chạy Docker Services

```bash
# Bước 1: Di chuyển vào thư mục backend
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend

# Bước 2: Khởi động Docker services (PostgreSQL, Redis, Kafka)
/Applications/Docker.app/Contents/Resources/bin/docker compose up -d

# Bước 3: Kiểm tra các container đang chạy
/Applications/Docker.app/Contents/Resources/bin/docker compose ps
```

### Terminal 2: Chạy Backend

```bash
# Di chuyển vào thư mục backend
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend

# Chạy Backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Terminal 3: Chạy Frontend (nếu cần)

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/frontend
npm run dev
```

---

## 📋 Tổng Hợp Lệnh

| # | Mô tả | Lệnh |
|---|-------|------|
| 1 | Di chuyển vào backend | `cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend` |
| 2 | Chạy Docker | `/Applications/Docker.app/Contents/Resources/bin/docker compose up -d` |
| 3 | Xem logs Docker | `/Applications/Docker.app/Contents/Resources/bin/docker compose logs -f` |
| 4 | Kiểm tra Docker | `/Applications/Docker.app/Contents/Resources/bin/docker compose ps` |
| 5 | Dừng Docker | `/Applications/Docker.app/Contents/Resources/bin/docker compose down` |
| 6 | Chạy Backend | `python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload` |
| 7 | Chạy Frontend | `cd /Users/ngohongnguyen/Documents/works/CameraAI/app/frontend && npm run dev` |

---

## Yêu Cầu Môi Trường

### 1. Python
- **Python 3.9+** (khuyến nghị: Python 3.11)

Kiểm tra phiên bản Python:
```bash
python3 --version
```

### 2. Docker Desktop
- **Docker Desktop** cho macOS/Windows
- Kiểm tra: `docker --version`

### 3. Cài Đặt Dependencies

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend
pip install -r requirements.txt
```

---

## Cài Đặt Infrastructure với Docker

### 1. Khởi động Docker Desktop
- Mở **Docker Desktop** trên máy
- Đợi Docker khởi động hoàn tất

### 2. Chạy Docker Compose

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend
docker compose up -d
```

### 3. Kiểm tra các services đang chạy

```bash
docker compose ps
```

**Kết quả:**

| Service | Port | Mô tả |
|---------|------|--------|
| zookeeper | 2181 | Zookeeper cho Kafka |
| kafka | 9092, 29092 | Kafka Broker |
| kafka-ui | 8082 | Kafka Web UI |
| postgres | 5432 | PostgreSQL Database |
| redis | 6379 | Redis Cache |

### 4. Truy cập Kafka UI
Mở trình duyệt: **http://localhost:8082**

### 5. Tạo Kafka Topics

```bash
# Tạo topic cho tracking
docker exec kafka kafka-topics --create \
  --topic ai.tracking \
  --bootstrap-server localhost:29092 \
  --partitions 1 --replication-factor 1

# Kiểm tra topics đã tạo
docker exec kafka kafka-topics --list \
  --bootstrap-server localhost:29092
```

### 6. Dừng Docker Compose

```bash
docker compose down
```

---

## Cấu Hình Môi Trường (.env)

Tạo file `.env` trong thư mục `app/backend/`:

```env
# =====================================================
# Docker Development (Backend chạy trên host, connect vào Docker services)
# =====================================================
DATABASE_URL=postgresql+asyncpg://ngohongnguyen:postgres@localhost:5432/camera_analyst
DATABASE_URL_SYNC=postgresql+psycopg2://ngohongnguyen:postgres@localhost:5432/camera_analyst
KAFKA_BOOTSTRAP_SERVERS=localhost:29092
REDIS_URL=redis://localhost:6379

# =====================================================
# JWT Authentication
# =====================================================
SECRET_KEY=your-secret-key-change-in-production-use-something-very-secure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## Chạy Ứng Dụng Backend

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend

# Chạy với hot reload (khuyến nghị)
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Hoặc chạy bình thường
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080
```

---

## Luồng Hoạt Động AI ↔ Backend

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                    AI System                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Face         │  │ HAR          │  │ Food QC      │  │ Tracking     │  │
│  │ Detection    │  │ Actions      │  │ Detection    │  │ Human Count  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │                  │          │
│         └──────────────────┴──────────────────┴──────────────────┘          │
│                                      │                                       │
│                                      ▼                                       │
│                           ┌─────────────────────┐                            │
│                           │   Kafka Topics     │                            │
│                           │  ai.face.*         │                            │
│                           │  ai.action.*       │                            │
│                           │  ai.food.*         │                            │
│                           │  ai.tracking       │                            │
│                           └─────────┬──────────┘                            │
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │ (AI gửi về)
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND (FastAPI)                               │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Kafka Consumer Service                               │   │
│  │  - Lắng nghe Kafka topics                                            │   │
│  │  - Gọi handler tương ứng khi có message                              │   │
│  │  - Xử lý và lưu vào Database                                         │   │
│  │  - Broadcast qua WebSocket                                           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Database (PostgreSQL)                               │   │
│  │  - AttendanceRecords, StaffActions, FoodQCResults, CustomerEvents    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### JSON Format từ AI gửi qua Kafka

#### 1. Tracking (Human Counting) - `ai.tracking`
```json
{
  "timestamp": "2026-03-14T10:30:00Z",
  "number_of_human": 5,
  "type": "tracking",
  "camera_id": "cam-001"
}
```

#### 2. Face Detection - `ai.face.detections`
```json
{
  "timestamp": "2026-03-14T10:30:00Z",
  "camera_id": "cam-001",
  "detections": [
    {
      "track_id": "person-123",
      "staff_id": "staff-uuid",
      "event_type": "check_in",
      "confidence": 0.95,
      "face_embedding": [0.123, -0.456, ...],
      "image_url": "https://..."
    }
  ]
}
```

#### 3. Action Detection (HAR) - `ai.action.detections`
```json
{
  "timestamp": "2026-03-14T10:30:00Z",
  "camera_id": "cam-001",
  "actions": [
    {
      "track_id": "person-123",
      "staff_id": "staff-uuid",
      "action_type": "cooking",
      "action_label": "dang nau",
      "confidence": 0.92,
      "duration_seconds": 300,
      "is_productive": true
    }
  ]
}
```

#### 4. Food QC Detection - `ai.food.detections`
```json
{
  "timestamp": "2026-03-14T10:30:00Z",
  "camera_id": "cam-kitchen-001",
  "detections": [
    {
      "food_item_id": "food-001",
      "result_status": "pass",
      "similarity_score": 0.88,
      "color_match": true,
      "portion_match": true,
      "topping_present": true,
      "proof_image_url": "https://...",
      "staff_id": "staff-uuid"
    }
  ]
}
```

#### 5. Customer Detection - `ai.customer.detections`
```json
{
  "timestamp": "2026-03-14T10:30:00Z",
  "camera_id": "cam-entrance-001",
  "events": [
    {
      "session_id": "session-abc123",
      "event_type": "entry",
      "zone": "entrance",
      "dwell_time_seconds": null,
      "clothing_color": "blue",
      "is_staff": false
    }
  ]
}
```

---

## Database Migration

### 1. Cài đặt Alembic

```bash
pip install alembic
```

### 2. Khởi tạo Alembic

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend
alembic init alembic
```

### 3. Cấu hình Alembic

Sửa file `alembic.ini`:
```ini
sqlalchemy.url = postgresql+asyncpg://ngohongnguyen@localhost:5432/camera_analyst
```

Sửa file `alembic/env.py` thêm:
```python
from app.models import Base
target_metadata = Base.metadata
```

### 4. Các lệnh Migration

```bash
# Tạo migration mới
alembic revision --autogenerate -m "create users table"

# Chạy migration
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Xem lịch sử migration
alembic history
```

---

## Seed Data

### Chạy Seed Users

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend

# Seed users (tạo tài khoản mặc định)
python3 seed_users.py
```

### Tài khoản mặc định sau seed

| Email | Password | Role |
|-------|----------|------|
| admin@test.com | admin123 | admin |
| staff@test.com | staff123 | staff |
| manager@test.com | manager123 | manager |

---

## Kiểm Tra

| Service | URL |
|---------|-----|
| **API Docs** | http://localhost:8080/docs |
| **Health Check** | http://localhost:8080/health |
| **Kafka UI** | http://localhost:8082 |

---

## Tài Khoản Mặc Định

| Field | Value |
|-------|-------|
| Email | admin@test.com |
| Password | admin123 |

---

## Cấu Trúc Project

```
app/backend/
├── app/
│   ├── main.py              # Entry point & Kafka Consumer
│   ├── api/                 # API routes
│   │   ├── auth.py
│   │   ├── cameras.py
│   │   ├── staff.py
│   │   ├── dashboard.py
│   │   ├── food.py
│   │   └── websocket.py
│   ├── db/                  # Database config
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Services
│       └── kafka_service.py # Kafka Consumer & Handlers
├── docker-compose.yml       # Docker services
├── SETUP_DOCKER.md          # Hướng dẫn Docker
├── requirements.txt
└── .env
```

---

## Các Kafka Topics

| Topic | Mô tả |
|-------|-------|
| `camera.commands` | Commands từ Backend → AI |
| `ai.config` | AI Configuration |
| `ai.face.detections` | Face detection results |
| `ai.action.detections` | HAR (Human Action Recognition) |
| `ai.food.detections` | Food QC results |
| `ai.customer.detections` | Customer flow detection |
| `ai.tracking` | Human counting/tracking |
