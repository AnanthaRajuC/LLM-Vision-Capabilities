import os
import requests
import ollama
from PIL import Image
import base64
from io import BytesIO
import sys
from datetime import datetime
import json
from clickhouse_driver import Client as ClickHouseClient

# ====================== CONFIGURATION DEFAULTS ======================

DEFAULT_MODEL_NAME = "qwen2.5vl:latest"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_IMAGE_PATH = os.path.join(SCRIPT_DIR, "demo.jpg")
OLLAMA_URL = "http://localhost:11434"

PROMPT = (
    "Identify the crop in this image and respond ONLY in the following JSON format:\n\n"
    "{\n"
    "  \"crop\": \"<primary crop name>\",\n"
    "  \"alternate_names\": [\"<alternate name 1>\", \"<alternate name 2>\"],\n"
    "  \"color\": [\"<color 1>\", \"<color 2>\"],\n"
    "  \"confidence\": <confidence score from 0 to 1>\n"
    "}\n\n"
    "If any field is not known, return an empty list or null value as appropriate. Do not include any other text."
)

# ====================== CLICKHOUSE CONFIGURATION ======================

CLICKHOUSE_CONFIG = {
    'host': 'localhost',
    'port': 9000,
    'user': 'default',
    'password': 'root',
    'database': 'default',
    'table': 'crop_detection_results'
}

# ====================== SAVE TO CLICKHOUSE FUNCTION ======================

def save_to_clickhouse(data: dict):
    client = ClickHouseClient(
        host=CLICKHOUSE_CONFIG['host'],
        port=CLICKHOUSE_CONFIG['port'],
        user=CLICKHOUSE_CONFIG['user'],
        password=CLICKHOUSE_CONFIG['password'],
        database=CLICKHOUSE_CONFIG['database']
    )
    # Convert ISO string to datetime objects
    start_dt = datetime.fromisoformat(data['metadata']['startDateTime'])
    end_dt = datetime.fromisoformat(data['metadata']['endDateTime'])

    client.execute(f'''
            INSERT INTO {CLICKHOUSE_CONFIG['table']} 
            (crop, alternate_names, color, confidence, startDateTime, endDateTime, duration)
            VALUES
        ''', [(data['crop'], data['alternate_names'], data['color'], data['confidence'],
               start_dt, end_dt, data['metadata']['duration'])])

# ====================== PARSE COMMAND LINE ARGUMENTS ======================

model_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL_NAME
image_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_IMAGE_PATH

# Flag to control saving
save_to_db = True  # Change this to False to disable saving

print(f"Using model name: {model_name}")
print(f"Using image path: {image_path}")
print(f"Saving to ClickHouse enabled: {save_to_db}\n")

# ====================== CHECK OLLAMA STATUS ======================

print("Checking if Ollama server is running...")
try:
    requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
    print(f"Ollama is running at {OLLAMA_URL}\n")
except requests.exceptions.RequestException:
    print("Ollama is not running. Please start the Ollama server.")
    sys.exit(1)

# ====================== IMAGE ENCODING FUNCTION ======================

def encode_image(image_path):
    print(f"Encoding image from: {image_path}")
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    print("Image encoding complete.\n")
    return img_str

# ====================== PREPARE INPUT ======================

print("Preparing input image and prompt...")
image_base64 = encode_image(image_path)
print("Prompt ready.\n")

# ====================== SEND REQUEST TO OLLAMA ======================

print("Sending image and prompt to Ollama model...")
start_time = datetime.now()

if model_name.startswith("llama3.2-vision"):
    messages = [{
        'role': 'user',
        'content': PROMPT,
        'images': [image_base64]
    }]
else:
    messages = [{
        'role': 'user',
        'content': PROMPT,
        'images': [image_base64]
    }]

response = ollama.chat(
    model=model_name,
    messages=messages
)

end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

# ====================== PARSE AND ADD METADATA ======================

try:
    result_json = json.loads(response['message']['content'])
except json.JSONDecodeError:
    print("Error: Ollama response is not valid JSON.")
    sys.exit(1)

result_json['metadata'] = {
    'startDateTime': start_time.isoformat(),
    'endDateTime': end_time.isoformat(),
    'duration': round(duration, 2)
}

# ====================== OUTPUT FINAL JSON ======================

print("Received response with metadata:\n")
print(json.dumps(result_json, indent=2))

# ====================== SAVE TO CLICKHOUSE IF ENABLED ======================

if save_to_db:
    print("\nSaving results to ClickHouse...")
    try:
        save_to_clickhouse(result_json)
        print("Saved to ClickHouse successfully.")
    except Exception as e:
        print(f"Failed to save to ClickHouse: {e}")
else:
    print("\nSave to ClickHouse disabled, skipping save.")
