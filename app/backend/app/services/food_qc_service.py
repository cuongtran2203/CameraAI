"""
Mock Kafka Service for Food QC - Simulates AI Food Detection Data
This service generates mock food QC data that would normally come from Kafka
"""
import json
import asyncio
import logging
import random
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4

logger = logging.getLogger(__name__)


# =====================================================
# MOCK FOOD QC DATA GENERATORS
# =====================================================

class MockFoodQCDataGenerator:
    """Generate mock Food QC data similar to what AI would send via Kafka"""

    # Food categories and items for realistic mock data
    FOOD_ITEMS = [
        {"name": "Phở Bò", "category": "main", "base_score": 0.95},
        {"name": "Bún Chả", "category": "main", "base_score": 0.93},
        {"name": "Cơm Rang", "category": "main", "base_score": 0.91},
        {"name": "Mì Xào", "category": "main", "base_score": 0.90},
        {"name": "Gỏi Cuốn", "category": "appetizer", "base_score": 0.94},
        {"name": "Nem Nướng", "category": "appetizer", "base_score": 0.92},
        {"name": "Chả Giò", "category": "appetizer", "base_score": 0.89},
        {"name": "Trà Đá", "category": "drink", "base_score": 0.98},
    ]

    DEFECT_TYPES = [
        "color_mismatch",
        "portion_small",
        "missing_topping",
        "shape_deformed",
        "temperature_low",
        "temperature_high",
        "foreign_object",
        "packaging_damaged",
    ]

    CAMERA_NODES = ["NODE-01", "NODE-02", "NODE-03", "NODE-04", "NODE-05"]
    PRODUCTION_LINES = ["Line A", "Line B", "Line C"]
    BATCH_PREFIXES = ["A-", "B-", "C-"]

    @classmethod
    def generate_qc_result(cls, camera_id: str = "NODE-04") -> Dict[str, Any]:
        """Generate a single QC result similar to AI detection"""

        # Select random food item
        food_item = random.choice(cls.FOOD_ITEMS)

        # Generate similarity score with some variation
        base_score = food_item["base_score"]
        similarity_score = round(base_score + random.uniform(-0.08, 0.05), 3)

        # Determine status based on score: >= 90% = pass, < 90% = fail
        if similarity_score >= 0.90:
            status = "pass"
        else:
            status = "fail"

        # Generate specific defect if failed
        defects = []
        if status == "fail":
            defects = random.sample(cls.DEFECT_TYPES[:6], k=random.randint(1, 2))

        # Generate detailed analysis - simplified based on pass/fail
        if status == "pass":
            analysis = {
                "color_match": random.uniform(0.90, 0.99),
                "texture_match": random.uniform(0.90, 0.99),
                "portion_ratio": random.uniform(0.95, 1.05),
                "topping_coverage": random.uniform(0.90, 1.0),
            }
        else:
            # Failed - scores below 90%
            analysis = {
                "color_match": random.uniform(0.60, 0.89),
                "texture_match": random.uniform(0.65, 0.89),
                "portion_ratio": random.uniform(0.75, 0.89),
                "topping_coverage": random.uniform(0.60, 0.89),
            }

        # Generate timestamp with slight variation
        timestamp = datetime.utcnow()

        # Generate batch ID
        batch_num = random.randint(100, 999)
        batch_prefix = random.choice(cls.BATCH_PREFIXES)
        batch_id = f"{batch_prefix}{batch_num}-{timestamp.strftime('%H%M')}"

        result = {
            "message_id": str(uuid4()),
            "timestamp": timestamp.isoformat(),
            "camera_id": camera_id,
            "production_line": random.choice(cls.PRODUCTION_LINES),
            "batch_id": batch_id,

            # Food info
            "food_item": food_item["name"],
            "food_category": food_item["category"],

            # QC Result
            "result_status": status,
            "similarity_score": similarity_score,
            "confidence": round(random.uniform(0.92, 0.999), 3),

            # Detailed analysis
            "analysis": analysis,
            "defects": defects,

            # Additional metrics
            "color_score": round(analysis["color_match"] * 100, 1),
            "texture_score": round(analysis["texture_match"] * 100, 1),
            "portion_score": round(analysis["portion_ratio"] * 100, 1),
            "topping_score": round(analysis["topping_coverage"] * 100, 1),

            # Environmental data (simulated sensor data)
            "environmental": {
                "surface_temp": round(random.uniform(65.0, 75.0), 1),
                "ambient_temp": round(random.uniform(22.0, 28.0), 1),
                "humidity": round(random.uniform(45.0, 65.0), 1),
            },

            # Image URLs (mock URLs)
            "proof_image_url": f"/api/v1/images/proof/{uuid4().hex[:8]}.jpg",
            "comparison_image_url": f"/api/v1/images/comparison/{uuid4().hex[:8]}.jpg",

            # AI Model info
            "ai_model": {
                "name": "food-qc-v2.1",
                "version": "2.1.5",
                "inference_time_ms": random.randint(45, 120),
            }
        }

        return result

    @classmethod
    def generate_batch_results(cls, count: int = 5, camera_id: str = "NODE-04") -> Dict[str, Any]:
        """Generate a batch of QC results"""

        results = [cls.generate_qc_result(camera_id) for _ in range(count)]

        # Calculate summary
        passed = sum(1 for r in results if r["result_status"] == "pass")
        warnings = sum(1 for r in results if r["result_status"] == "warning")
        failed = sum(1 for r in results if r["result_status"] == "fail")

        avg_score = sum(r["similarity_score"] for r in results) / len(results)

        return {
            "message_type": "food_qc_batch",
            "timestamp": datetime.utcnow().isoformat(),
            "camera_id": camera_id,
            "results": results,
            "summary": {
                "total_checked": count,
                "passed": passed,
                "warning": warnings,
                "failed": failed,
                "pass_rate": round(passed / count * 100, 1),
                "average_similarity_score": round(avg_score, 3),
            }
        }

    @classmethod
    def generate_live_stats(cls, camera_id: str = "NODE-04") -> Dict[str, Any]:
        """Generate live statistics for the dashboard"""

        return {
            "message_type": "food_qc_stats",
            "timestamp": datetime.utcnow().isoformat(),
            "camera_id": camera_id,
            "stats": {
                "items_checked_today": random.randint(150, 300),
                "passed_today": random.randint(130, 270),
                "failed_today": random.randint(2, 15),
                "warning_today": random.randint(5, 25),
                "pass_rate_today": round(random.uniform(0.88, 0.97), 2),
                "current_session": {
                    "items_checked": random.randint(10, 30),
                    "passed": random.randint(8, 27),
                    "failed": random.randint(0, 3),
                    "pass_rate": round(random.uniform(0.85, 0.98), 2),
                },
                "avg_check_time_seconds": round(random.uniform(2.5, 5.5), 1),
            },
            "thresholds": {
                "pass": 90,
                "optimal": 95,
            }
        }


