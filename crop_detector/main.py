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


# ------------------------ Description Generator ------------------------
def generate_description_from_json(data: dict) -> str:
    try:
        crop = data.get("crop", "Unknown crop")
        color = ", ".join(data.get("color", []))
        stage = data.get("growth_stage", {}).get("stage", "unknown")
        age = data.get("growth_stage", {}).get("estimated_age_months", "N/A")
        health = data.get("health_assessment", {}).get("overall_health", "unknown")
        stress = ", ".join(data.get("health_assessment", {}).get("stress_indicators", []))
        setting = data.get("environmental_context", {}).get("setting", "unknown")
        terrain = data.get("environmental_context", {}).get("terrain", "unknown")
        irrigation = data.get("growing_conditions", {}).get("irrigation_evidence", "unknown")
        season = data.get("growing_conditions", {}).get("season_indication", "unknown")

        description = (
            f"The image shows a {crop} crop with colors {color}. "
            f"It is in the {stage} stage and approximately {age} months old. "
            f"Overall health is {health}, with stress indicators such as {stress}. "
            f"The field is located in a {setting} area with {terrain} terrain. "
            f"Irrigation type is {irrigation}, and it's currently the {season}."
        )

        return description
    except Exception as e:
        print(f"Error generating description: {e}")
        return "Description unavailable."

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

# Generate textual description
print("Generating text description from JSON")
result_json['text_description'] = generate_description_from_json(result_json)

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
            save_to_clickhouse_detailed(CLICKHOUSE_CONFIG, result_json)

        print("Saved to ClickHouse successfully.")
    except Exception as e:
        print(f"Failed to save to ClickHouse: {e}")

