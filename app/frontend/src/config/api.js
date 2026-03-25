// Shared API configuration
// Uses Vite proxy in development, direct URL in production

const env = import.meta.env

// Determine if we're in development mode (using proxy)
const isDev = env.DEV

// API base URL
// In dev: uses Vite proxy (/api -> http://localhost:8080/api)
// In prod: use actual backend URL
export const API_BASE_URL = isDev ? '/api' : (env.VITE_API_URL || 'http://localhost:8080/api')

// WebSocket base URL
// In dev: uses Vite proxy (/ws -> ws://localhost:8080)
// In prod: use actual backend WebSocket
export const WS_BASE_URL = isDev ? '' : (env.VITE_API_URL?.replace(/\/api$/, '').replace(/^http/, 'ws') || 'ws://localhost:8080')

// Stream base URL (for video streaming)
export const STREAM_BASE_URL = isDev ? 'http://localhost:8080' : (env.VITE_API_URL?.replace('/api', '') || 'http://localhost:8080')

// MediaMTX URL (RTSP → HLS proxy)
export const MEDIAMTX_URL = isDev ? 'http://localhost:8888' : (env.VITE_MEDIAMTX_URL || 'http://localhost:8888')

// MediaMTX RTSP port
export const MEDIAMTX_RTSP_PORT = 8554
