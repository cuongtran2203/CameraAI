import os
import time
import requests
import random
import sys

API_URL = "http://localhost:8000/api/v1/retrieval/search"
CAMERA_IDS = ["cam_test_01", "cam_test_02"]

def mock_camera_stream(target_path: str, interval: int = 5):
    if not os.path.exists(target_path):
        print(f"Error: Path '{target_path}' not found.")
        sys.exit(1)
        
    images = []
    if os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    images.append(os.path.join(root, file))
        if not images:
            print(f"Error: No images found in directory '{target_path}'")
            sys.exit(1)
        print(f"Found {len(images)} images in directory. Will pick randomly.")
    else:
        images = [target_path]

    print(f"Starting mock camera stream...")
    print(f"Target API: {API_URL}")
    print(f"Interval: {interval} seconds")
    print(f"Cameras: {', '.join(CAMERA_IDS)}")
    print("-" * 50)

    try:
        while True:
            camera_id = random.choice(CAMERA_IDS)
            image_path = random.choice(images)
            print(f"[{time.strftime('%H:%M:%S')}] {camera_id} capturing {os.path.basename(image_path)}...")
            
            with open(image_path, "rb") as f:
                # Need to post as multipart/form-data
                files = {"image": (os.path.basename(image_path), f, "image/jpeg")}
                data = {"camera_id": camera_id}
                
                try:
                    response = requests.post(API_URL, files=files, data=data)
                    if response.status_code == 200:
                        result = response.json()
                        top_results = result.get("top_k", [])
                        if top_results:
                            top_match = top_results[0]
                            food_name = top_match.get("description", "Unknown")
                            score = top_match.get("score", 0)
                            print(f"  ✅ AI detected: {food_name} (Score: {score}) -> Published to Kafka!")
                        else:
                            print(f"  ⚠️ AI processed image but found no matches.")
                    else:
                        print(f"  ❌ API Error {response.status_code}: {response.text}")
                except requests.exceptions.ConnectionError:
                    print(f"  ❌ Connection Error: Ensure ai_service is running on port 8000.")
                except Exception as e:
                    print(f"  ❌ Error: {e}")
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopping mock stream...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mock_camera_client.py <path_to_image_OR_folder> [interval_seconds]")
        print("Example 1: python3 mock_camera_client.py sample_food.jpg 5")
        print("Example 2: python3 mock_camera_client.py my_food_images_folder/ 5")
        sys.exit(1)
        
    target_path = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    mock_camera_stream(target_path, interval)
