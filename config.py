import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

OLLAMA_URL = "http://localhost:11434"

DEFAULT_MODEL_NAME = "qwen2.5vl:latest"
DEFAULT_IMAGE_PATH = os.path.join(SCRIPT_DIR, "demo.jpg")

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

CLICKHOUSE_CONFIG = {
    'host': 'localhost',
    'port': 9000,
    'user': 'default',
    'password': 'root',
    'database': 'default',
    'table': 'crop_detection_results'
}
