# Frontend Vue 3 Dashboard Development

## Overview

This project uses **Vue 3** for frontend development.

The frontend is built for real-time dashboard and monitoring features, consuming data from backend APIs and listening to real-time updates through **WebSocket**.

The application should be built with:

- Vue 3
- vue-router
- Pinia
- WebSocket
- clean HTML structure
- readable and maintainable CSS classes
- ESLint-friendly code style

The goal is to create a frontend that is:

- responsive
- clean
- scalable
- easy to maintain
- optimized for real-time updates
- smooth and not laggy when listening to WebSocket events

---

## Technology Stack

- Vue 3
- vue-router
- Pinia
- JavaScript or TypeScript
- WebSocket
- REST API integration
- ESLint
- Optional: Tailwind CSS

---

## Main Responsibilities

The frontend is responsible for:

- rendering dashboard UI
- connecting to backend REST APIs
- listening to real-time updates via WebSocket
- updating UI efficiently without unnecessary re-renders
- managing application state with Pinia
- handling route-based pages with vue-router
- displaying data with clean and accessible HTML

---

## Project Structure

Typical frontend structure:

```text
src/
├── api/
│   ├── camera.js
│   └── analytics.js
├── assets/
├── components/
│   ├── common/
│   ├── dashboard/
│   └── camera/
├── composables/
│   └── useWebSocket.js
├── layouts/
│   └── DefaultLayout.vue
├── router/
│   └── index.js
├── stores/
│   ├── camera.js
│   ├── analytics.js
│   └── websocket.js
├── views/
│   ├── DashboardView.vue
│   ├── CameraDetailView.vue
│   └── AlertsView.vue
├── App.vue
└── main.js