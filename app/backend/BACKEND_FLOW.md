# Backend Architecture - Camera AI System

## 1. Tổng Quan Luồng Hoạt Động

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    AI System                                            │
│                                                                                         │
│   DeepStream/Python AI ──gửi JSON──▶ Kafka Broker (ai.tracking)                      │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              │ Kafka Consumer lắng nghe
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND (FastAPI)                                          │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  1. app/main.py                                                               │    │
│  │     - Khởi tạo FastAPI app                                                  │    │
│  │     - Gọi start_kafka_consumer() khi app start                             │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                              │                                           │
│                                              ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  2. app/services/kafka_service.py                                            │    │
│  │     - KafkaConsumerService: Lắng nghe Kafka topics                          │    │
│  │     - handle_tracking(): Xử lý tracking message                             │    │
│  │     - handle_face_detection(): Xử lý face detection                        │    │
│  │     - handle_action_detection(): Xử lý HAR (hành động)                     │    │
│  │     - handle_food_detection(): Xử lý Food QC                               │    │
│  │     - handle_customer_detection(): Xử lý Customer events                    │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                              │                                           │
│                                              ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  3. Database Operations (trong mỗi handler)                                 │    │
│  │     - Kết nối PostgreSQL qua AsyncSessionLocal                              │    │
│  │     - Lưu vào các bảng: CustomerEvent, StaffAction, FoodQCResult...       │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                              │                                           │
│                                              ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  4. WebSocket Broadcast                                                      │    │
│  │     - Gọi broadcast_tracking_update()                                      │    │
│  │     - Gửi real-time cho Frontend qua app/api/websocket.py                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Cấu Trúc Thư Mục và Chức Năng

```
app/backend/
├── app/
│   ├── main.py                          # 🔑 ENTRY POINT
│   │   - Khởi tạo FastAPI app
│   │   - Gọi init_db() tạo database
│   │   - Gọi start_kafka_consumer() lắng nghe Kafka
│   │   - Đăng ký các routers
│   │
│   ├── api/                             # 📡 API ROUTES
│   │   ├── __init__.py                  # Export all routers
│   │   ├── auth.py                      # Login, Register, JWT
│   │   ├── cameras.py                   # Camera CRUD
│   │   ├── staff.py                     # Staff CRUD
│   │   ├── dashboard.py                 # Dashboard stats
│   │   ├── food.py                      # Food items, Food QC
│   │   └── websocket.py                 # 🔌 WebSocket handlers
│   │       - ConnectionManager: Quản lý kết nối WS
│   │       - websocket_dashboard(): Endpoint /ws/dashboard
│   │       - simulate_ai_stream_updates(): Test data
│   │
│   ├── db/                              # 🗄️ DATABASE
│   │   ├── database.py                  # SQLAlchemy config
│   │   │   - engine, AsyncSessionLocal
│   │   │   - settings (từ .env)
│   │   │
│   ├── models/                          # 📊 DATABASE MODELS
│   │   ├── models.py                    # SQLAlchemy ORM classes
│   │   │   - Company, Branch, User
│   │   │   - Staff, StaffFace, Shift
│   │   │   - Camera, CameraAIConfig
│   │   │   - AttendanceRecord, DailyAttendance
│   │   │   - StaffAction, DailyStaffPerformance
│   │   │   - FoodItem, FoodMasterImage, FoodQCResult
│   │   │   - CustomerEvent, HourlyCustomerStats
│   │   │
│   ├── schemas/                         # 📝 PYDANTIC SCHEMAS
│   │   ├── schemas.py                    # Request/Response models
│   │   │
│   └── services/                        # 🔧 BUSINESS LOGIC
│       └── kafka_service.py             # 📨 KAFKA HANDLERS
│           - KafkaProducerService: Gửi message cho AI
│           - KafkaConsumerService: Nhận message từ AI
│           - handle_tracking(): Xử lý tracking
│           - handle_face_detection(): Xử lý face
│           - handle_action_detection(): Xử lý HAR
│           - handle_food_detection(): Xử lý Food QC
│           - handle_customer_detection(): Xử lý customer
│
├── requirements.txt                     # Python dependencies
├── .env                                 # Environment variables
└── docker-compose.yml                   # Docker services
```

---

