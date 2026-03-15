# Camera AI Frontend - Hướng Dẫn Cài Đặt

## Yêu Cầu Môi Trường

### 1. Node.js
- **Node.js 18+** (khuyến nghị: Node.js 20)

Kiểm tra phiên bản Node:
```bash
node --version
```

### 2. npm
- **npm 9+** (đi kèm Node.js)

Kiểm tra phiên bản npm:
```bash
npm --version
```

---

## Cài Đặt

### 1. Cài Đặt Dependencies

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/frontend
npm install
```

### 2. Cấu Hình Môi Trường

Tạo file `.env` trong thư mục `app/frontend/`:

```env
VITE_API_URL=http://localhost:8080/api
```

---

## Chạy Ứng Dụng

### Development Mode

```bash
cd /Users/ngohongnguyen/Documents/works/CameraAI/app/frontend
npm run dev
```

Ứng dụng sẽ chạy tại: **http://localhost:5173**

### Production Build

```bash
npm run build
```

Build output sẽ nằm trong thư mục `dist/`

### Preview Production Build

```bash
npm run preview
```

---

## Các Lệnh npm

| Lệnh | Mô Tả |
|-------|--------|
| `npm run dev` | Chạy development server |
| `npm run build` | Build cho production |
| `npm run preview` | Preview production build |

---

## Cấu Trúc Project

```
app/frontend/
├── src/
│   ├── components/      # Vue components
│   │   ├── AppLayout.vue
│   │   ├── AppHeader.vue
│   │   ├── AppSidebar.vue
│   │   └── AppFooter.vue
│   ├── views/          # Page views
│   │   ├── DashboardView.vue
│   │   ├── LiveView.vue
│   │   └── ...
│   ├── composables/    # Vue composables
│   │   └── useAuth.js
│   ├── services/      # API services
│   │   └── ApiService.js
│   ├── router/        # Vue Router
│   │   └── index.js
│   ├── main.js        # Entry point
│   └── style.css      # Global styles
├── public/            # Static assets
├── index.html         # HTML entry
├── package.json
├── vite.config.js     # Vite config
├── tailwind.config.js # Tailwind config
└── postcss.config.js  # PostCSS config
```

---

## Công Nghệ Sử Dụng

### Dependencies
- **vue** ^3.5.25 - Vue.js 3
- **vue-router** ^5.0.3 - Vue Router

### DevDependencies
- **vite** ^7.3.1 - Build tool
- **@vitejs/plugin-vue** ^6.0.2 - Vue plugin for Vite
- **tailwindcss** ^3.4.0 - CSS framework
- **postcss** - CSS post-processor
- **autoprefixer** - Vendor prefixer

---

## Kết Nối API

Frontend kết nối với backend tại:
- **API URL**: http://localhost:8080/api
- **API Docs**: http://localhost:8080/docs

---

## Các Lỗi Thường Gặp

### 1. "command not found: npm"
- Cài đặt Node.js: https://nodejs.org/

### 2. "port already in use"
- Kill process đang chạy trên port 5173:
  ```bash
  lsof -ti:5173 | xargs kill -9
  ```
- Hoặc đổi port trong vite.config.js

### 3. Lỗi Tailwind CSS
- Đảm bảo đã cài đặt:
  ```bash
  npm install -D tailwindcss@3 postcss autoprefixer
  ```

---

## Tài Khoản Test

| Field | Value |
|-------|-------|
| Email | admin@test.com |
| Password | admin123 |

---

## Liên Hệ

Nếu gặp vấn đề khác, vui lòng kiểm tra log hoặc liên hệ team phát triển.
