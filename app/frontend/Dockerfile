# =====================================================
# CameraAI — Frontend (Vue 3 + Vite)
# =====================================================

# ── Stage 1: Build ────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy source
COPY . .

# Build argument for API URL (defaults for Docker, override at runtime)
ARG VITE_API_URL=http://localhost:8080/api
ARG VITE_WS_URL=ws://localhost:8080
ARG VITE_AI_SERVICE_URL=http://localhost:8000

ENV VITE_API_URL=${VITE_API_URL}
ENV VITE_WS_URL=${VITE_WS_URL}
ENV VITE_AI_SERVICE_URL=${VITE_AI_SERVICE_URL}

RUN npm run build

# ── Stage 2: Serve with Nginx ─────────────────────────
FROM nginx:alpine

# Remove default nginx site
RUN rm -rf /usr/share/nginx/html/*

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
