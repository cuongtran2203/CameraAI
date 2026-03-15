# AI Camera Event Processing System

## Overview

This project is an AI camera backend system built using **Python** and **FastAPI**.

The system receives **real-time detection events from AI cameras** (for example DeepStream pipelines) through **Kafka event streaming**.

The backend processes these events, stores operational and analytics data in **PostgreSQL**, and exposes APIs and real-time streams for frontend dashboards.

The architecture follows **Event-Driven Architecture** for scalability and real-time processing.

---

## Technology Stack

### Backend
- Python 3.10+
- FastAPI
- Uvicorn
- AsyncIO
- Pydantic

### Streaming
- Apache Kafka
- Kafka Consumer / Producer

### Database
- PostgreSQL
- SQLAlchemy or SQLModel
- Alembic for migrations

### AI Pipeline
- NVIDIA DeepStream
- AI Camera detection
- Object detection
- Face recognition
- Tracking events

### Realtime
- WebSocket
- REST API

### Optional
- Redis
- LangChain
- LangGraph
- Chroma / Vector DB
- OpenAI / LLM APIs

---

## System Architecture

The system processes AI camera events using Kafka and stores structured data in PostgreSQL.

Architecture flow:

AI Camera / DeepStream  
        ↓  
Detection JSON Event  
        ↓  
Kafka Topic  
        ↓  
FastAPI Kafka Consumer  
        ↓  
Event Processing Service  
        ↓  
PostgreSQL / Cache  
        ↓  
Frontend Dashboard API / WebSocket

---

## Main Responsibilities

The backend is responsible for:

- consuming AI camera events from Kafka
- validating and transforming event payloads
- storing event logs in PostgreSQL
- storing camera metadata and configuration
- generating analytics and summaries
- serving APIs for frontend dashboards
- pushing real-time updates via WebSocket

---

## Event Data Format

AI camera pipelines publish events in JSON format.

Example:

```json
{
  "camera_id": "cam_01",
  "timestamp": "2026-03-09T10:00:00",
  "event_type": "person_detected",
  "track_id": 12345,
  "objects": [
    {
      "id": 1,
      "label": "person",
      "confidence": 0.97,
      "bbox": [100, 200, 300, 500]
    }
  ]
}