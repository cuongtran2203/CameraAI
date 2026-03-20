import json
import os
import logging
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)

class KafkaPublisher:
    _instance = None
    _producer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._producer is None:
            self._connect()

    def _connect(self):
        try:
            from kafka import KafkaProducer
            bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
            self._producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
            )
            logger.info(f"Connected to Kafka at {bootstrap_servers}")
        except ImportError:
            logger.error("kafka-python is not installed.")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            self._producer = None

    def publish_food_detection(self, camera_id: str, food_item: str, result_status: str, similarity_score: float, details: dict):
        if not self._producer:
            logger.warning("Kafka producer not available, skipping message")
            return

        detection = {
            "food_item_id": "",
            "food_item": food_item,
            "result_status": result_status,
            "similarity_score": similarity_score,
            "color_match": details.get("color_match", True),
            "portion_match": details.get("portion_match", True),
            "topping_present": details.get("topping_present", True),
            "proof_image_url": details.get("proof_image_url", ""),
            "staff_id": "",
            "message_id": str(uuid4())
        }

        message = {
            "camera_id": camera_id,
            "timestamp": datetime.utcnow().isoformat(),
            "detections": [detection]
        }

        try:
            future = self._producer.send("ai.food.detections", key=camera_id, value=message)
            future.get(timeout=10)
            logger.info(f"Published food detection for {food_item} from {camera_id}")
        except Exception as e:
            logger.error(f"Failed to publish food detection: {e}")

publisher = KafkaPublisher()
