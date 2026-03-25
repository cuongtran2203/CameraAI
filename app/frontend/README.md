# Camera AI Frontend - Hướng Dẫn Cài Đặt

---

## 🚀 Quick Start

### 1. Cài đặt dependencies

```bash
cd /home/cuongtdm/Documents/tructt/service/CameraAI/app/frontend
npm install
```

### 2. Cấu hình Environment

File `.env` đã có sẵn với nội dung:

```env
VITE_API_URL=http://localhost:8080/api
```

### 3. Chạy Development Server

```bash
npm run dev
```

**Frontend chạy tại:** http://localhost:5173

---

## 📋 Scripts

| Command | Mô tả |
|---------|--------|
| `npm run dev` | Chạy development server với hot reload |
| `npm run build` | Build production bundle |
| `npm run preview` | Preview production build |

---

## 🔗 Kết nối Backend

Frontend sử dụng:

| Service | URL |
|---------|-----|
| **API Base** | `http://localhost:8080/api` |
| **WebSocket** | `ws://localhost:8080/ws/dashboard` |

### Authentication

Frontend tự động:
- Đăng nhập → lưu token vào cookie
- Gọi API → attach token vào header
- WebSocket → sử dụng cookie auth

---

## 📱 Các Màn Hình

### 1. Dashboard (`/`)
- Tổng quan metrics
- Staff attendance
- Food QC stats
- Customer count
- Real-time updates qua WebSocket

### 2. Food QC (`/food-qc`)
- Danh sách kết quả QC
- Filter theo ngày, trạng thái
- Real-time updates
- Load more / Collapse

### 3. RTSP Setup (`/rtsp-setup`)
- Quản lý camera streams
- Thêm/Sửa/Xóa camera
- Test RTSP connection

---

## 🔌 API Integration

### Sử dụng API Service

```javascript
import api from './services/api'

// Login
const response = await api.post('/v1/auth/login', {
  email: 'admin@cameraai.com',
  password: 'admin123'
})

// Get Dashboard Stats
const stats = await api.get('/v1/dashboard/stats', {
  params: { branch_id: 'branch-main-001' }
})

// Get Food QC Results
const results = await api.get('/v1/food/qc-results', {
  params: { page: 1, page_size: 10 }
})
```

### WebSocket Integration

```javascript
// Kết nối WebSocket
const ws = new WebSocket('ws://localhost:8080/ws/dashboard')

ws.onopen = () => {
  console.log('Connected to WebSocket')
}

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  console.log('Received:', data)
}

ws.onerror = (error) => {
  console.error('WebSocket Error:', error)
}
```

---

## 🎨 Development

### Project Structure

```
frontend/
├── src/
│   ├── views/              # Page components
│   │   ├── DashboardView.vue
│   │   ├── FoodQCView.vue
│   │   └── RTSPSetupView.vue
│   ├── components/         # Reusable components
│   │   ├── AppLayout.vue
│   │   ├── AppHeader.vue
│   │   ├── AppSidebar.vue
│   │   └── AppFooter.vue
│   ├── services/          # API & WebSocket services
│   │   ├── api.js         # Axios instance
│   │   └── websocket.js   # WebSocket manager
│   ├── router/             # Vue Router
│   └── App.vue
├── package.json
└── vite.config.js
```

### Tech Stack

- **Vue 3** - Framework
- **Vite** - Build tool
- **Vue Router** - Routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **HLS.js** - RTSP streaming

---

## 🐛 Troubleshooting

### Lỗi CORS

Kiểm tra Backend CORS configuration trong `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc thêm frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Lỗi 401 Unauthorized

1. Đăng nhập lại
2. Kiểm tra token còn hiệu lực
3. Xóa cookie và đăng nhập lại

### Lỗi WebSocket

Kiểm tra Backend đang chạy:
```bash
curl http://localhost:8080/health
```

### Port already in use

```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

---

## 📋 Tài Khoản Test

| Email | Password | Role |
|-------|----------|------|
| admin@cameraai.com | admin123 | admin |
| manager@cameraai.com | manager123 | manager |
| staff@cameraai.com | staff123 | staff |

---

## 📞 Hỗ Trợ

Nếu gặp lỗi:
1. Kiểm tra Backend đang chạy (port 8080)
2. Kiểm tra Docker containers đang chạy
3. Kiểm tra API URL trong `.env`
