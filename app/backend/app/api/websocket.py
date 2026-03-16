"""
WebSocket Handler - Real-time data streaming
"""
import json
import asyncio
import logging
from typing import Dict, Set
from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.models.models import Camera, User
from app.api.auth import get_current_user
from app.services.food_qc_service import (
    simulate_food_qc_updates,
    food_qc_manager,
    MockFoodQCDataGenerator
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["WebSocket"])


# =====================================================
# Connection Manager
# =====================================================

class ConnectionManager:
    """
    Manage WebSocket connections
    """

    def __init__(self):
        # All active connections
        self.active_connections: Set[WebSocket] = set()
        # Camera-specific connections
        self.camera_connections: Dict[str, Set[WebSocket]] = {}
        # Dashboard connections (receive all updates)
        self.dashboard_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket, channel: str = "dashboard"):
        """Accept and register new connection"""
        await websocket.accept()
        self.active_connections.add(websocket)

        if channel != "dashboard":
            if channel not in self.camera_connections:
                self.camera_connections[channel] = set()
            self.camera_connections[channel].add(websocket)
        else:
            self.dashboard_connections.add(websocket)

        logger.info(f"WebSocket connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket, channel: str = "dashboard"):
        """Remove connection"""
        self.active_connections.discard(websocket)

        if channel != "dashboard":
            if channel in self.camera_connections:
                self.camera_connections[channel].discard(websocket)
        else:
            self.dashboard_connections.discard(websocket)

        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def send_personal(self, message: dict, websocket: WebSocket):
        """Send message to specific client"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")

    async def broadcast(self, message: dict, channel: str = "dashboard"):
        """Broadcast message to channel"""
        if channel == "dashboard":
            connections = self.dashboard_connections
        else:
            connections = self.camera_connections.get(channel, set())

        # Also send to all dashboard connections
        for connection in list(self.dashboard_connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to dashboard: {e}")

        # Send to specific channel
        for connection in list(connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {channel}: {e}")

    async def broadcast_dashboard_update(self, data: dict):
        """Broadcast dashboard update to all dashboard connections"""
        message = {
            "type": "dashboard_update",
            "data": data,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.broadcast(message, "dashboard")

    async def broadcast_camera_update(self, camera_id: str, data: dict):
        """Broadcast camera update to specific camera channel"""
        message = {
            "type": "camera_update",
            "camera_id": camera_id,
            "data": data,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.broadcast(message, camera_id)


# Singleton instance
manager = ConnectionManager()


# =====================================================
# WebSocket Endpoints
# =====================================================

@router.websocket("/ws/dashboard")
async def websocket_dashboard(
    websocket: WebSocket,
    token: str = None
):
    """
    WebSocket endpoint for dashboard real-time updates
    Supports both:
    1. Token in query parameter: /ws/dashboard?token=xxx
    2. Token in cookie: auth_token=xxx (RECOMMENDED - more secure)
    """
    auth_token = None

    # Priority 1: Check cookie (more secure - not logged in URL)
    if websocket.cookies.get("auth_token"):
        auth_token = websocket.cookies.get("auth_token")
    # Priority 2: Check query parameter (for backward compatibility)
    elif token:
        auth_token = token

    # Validate token if provided
    if auth_token:
        try:
            from jose import jwt
            from app.db.database import settings
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if not user_id:
                await websocket.close(code=4001, reason="Invalid token")
                return
            logger.info(f"WebSocket authenticated for user: {user_id}")
        except Exception as e:
            logger.warning(f"WebSocket auth failed: {e}")
            # Allow connection for testing; in production, close it
            # await websocket.close(code=4001, reason="Invalid token")
            # return
    else:
        logger.warning("WebSocket connection without authentication")

    channel = "dashboard"
    await manager.connect(websocket, channel)

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "channel": channel,
            "message": "Connected to dashboard updates"
        })

        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=60)

                # Handle ping/pong
                if data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})

                # Handle subscription requests
                elif data.get("type") == "subscribe_camera":
                    camera_id = data.get("camera_id")
                    if camera_id:
                        pass  # Already subscribed via URL routing

                logger.debug(f"Received: {data}")

            except asyncio.TimeoutError:
                # Send keep-alive ping
                await websocket.send_json({"type": "ping"})
            except json.JSONDecodeError:
                logger.warning("Invalid JSON received")

    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, channel)


@router.websocket("/ws/camera/{camera_id}")
async def websocket_camera(
    websocket: WebSocket,
    camera_id: str,
    token: str = None
):
    """
    WebSocket endpoint for specific camera real-time updates
    """
    channel = camera_id
    await manager.connect(websocket, channel)

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "channel": channel,
            "message": f"Connected to camera {camera_id} updates"
        })

        # Keep connection alive
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=60)

                if data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})

            except asyncio.TimeoutError:
                await websocket.send_json({"type": "ping"})
            except json.JSONDecodeError:
                logger.warning("Invalid JSON received")

    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, channel)


# =====================================================
# Food QC WebSocket Endpoint
# =====================================================

@router.websocket("/ws/food-qc")
async def websocket_food_qc(websocket: WebSocket):
    """
    WebSocket endpoint for Food QC real-time updates
    Receives live QC results and statistics from AI/Kafka
    """
    await websocket.accept()
    food_qc_manager.add_subscriber(websocket, "food_qc")

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "channel": "food_qc",
            "message": "Connected to Food QC real-time updates"
        })

        # Send initial stats
        initial_stats = MockFoodQCDataGenerator.generate_live_stats()
        await websocket.send_json({
            "type": "food_qc_stats",
            "data": initial_stats,
            "timestamp": asyncio.get_event_loop().time()
        })

        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=60)

                # Handle ping/pong
                if data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})

                # Handle subscription to specific camera
                elif data.get("type") == "subscribe_camera":
                    camera_id = data.get("camera_id")
                    logger.info(f"Food QC client subscribed to camera: {camera_id}")

                # Handle request for historical data
                elif data.get("type") == "get_history":
                    # Generate some historical mock data
                    history = []
                    for i in range(10):
                        result = MockFoodQCDataGenerator.generate_qc_result()
                        history.append(result)
                    await websocket.send_json({
                        "type": "food_qc_history",
                        "data": history
                    })

                logger.debug(f"Received from Food QC client: {data}")

            except asyncio.TimeoutError:
                # Send keep-alive ping
                await websocket.send_json({"type": "ping"})
            except json.JSONDecodeError:
                logger.warning("Invalid JSON received from Food QC client")

    except WebSocketDisconnect:
        food_qc_manager.remove_subscriber(websocket, "food_qc")
        logger.info("Food QC WebSocket disconnected")
    except Exception as e:
        logger.error(f"Food QC WebSocket error: {e}")
        food_qc_manager.remove_subscriber(websocket, "food_qc")


# =====================================================
# Helper Functions (called by Kafka consumer)
# =====================================================

async def notify_dashboard_update(data: dict):
    """
    Send update to all dashboard connections
    Called from Kafka consumer when new data arrives
    """
    await manager.broadcast_dashboard_update(data)


async def notify_camera_update(camera_id: str, data: dict):
    """
    Send update to specific camera connections
    Called from Kafka consumer
    """
    await manager.broadcast_camera_update(camera_id, data)


# =====================================================
# AI Stream Simulation (15-minute intervals)
# =====================================================

async def simulate_ai_stream_updates(interval_seconds: int = 60):
    """
    Simulate AI streaming data every 15 minutes (configurable interval)
    Sends AI data to dashboard WebSocket connections

    For production: interval should be 900 (15 minutes)
    For testing: interval can be 60 seconds
    """
    import random
    from datetime import datetime, time, timedelta

    while True:
        try:
            now = datetime.utcnow()
            current_time = now.time()

            # Only generate data between 6 AM and 10 PM
            if time(6, 0) <= current_time <= time(22, 0):
                # Adjust activity based on time (lunch/dinner rush)
                if 11 <= current_time.hour <= 13:
                    activity_multiplier = 1.5
                elif 18 <= current_time.hour <= 20:
                    activity_multiplier = 1.8
                else:
                    activity_multiplier = 0.7

                # Generate AI data
                customer_entry = int(random.randint(3, 10) * activity_multiplier)
                customer_exit = int(random.randint(2, 8) * activity_multiplier)

                staff_activities = [
                    {"staff_id": f"staff-{i}", "staff_name": f"Staff {i}",
                     "action": random.choice(["cooking", "washing", "cleaning", "serving", "preparing"]),
                     "duration_min": random.randint(5, 15)}
                    for i in range(1, random.randint(4, 8))
                ]

                # HAR - Human Activity Recognition data with working time
                staff_har_data = []
                staff_names = ["Marco V.", "Sarah L.", "John D.", "Emily K.", "David L.", "Lisa M."]
                for i, activity in enumerate(staff_activities):
                    # Random work time between 30-120 minutes this shift
                    work_time = random.randint(30, 120)
                    # Calculate active percentage (70-98%)
                    active_pct = random.randint(70, 98)
                    staff_har_data.append({
                        "staff_id": activity["staff_id"],
                        "staff_name": staff_names[i] if i < len(staff_names) else f"Staff {i+1}",
                        "current_action": activity["action"],
                        "work_time_min": work_time,
                        "active_time_min": int(work_time * active_pct / 100),
                        "active_percentage": active_pct,
                        "status": "active" if active_pct > 60 else "idle"
                    })

                food_items_checked = random.randint(5, 15)
                qc_pass = int(food_items_checked * random.uniform(0.75, 0.95))
                qc_fail = food_items_checked - qc_pass
                qc_warnings = random.randint(0, 2)

                safety_alerts = []
                if random.random() < 0.15:
                    safety_alerts.append({
                        "type": random.choice(["no_helmet", "no_gloves", "foreign_object", "temperature_alert"]),
                        "severity": random.choice(["warning", "critical"]),
                        "location": random.choice(["kitchen_1", "kitchen_2", "grill_area"]),
                        "description": random.choice([
                            "Staff detected without safety helmet",
                            "Temperature exceeds safe threshold",
                            "Foreign object detected in food",
                            "Staff not wearing gloves"
                        ])
                    })

                equipment_status = [
                    {"equipment_id": f"eq-{i}",
                     "name": random.choice(["Oven", "Refrigerator", "Freezer", "Dishwasher", "Fryer"]),
                     "status": random.choice(["normal", "normal", "normal", "warning"]),
                     "temperature": random.randint(20, 180) if "Oven" in random.choice(["Oven", "Fryer"]) else random.randint(2, 8)}
                    for i in range(1, 6)
                ]

                ai_data = {
                    "timestamp": now.isoformat(),
                    "customers": {
                        "entry_count": customer_entry,
                        "exit_count": customer_exit,
                        "current_in_store": customer_entry - customer_exit,
                        "avg_dwell_time_min": random.randint(15, 45),
                        "peak_detection": random.choice([True, False]) if activity_multiplier > 1 else False
                    },
                    "staff": {
                        "active_count": len(staff_activities),
                        "activities": staff_activities,
                        "har_data": staff_har_data,  # Human Activity Recognition with work time
                        "productivity_score": random.randint(70, 95)
                    },
                    "food_qc": {
                        "items_checked": food_items_checked,
                        "passed": qc_pass,
                        "failed": qc_fail,
                        "warnings": qc_warnings,
                        "pass_rate": round(qc_pass / food_items_checked * 100, 1) if food_items_checked > 0 else 0
                    },
                    "safety": {
                        "alerts": safety_alerts,
                        "total_alerts": len(safety_alerts),
                        "critical_alerts": sum(1 for a in safety_alerts if a["severity"] == "critical")
                    },
                    "equipment": {
                        "items": equipment_status,
                        "warnings": sum(1 for e in equipment_status if e["status"] == "warning")
                    },
                    "summary": {
                        "overall_score": random.randint(75, 95),
                        "status": random.choice(["normal", "normal", "normal", "attention"]) if len(safety_alerts) == 0 else "attention",
                        "notes": "All systems operational" if len(safety_alerts) == 0 else f"{len(safety_alerts)} safety alert(s) require attention"
                    }
                }

                # Send AI stream data
                await manager.broadcast_dashboard_update({
                    "type": "ai_stream",
                    "data": ai_data
                })

                logger.info(f"AI stream data sent: {now.isoformat()}")

            # Wait for next interval (default 60 seconds for testing, use 900 for 15 minutes in production)
            await asyncio.sleep(interval_seconds)

        except Exception as e:
            logger.error(f"Error in simulate_ai_stream_updates: {e}")
            await asyncio.sleep(interval_seconds)


# =====================================================
# Background Task for Testing
# =====================================================

async def simulate_dashboard_updates():
    """
    Simulate dashboard updates for testing
    In production, this would be triggered by Kafka messages
    """
    import random
    from datetime import datetime

    while True:
        try:
            # Simulate data
            data = {
                "staff": {
                    "total_online": random.randint(5, 10),
                    "total_scheduled": 10,
                    "attendance_rate": round(random.uniform(0.7, 1.0), 2)
                },
                "actions": {
                    "productive_count": random.randint(20, 50),
                    "idle_count": random.randint(0, 5)
                },
                "food_qc": {
                    "total_checked": random.randint(30, 60),
                    "pass_rate": round(random.uniform(0.85, 0.98), 2)
                },
                "customers": {
                    "current_in_store": random.randint(10, 30),
                    "entry_today": random.randint(100, 200)
                }
            }

            await notify_dashboard_update(data)

            # Wait 5 seconds before next update
            await asyncio.sleep(5)

        except Exception as e:
            logger.error(f"Error in simulate_dashboard_updates: {e}")
            await asyncio.sleep(5)
