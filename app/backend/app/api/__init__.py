# API Routes package
from app.api.auth import router as auth_router
from app.api.cameras import router as cameras_router
from app.api.staff import router as staff_router
from app.api.dashboard import router as dashboard_router
from app.api.food import router as food_router
from app.api.websocket import router as websocket_router
from app.api.system import router as system_router

__all__ = [
    "auth_router",
    "cameras_router",
    "staff_router",
    "dashboard_router",
    "food_router",
    "websocket_router",
    "system_router",
]
