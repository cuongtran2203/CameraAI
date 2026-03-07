# DeepStream to Kafka to Web Dashboard Example

This example demonstrates how to export real-time detection metadata from DeepStream to a Kafka topic, and then consume that data in a Python web application to display on a live dashboard.

## Architecture

1.  **DeepStream Pipeline**: Runs inference (YOLO/ResNet) and uses a custom probe to extract metadata (bounding boxes, labels).
2.  **Kafka Producer**: Sends JSON-formatted detection data to a Kafka topic (`camera-detections`).
3.  **Kafka Broker**: Message queue managing the data stream.
4.  **Web Server (Consumer)**: A Flask + Socket.IO server that consumes messages from Kafka and pushes them to connected web clients.
5.  **Frontend**: HTML/JS dashboard visualizing the data overlay.

## Directory Structure

*   `kafka_exporter.py`: Python module to be used within your DeepStream app to send data.
*   `web_dashboard/`: The consumer application.
    *   `app.py`: Flask server with Kafka Consumer.
    *   `templates/dashboard.html`: The frontend UI.
*   `docker-compose-kafka.yml`: Setup for Kafka and Zookeeper.

## How to Run

### 1. Start Kafka
First, you need a running Kafka broker.

```bash
cd deepstream/kafka_example
docker-compose -f docker-compose-kafka.yml up -d
```

### 2. Integrate Producer into DeepStream
Modify your DeepStream `main.py` (or use the provided `kafka_exporter.py`).

*   Import the exporter: `from kafka_example.kafka_exporter import KafkaExporter`
*   Initialize it: `exporter = KafkaExporter()`
*   In your probe function, extract metadata and call `exporter.send_detections(frame_num, detections)`.

*(See `kafka_exporter.py` for a code snippet)*

### 3. Run the Web Dashboard
Install dependencies:
```bash
pip install flask flask-socketio confluent-kafka
```

Run the server:
```bash
python3 deepstream/kafka_example/web_dashboard/app.py
```

Visit `http://localhost:5000` in your browser.

### 4. Run DeepStream App
Run your DeepStream application. You should see detection logs appearing in the web dashboard in real-time.
