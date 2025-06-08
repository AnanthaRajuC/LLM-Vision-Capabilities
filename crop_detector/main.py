#!/usr/bin/env python3
"""
Crop Detection System using Qwen 2.5 Vision LLM
Identifies crops in images and stores results in ClickHouse
"""

import sys
import json
from datetime import datetime

from crop_detector.config import DEFAULT_MODEL_NAME, DEFAULT_IMAGE_PATH, PROMPT, CLICKHOUSE_CONFIG, PROMPT_TYPE

from crop_detector.image_utils import encode_image
from ollama_client import check_ollama_status, call_model
from crop_detector.db.clickhouse_client import save_to_clickhouse_basic
from crop_detector.db.clickhouse_client import save_to_clickhouse_detailed
from crop_detector.db.clickhouse_client import save_to_clickhouse_with_embeddings

# Parse CLI arguments
model_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL_NAME
image_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_IMAGE_PATH

# Set this flag to control DB saving
save_to_db = True

print(f"Model: {model_name}")
print(f"Image: {image_path}")
print(f"Save to ClickHouse: {save_to_db}")

# ====================== CHECK OLLAMA STATUS ======================
if not check_ollama_status():
    print("Ollama is not running. Start the Ollama server.")
    sys.exit(1)

# Encode image
image_base64 = encode_image(image_path)

# Send to Ollama
start_time = datetime.now()
response = call_model(model_name, PROMPT, image_base64)
end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

# Parse response
try:
    print("Parsing result from model")
    result_json = json.loads(response['message']['content'])
except json.JSONDecodeError:
    print("Error: Invalid JSON response from model.")
    sys.exit(1)

# Add metadata
print("Adding Metadata")
result_json['metadata'] = {
    'startDateTime': start_time.isoformat(),
    'endDateTime': end_time.isoformat(),
    'duration': round(duration, 2)
}

# Output result
print(json.dumps(result_json, indent=2))

# Save to ClickHouse
if save_to_db:
    try:
        print("Saving result to ClickHouse")

        # Use the appropriate save function based on PROMPT_TYPE
        if PROMPT_TYPE == "basic":
            save_to_clickhouse_basic(CLICKHOUSE_CONFIG, result_json)
        else:
            #save_to_clickhouse_detailed(CLICKHOUSE_CONFIG, result_json)
            save_to_clickhouse_with_embeddings(CLICKHOUSE_CONFIG, result_json)

        print("Saved to ClickHouse successfully.")
    except Exception as e:
        print(f"Failed to save to ClickHouse: {e}")

