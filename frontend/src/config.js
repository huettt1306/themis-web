// src/config.js

// === Cấu hình backend ===
export const BACKEND_HOST = "http://localhost"
export const BACKEND_PORT = 8000

// URL gốc backend
export const BACKEND_URL = `${BACKEND_HOST}:${BACKEND_PORT}`

// === Đường dẫn API ===
export const API = {
  LOGIN: `${BACKEND_URL}/login`,
  PROBLEMS: `${BACKEND_URL}/problems`,
  SUBMIT: `${BACKEND_URL}/submit`,
  RESULT: `${BACKEND_URL}/submit/result`
}

// === Tùy chọn khác ===
export const POLL_INTERVAL = 2000      // ms giữa mỗi lần kiểm tra log
export const POLL_RETRY = 60           // số lần kiểm tra tối đa
