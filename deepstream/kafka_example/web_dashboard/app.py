from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from confluent_kafka import Consumer
import threading
import json
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:29092'
KAFKA_TOPIC = 'camera-detections'

def kafka_consumer_thread():
    """
    Background thread to consume messages from Kafka and emit to WebSocket clients.
    """
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'dashboard-consumer-group',
        'auto.offset.reset': 'latest'
    }

    try:
        consumer = Consumer(conf)
        consumer.subscribe([KAFKA_TOPIC])
        print("Kafka Consumer Started...")
    except Exception as e:
        print(f"Failed to start consumer: {e}")
        return

    try:
        while True:
            msg = consumer.poll(1.0) # Timeout 1s

            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            # Process valid message
            try:
                message_value = msg.value().decode('utf-8')
                data = json.loads(message_value)

                # Emit to all connected clients
                # Namespace '/' is default
                socketio.emit('new_detection', data)
                # print(f"Received frame {data['frame_num']}")

            except json.JSONDecodeError:
                print("Error decoding JSON message")
            except Exception as e:
                print(f"Error processing message: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    # Start Kafka Consumer in a background thread
    t = threading.Thread(target=kafka_consumer_thread)
    t.daemon = True
    t.start()

    # Start Web Server
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