# =====================================================
# FOOD QC WEBSOCKET MANAGER
# =====================================================

class FoodQCWebSocketManager:
    """
    Manages WebSocket connections for Food QC real-time updates
    This is a simplified version that works with the existing ConnectionManager
    """

    def __init__(self):
        self._subscribers: Dict[str, set] = {
            "food_qc": set(),
            "food_qc_stats": set(),
        }
        self._latest_data: Dict[str, Any] = {}

    def add_subscriber(self, websocket, channel: str = "food_qc"):
        """Add a WebSocket subscriber"""
        if channel not in self._subscribers:
            self._subscribers[channel] = set()
        self._subscribers[channel].add(websocket)
        logger.info(f"Food QC subscriber added. Total: {len(self._subscribers[channel])}")

    def remove_subscriber(self, websocket, channel: str = "food_qc"):
        """Remove a WebSocket subscriber"""
        if channel in self._subscribers:
            self._subscribers[channel].discard(websocket)
            logger.info(f"Food QC subscriber removed. Total: {len(self._subscribers[channel])}")

    async def broadcast_qc_result(self, data: Dict[str, Any]):
        """Broadcast a QC result to all subscribers"""
        message = {
            "type": "food_qc_result",
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._latest_data["food_qc"] = message
        logger.info(f"Broadcasting QC result: {data.get('food_item')} - {data.get('result_status')}")

        # Send to food_qc channel subscribers (direct)
        subscribers = self._subscribers.get("food_qc", set())
        logger.info(f"Food QC subscribers count: {len(subscribers)}")
        for ws in list(subscribers):
            try:
                await ws.send_json(message)
                logger.debug("Sent to food_qc subscriber")
            except Exception as e:
                logger.error(f"Error sending to food_qc subscriber: {e}")
                self._subscribers["food_qc"].discard(ws)

        # Also broadcast to dashboard for general listeners
        from app.api.websocket import manager
        await manager.broadcast(message, "dashboard")

    async def broadcast_stats(self, data: Dict[str, Any]):
        """Broadcast statistics to all subscribers"""
        message = {
            "type": "food_qc_stats",
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._latest_data["food_qc_stats"] = message

        # Send to food_qc channel subscribers (direct)
        for ws in list(self._subscribers.get("food_qc", set())):
            try:
                await ws.send_json(message)
            except Exception as e:
                logger.error(f"Error sending stats to food_qc subscriber: {e}")
                self._subscribers["food_qc"].discard(ws)

        # Also broadcast to dashboard
        from app.api.websocket import manager
        await manager.broadcast(message, "dashboard")

    def get_latest_data(self, channel: str = "food_qc") -> Optional[Dict[str, Any]]:
        """Get the latest data for a channel"""
        return self._latest_data.get(channel)


# Singleton instance
food_qc_manager = FoodQCWebSocketManager()


# =====================================================
# SIMULATION LOOP
# =====================================================

async def simulate_food_qc_updates(interval_seconds: int = 3):
    """
    Simulate Food QC data streaming (like Kafka would send)
    Runs continuously and sends updates to WebSocket connections
    """
    logger.info(f"Starting Food QC simulation (interval: {interval_seconds}s)")
    logger.info(f"Food QC Manager subscribers: {len(food_qc_manager._subscribers.get('food_qc', set()))}")

    while True:
        try:
            # Generate random QC result
            camera_id = random.choice(MockFoodQCDataGenerator.CAMERA_NODES)

            # Randomly decide between single result or stats update
            if random.random() < 0.7:
                # Send single QC result
                qc_data = MockFoodQCDataGenerator.generate_qc_result(camera_id)
                await food_qc_manager.broadcast_qc_result(qc_data)
                logger.debug(f"Food QC result sent: {qc_data['food_item']} - {qc_data['result_status']}")
            else:
                # Send stats update
                stats_data = MockFoodQCDataGenerator.generate_live_stats(camera_id)
                await food_qc_manager.broadcast_stats(stats_data)
                logger.debug(f"Food QC stats sent: pass rate {stats_data['stats']['pass_rate_today']}")

            # Wait for next interval
            await asyncio.sleep(interval_seconds)

        except Exception as e:
            logger.error(f"Error in simulate_food_qc_updates: {e}")
            await asyncio.sleep(interval_seconds)


# =====================================================
# HANDLER FUNCTIONS (for future Kafka integration)
# =====================================================

async def handle_food_qc_message(message: Dict[str, Any]):
    """
    Handle incoming Food QC message from Kafka
    This will be used when real Kafka integration is ready
    """
    message_type = message.get("message_type", "food_qc_result")

    if message_type == "food_qc_result":
        await food_qc_manager.broadcast_qc_result(message)
    elif message_type == "food_qc_batch":
        # Handle batch results
        for result in message.get("results", []):
            await food_qc_manager.broadcast_qc_result(result)
    elif message_type == "food_qc_stats":
        await food_qc_manager.broadcast_stats(message)

    logger.info(f"Processed Food QC message: {message_type}")
