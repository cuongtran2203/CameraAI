# =====================================================
# Docker Compose - Camera AI Backend Services
# =====================================================
#
# Services included:
# - Zookeeper (required for Kafka)
# - Kafka (message broker)
# - Kafka UI (manage Kafka topics)
# - PostgreSQL (database)
# - Redis (caching)
#
# =====================================================

# 1. Start all services
docker compose up -d

# 2. Check services status
docker compose ps

# 3. View logs
docker compose logs -f

# 4. Stop all services
docker compose down

# =====================================================
# Kafka Topics
# =====================================================

# Create topic for tracking (after Kafka starts)
docker exec -it kafka kafka-topics \
  --create \
  --topic ai.tracking \
  --bootstrap-server localhost:29092 \
  --partitions 1 \
  --replication-factor 1

# List all topics
docker exec -it kafka kafka-topics \
  --list \
  --bootstrap-server localhost:29092

# =====================================================
# Environment Variables
# =====================================================

# Update .env file with:
# DATABASE_URL=postgresql+asyncpg://ngohongnguyen:postgres@postgres:5432/camera_analyst
# KAFKA_BOOTSTRAP_SERVERS=localhost:29092
# REDIS_URL=redis://redis:6379