## 3. Luồng Xử Lý Chi Tiết

### A. Nhận Message từ AI (Kafka Consumer)

```
1. AI gửi message lên Kafka
   Topic: ai.tracking
   {
     "timestamp": "2026-03-14T10:30:00Z",
     "number_of_human": 5,
     "type": "tracking",
     "camera_id": "cam-001"
   }

2. main.py ──▶ start_kafka_consumer()
   ├── Khởi tạo KafkaConsumerService
   ├── Đăng ký handlers:
   │   └── KafkaTopics.AI_TRACKING → handle_tracking

3. KafkaConsumerService._consume_loop()
   ├── Lắng nghe topic ai.tracking
   ├── Khi có message → Gọi handler(message.value)

4. handle_tracking(message)
   ├── Parse JSON message
   ├── Gọi save_tracking_to_db()
   │   └── Tạo CustomerEvent
   │   └── Cập nhật HourlyCustomerStats
   └── Gọi broadcast_tracking_update()
       └── Gửi qua WebSocket cho Frontend
```

### B. Các Handler và Chức Năng

| Handler | Topic | Xử Lý | Database |
|---------|-------|--------|----------|
| `handle_tracking` | `ai.tracking` | Đếm số người | `CustomerEvent`, `HourlyCustomerStats` |
| `handle_face_detection` | `ai.face.detections` | Nhận diện khuôn mặt, chấm công | `AttendanceRecord`, `DailyAttendance` |
| `handle_action_detection` | `ai.action.detections` | Nhận diện hành động (HAR) | `StaffAction`, `DailyStaffPerformance` |
| `handle_food_detection` | `ai.food.detections` | Kiểm tra chất lượng món ăn | `FoodQCResult` |
| `handle_customer_detection` | `ai.customer.detections` | Theo dõi khách hàng | `CustomerEvent`, `HourlyCustomerStats` |

---

## 4. Cách Debug

### Debug 1: Kiểm tra Kafka nhận được message chưa

```bash
# Xem messages trong topic (Kafka UI)
# Truy cập: http://localhost:8080
# Chọn topic: ai.tracking
# Click "Messages" để xem

# Hoặc dùng command line
docker exec kafka kafka-console-consumer \
  --topic ai.tracking \
  --bootstrap-server localhost:29092 \
  --from-beginning
```

### Debug 2: Kiểm tra Backend log

```bash
# Backend đang chạy sẽ hiển thị log:
# - "Tracking: camera=..., humans=..."
# - "Tracking data saved to DB: ..."
# - "Broadcasted tracking update: ..."
```

### Debug 3: Kiểm tra Database

```bash
# Kiểm tra PostgreSQL
docker exec -it postgres psql -U ngohongnguyen -d camera_analyst

# Xem dữ liệu
SELECT * FROM customer_events;
SELECT * FROM hourly_customer_stats;
```

### Debug 4: Kiểm tra WebSocket

```javascript
// Mở Browser Console
// Kết nối WebSocket
const ws = new WebSocket('ws://localhost:8080/ws/dashboard');

ws.onmessage = (event) => {
  console.log('Received:', JSON.parse(event.data));
};
```

---

## 5. File Quan Trọng Khi Debug

| Vấn Đề | File Cần Xem |
|---------|--------------|
| Kafka không nhận message | `kafka_service.py` - `_create_consumer()` |
| Handler không được gọi | `main.py` - `start_kafka_consumer()` |
| Lưu DB lỗi | `kafka_service.py` - `save_*_to_db()` |
| WebSocket không gửi được | `websocket.py` - `broadcast_tracking_update()` |
| Không kết nối được DB | `database.py` - `AsyncSessionLocal` |
| Models không đúng | `models.py` - SQLAlchemy classes |

---

## 6. Test Manual

```bash
# 1. Gửi message test
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/backend
python3 test_kafka_producer.py

# 2. Kiểm tra Backend log
# Sẽ thấy:
# - Tracking: camera=cam-entrance-001, humans=3
# - Tracking data saved to DB: {...}
# - Broadcasted tracking update: ...

# 3. Kiểm tra Database
docker exec -it postgres psql -U ngohongnguyen -d camera_analyst
SELECT * FROM customer_events ORDER BY created_at DESC LIMIT 5;
```
