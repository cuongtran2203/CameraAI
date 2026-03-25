"""
Kafka Producer & Consumer Services
Camera Analyst System
"""
import json
import asyncio
import logging
from datetime import datetime
from typing import Optional, Callable, Dict, Any
from uuid import uuid4

from kafka import KafkaProducer, KafkaConsumer

from app.db.database import settings

logger = logging.getLogger(__name__)


# =====================================================
# KAFKA TOPICS
# =====================================================

class KafkaTopics:
    """Kafka topic names"""
    # Commands - Frontend -> AI
    CAMERA_COMMANDS = "camera.commands"
    AI_CONFIG = "ai.config"

    # Results - AI -> Backend
    AI_FACE_DETECTIONS = "ai.face.detections"
    AI_ACTION_DETECTIONS = "ai.action.detections"
    AI_FOOD_DETECTIONS = "ai.food.detections"
    AI_CUSTOMER_DETECTIONS = "ai.customer.detections"

    # Aggregated
    AI_PROCESSED = "ai.processed"


# =====================================================
# KAFKA PRODUCER
# =====================================================

class KafkaProducerService:
    """
    Kafka Producer - Gửi message từ Backend -> AI
    """

    _instance: Optional['KafkaProducerService'] = None
    _producer: Optional[KafkaProducer] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._producer is None:
            self._connect()

    def _connect(self):
        """Connect to Kafka"""
        try:
            self._producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=1,
                compression_type='gzip'
            )
            logger.info(f"Kafka producer connected to {settings.KAFKA_BOOTSTRAP_SERVERS}")
        except Exception as e:
            logger.error(f"Failed to connect Kafka producer: {e}")
            self._producer = None

    async def send_command(
        self,
        camera_id: str,
        command: str,
        options: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Gửi command xuống AI

        Args:
            camera_id: ID của camera
            command: Lệnh (START_STREAM, STOP_STREAM, RESTART)
            options: Các tùy chọn bổ sung

        Returns:
            True nếu gửi thành công
        """
        message = {
            "message_id": str(uuid4()),
            "command": command,
            "camera_id": camera_id,
            "timestamp": datetime.utcnow().isoformat(),
            "options": options or {}
        }

        try:
            if self._producer:
                future = self._producer.send(
                    KafkaTopics.CAMERA_COMMANDS,
                    key=camera_id,
                    value=message
                )
                # Wait for send to complete
                future.get(timeout=10)
                logger.info(f"Sent command {command} for camera {camera_id}")
                return True
            else:
                logger.warning("Kafka producer not connected")
                return False
        except Exception as e:
            logger.error(f"Failed to send command: {e}")
            return False

    async def send_ai_config(
        self,
        camera_id: str,
        config: Dict[str, Any]
    ) -> bool:
        """Gửi AI config cho camera"""
        message = {
            "camera_id": camera_id,
            "config": config,
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            if self._producer:
                future = self._producer.send(
                    KafkaTopics.AI_CONFIG,
                    key=camera_id,
                    value=message
                )
                future.get(timeout=10)
                logger.info(f"Sent AI config for camera {camera_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to send AI config: {e}")
            return False

    def close(self):
        """Close producer"""
        if self._producer:
            self._producer.close()
            self._producer = None


# =====================================================
# KAFKA CONSUMER
# =====================================================

class KafkaConsumerService:
    """
    Kafka Consumer - Nhận message từ AI -> Backend
    """

    def __init__(self):
        self._consumers: Dict[str, KafkaConsumer] = {}
        self._running = False

    def _create_consumer(self, topic: str, group_id: str = "backend-consumer") -> KafkaConsumer:
        """Create a Kafka consumer for a topic"""
        return KafkaConsumer(
            topic,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            group_id=group_id,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            consumer_timeout_ms=1000
        )

    async def start_consuming(
        self,
        handlers: Dict[str, Callable[[Dict], Any]]
    ):
        """
        Start consuming messages từ multiple topics

        Args:
            handlers: Dict mapping topic -> handler function
        """
        self._running = True
        tasks = []

        for topic, handler in handlers.items():
            consumer = self._create_consumer(topic)
            self._consumers[topic] = consumer
            task = asyncio.create_task(self._consume_loop(topic, consumer, handler))
            tasks.append(task)

        logger.info(f"Started consuming topics: {list(handlers.keys())}")

        # Wait for all tasks
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _consume_loop(
        self,
        topic: str,
        consumer: KafkaConsumer,
        handler: Callable[[Dict], Any]
    ):
        """Consume loop for a single topic"""
        while self._running:
            try:
                for message in consumer:
                    if not self._running:
                        break
                    try:
                        await handler(message.value)
                    except Exception as e:
                        logger.error(f"Error handling message from {topic}: {e}")
            except Exception as e:
                logger.error(f"Consumer error for {topic}: {e}")
                await asyncio.sleep(1)

    def stop(self):
        """Stop all consumers"""
        self._running = False
        for consumer in self._consumers.values():
            consumer.close()
        self._consumers.clear()
        logger.info("Kafka consumers stopped")


# =====================================================
# HANDLER FUNCTIONS
# =====================================================

async def handle_face_detection(message: Dict):
    """Handle face detection message from AI"""
    # TODO: Save to database
    # - Parse message
    # - Find or create staff_face record
    # - Create attendance record if check-in/check-out
    logger.info(f"Face detection: {message.get('camera_id')}")


async def handle_action_detection(message: Dict):
    """Handle action detection message from AI"""
    # TODO: Save to database
    # - Parse actions
    # - Create staff_action records
    # - Update daily_staff_performance
    logger.info(f"Action detection: {message.get('camera_id')}")


async def handle_food_detection(message: Dict):
    """
    Handle food detection message from AI
    1. Parse food detections from Kafka message
    2. Save to food_qc_results table in database
    3. Broadcast via WebSocket for real-time frontend updates
    """
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import text
        from app.db.database import settings
        from app.models.models import FoodQCResult, FoodItem
        from app.services.food_qc_service import food_qc_manager
        from datetime import datetime

        # Get detections from message
        detections = message.get('detections', [])
        timestamp = message.get('timestamp', datetime.utcnow().isoformat())
        camera_id = message.get('camera_id')

        if not detections:
            logger.warning("No detections in food QC message")
            return

        # Create async engine for this async operation
        engine = create_async_engine(settings.DATABASE_URL, echo=False)
        AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with AsyncSessionLocal() as session:
            for detection in detections:
                # Get food_item_id - try to find by name or use provided ID
                food_item_id = detection.get('food_item_id')
                food_item_name = detection.get('food_item', 'Unknown')

                # If no food_item_id, try to find food item by name
                if not food_item_id and food_item_name:
                    result = await session.execute(
                        text("SELECT id FROM food_items WHERE name ILIKE :name LIMIT 1"),
                        {"name": f"%{food_item_name}%"}
                    )
                    food_item = result.fetchone()
                    if food_item:
                        food_item_id = food_item[0]

                # Use first food item if still not found (for demo)
                if not food_item_id:
                    result = await session.execute(text("SELECT id FROM food_items LIMIT 1"))
                    food_item = result.fetchone()
                    if food_item:
                        food_item_id = food_item[0]
                    else:
                        logger.warning("No food items found in database, skipping")
                        continue

                # Parse result status
                result_status = detection.get('result_status', 'pass')
                # Normalize status
                if result_status in ['passed', 'pass']:
                    result_status = 'pass'
                elif result_status in ['failed', 'fail']:
                    result_status = 'fail'
                elif result_status == 'warning':
                    result_status = 'warning'

                # Parse similarity score
                similarity_score = detection.get('similarity_score', 0)
                if isinstance(similarity_score, str):
                    # If it's a percentage string like "85%", convert to decimal
                    similarity_score = float(similarity_score.replace('%', '')) / 100
                elif similarity_score > 1:
                    # If it's already a percentage (e.g., 85), convert to decimal
                    similarity_score = similarity_score / 100

                # Parse timestamp
                if isinstance(timestamp, str):
                    checked_at = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    checked_at = datetime.utcnow()

                # Create QC result record
                qc_result = FoodQCResult(
                    id=str(uuid4()),
                    camera_id=camera_id,
                    food_item_id=food_item_id,
                    result_status=result_status,
                    similarity_score=similarity_score,
                    color_match=detection.get('color_match'),
                    portion_match=detection.get('portion_match'),
                    topping_present=detection.get('topping_present'),
                    proof_image_url=detection.get('proof_image_url'),
                    staff_id=detection.get('staff_id'),
                    checked_by='ai',
                    checked_at=checked_at,
                    created_at=datetime.utcnow()
                )

                session.add(qc_result)

                # Prepare WebSocket broadcast data
                ws_data = {
                    'message_id': detection.get('message_id', str(uuid4())),
                    'timestamp': checked_at.isoformat(),
                    'camera_id': camera_id,
                    'food_item': food_item_name,
                    'food_item_id': food_item_id,
                    'result_status': result_status,
                    'similarity_score': similarity_score,
                    'confidence': detection.get('confidence', 0.95),
                    'color_match': detection.get('color_match'),
                    'portion_match': detection.get('portion_match'),
                    'topping_present': detection.get('topping_present'),
                    'proof_image_url': detection.get('proof_image_url'),
                }

                # Commit this record
                await session.commit()

                # Broadcast via WebSocket
                await food_qc_manager.broadcast_qc_result(ws_data)
                logger.info(f"Food QC saved and broadcasted: {food_item_name} - {result_status}")

        await engine.dispose()

    except Exception as e:
        import traceback
        logger.error(f"Error handling food detection: {e}")
        logger.error(traceback.format_exc())


async def handle_human_detection(message: Dict):
    """
    Handle human/customer detection message from DeepStream
    1. Parse detection events from Kafka message
    2. Log the detection (extend to save to DB / broadcast via WebSocket as needed)
    """
    try:
        camera_id = message.get('camera_id')
        humans = message.get('humans', [])
        timestamp = message.get('timestamp')

        logger.info(
            f"Human detection: camera={camera_id}, "
            f"count={len(humans)}, time={timestamp}"
        )

        # TODO: Save to database, update customer_event records,
        #       update hourly/daily stats, broadcast via WebSocket, etc.

    except Exception as e:
        import traceback
        logger.error(f"Error handling human detection: {e}")
        logger.error(traceback.format_exc())


async def handle_customer_detection(message: Dict):
    """Handle customer detection message from AI"""
    # TODO: Save to database
    # - Parse customer events
    # - Create customer_event records
    # - Update hourly/daily stats
    logger.info(f"Customer detection: {message.get('camera_id')}")


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_producer() -> KafkaProducerService:
    """Get Kafka producer singleton"""
    return KafkaProducerService()


async def send_camera_command(camera_id: str, command: str) -> bool:
    """Helper to send camera command"""
    producer = get_producer()
    return await producer.send_command(camera_id, command)


async def send_ai_config(camera_id: str, config: Dict) -> bool:
    """Helper to send AI config"""
    producer = get_producer()
    return await producer.send_ai_config(camera_id, config)
