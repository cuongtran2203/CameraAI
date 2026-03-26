"""
Camera Analyst API - Main Application Entry Point
FastAPI Backend
"""
import logging
import asyncio
from contextlib import asynccontextmanager

# Load .env file automatically on startup
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
from app.api import (
    auth_router,
    cameras_router,
    staff_router,
    dashboard_router,
    food_router,
    websocket_router,
    system_router,
)
from app.api.websocket import simulate_ai_stream_updates
from app.services.kafka_service import (
    KafkaConsumerService,
    handle_face_detection,
    handle_action_detection,
    handle_food_detection,
    handle_customer_detection,
    handle_human_detection,
    KafkaTopics
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# =====================================================
# Database Setup
# =====================================================

async def init_db():
    """Initialize database tables"""
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")


async def drop_db():
    """Drop all database tables (for development)"""
    logger.warning("Dropping all database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.warning("Database tables dropped")


# =====================================================
# Kafka Setup
# =====================================================

kafka_consumer = None


async def start_kafka_consumer():
    """Start Kafka consumer for AI messages"""
    global kafka_consumer

    logger.info("Starting Kafka consumer...")

    kafka_consumer = KafkaConsumerService()

    # Define handlers for each topic
    handlers = {
        KafkaTopics.AI_FACE_DETECTIONS: handle_face_detection,
        KafkaTopics.AI_ACTION_DETECTIONS: handle_action_detection,
        KafkaTopics.AI_FOOD_DETECTIONS: handle_food_detection,
        KafkaTopics.AI_CUSTOMER_DETECTIONS: handle_customer_detection,
    }

    # Start consuming in background
    # Note: In production, this should be started as a separate task
    # await kafka_consumer.start_consuming(handlers)

    logger.info("Kafka consumer ready (consuming disabled for now)")


def stop_kafka_consumer():
    """Stop Kafka consumer"""
    global kafka_consumer
    if kafka_consumer:
        kafka_consumer.stop()
        logger.info("Kafka consumer stopped")


# =====================================================
# Application Lifespan
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan - startup and shutdown events
    """
    # Startup
    logger.info("Starting Camera Analyst API...")
    logger.info(f"Database URL: {engine.url}")

    # Initialize database
    await init_db()

    # Start Kafka consumer
    await start_kafka_consumer()

    # Start AI stream simulation (60 seconds for testing, use 900 for 15 minutes in production)
    asyncio.create_task(simulate_ai_stream_updates(interval_seconds=60))  # 1 minute for testing

    # Start Food QC simulation (disabled — now handled via /food/search endpoint)
    # asyncio.create_task(simulate_food_qc_updates(interval_seconds=3))

    logger.info("Camera Analyst API started successfully!")

    yield

    # Shutdown
    logger.info("Shutting down Camera Analyst API...")

    # Stop Kafka consumer
    stop_kafka_consumer()

    # Close database connections
    await engine.dispose()

    logger.info("Camera Analyst API shutdown complete!")


# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title="Camera Analyst API",
    description="AI-Powered F&B Management System API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Include Routers
# =====================================================

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "camera-analyst-api",
        "version": "1.0.0"
    }


# API v1 routes
app.include_router(auth_router, prefix="/api/v1")
app.include_router(cameras_router, prefix="/api/v1")
app.include_router(staff_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(food_router, prefix="/api/v1")
app.include_router(system_router, prefix="/api/v1")

# WebSocket routes (no /api/v1 prefix)
app.include_router(websocket_router)


# =====================================================
# Root endpoint
# =====================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Camera Analyst API",
        "docs": "/docs",
        "version": "1.0.0"
    }


# =====================================================
# Development endpoints
# =====================================================

@app.post("/dev/reset-db")
async def reset_database():
    """
    Reset database (development only!)
    """
    logger.warning("Received database reset request")
    await drop_db()
    await init_db()
    return {"message": "Database reset complete"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
