# =====================================================
# Docker Compose - Camera AI Backend Services
# =====================================================
#
# Services included:
# - Zookeeper (required for Kafka)
# - Kafka (message broker)
# - Kafka UI (manage Kafka topics) - http://localhost:8082
# - PostgreSQL (database)
# - Redis (caching)
#
# =====================================================

# 1. Prerequisites
# ---------------
# - Install Docker Desktop: https://www.docker.com/products/docker-desktop/
# - Make sure Docker Desktop is running (check icon in menu bar)
# - If `docker` command not found, add to PATH:
#   echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc
#   source ~/.zshrc

# 2. Start all services
# ---------------------
docker compose up -d

# 3. Check services status
docker compose ps

# 4. View logs
docker compose logs -f

# 5. Stop all services
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

# =====================================================
# Service URLs
# =====================================================
# Kafka UI:     http://localhost:8082
# PostgreSQL:   localhost:5432
# Redis:        localhost:6379
# Kafka:        localhost:29092

# =====================================================
# Troubleshooting
# =====================================================
#
# If docker command not found:
#   - Ensure Docker Desktop is running
#   - Add to PATH: export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
#
# If containers fail to start:
#   - Check Docker Desktop logs: docker compose logs [service-name]
#   - Restart Docker Desktop
#
# If port already in use:
#   - Stop other services using the same port
#   - Or update port mappings in docker-compose.yml
