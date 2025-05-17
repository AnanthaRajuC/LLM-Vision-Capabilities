import os

import requests
import ollama
from PIL import Image
import base64
from io import BytesIO
import sys
from datetime import datetime
import json

# ====================== CONFIGURATION DEFAULTS ======================

DEFAULT_MODEL_NAME = "qwen2.5vl:latest"
# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Set default image path relative to the script directory
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

# ====================== PARSE COMMAND LINE ARGUMENTS ======================

model_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL_NAME
image_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_IMAGE_PATH

print(f"Using model name: {model_name}")
print(f"Using image path: {image_path}\n")

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

# Adjust input structure depending on model
if model_name.startswith("llama3.2-vision"):
    messages = [{
        'role': 'user',
        'content': PROMPT,
        'images': [image_base64]  # base64 expected
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
