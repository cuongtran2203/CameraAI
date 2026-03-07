import json
import time
from confluent_kafka import Producer
import socket

class KafkaExporter:
    def __init__(self, bootstrap_servers='localhost:29092', topic='camera-detections'):
        self.topic = topic
        conf = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': socket.gethostname()
        }
        self.producer = Producer(conf)

    def send_detections(self, frame_num, detections):
        """
        Send a batch of detections to Kafka.

        Args:
            frame_num (int): The current frame number.
            detections (list): A list of dictionaries, each containing detection info:
                               {'class_id': int, 'label': str, 'confidence': float, 'bbox': [x, y, w, h]}
        """
        payload = {
            'timestamp': time.time(),
            'frame_num': frame_num,
            'detections': detections
        }

        # Serialize to JSON
        json_payload = json.dumps(payload).encode('utf-8')

        try:
            self.producer.produce(self.topic, value=json_payload, callback=self.delivery_report)
            # Use poll to serve delivery reports (optional but recommended for high throughput)
            self.producer.poll(0)
        except BufferError:
            print(f"Local producer queue is full ({len(self.producer)} messages awaiting delivery)")

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            # print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
            pass

    def close(self):
        self.producer.flush()

# --- Example Usage in a DeepStream Probe ---
#
# exporter = KafkaExporter()
#
# def osd_sink_pad_buffer_probe(pad, info, u_data):
#     # ... (Standard pyds extraction logic) ...
#
#     frame_detections = []
#     l_obj = frame_meta.obj_meta_list
#     while l_obj is not None:
#         obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
#         frame_detections.append({
#             'class_id': obj_meta.class_id,
#             'label': obj_meta.obj_label,
#             'confidence': obj_meta.confidence,
#             'bbox': [
#                 obj_meta.rect_params.left,
#                 obj_meta.rect_params.top,
#                 obj_meta.rect_params.width,
#                 obj_meta.rect_params.height
#             ]
#         })
#         l_obj = l_obj.next
#
#     exporter.send_detections(frame_meta.frame_num, frame_detections)
#
#     return Gst.PadProbeReturn.OK
