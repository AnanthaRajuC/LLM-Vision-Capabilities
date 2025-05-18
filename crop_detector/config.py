import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

OLLAMA_URL = "http://localhost:11434"

DEFAULT_MODEL_NAME = "qwen2.5vl:latest"
DEFAULT_IMAGE_PATH = os.path.join(SCRIPT_DIR,"assets","demo.jpg")

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
    'host': os.getenv('CLICKHOUSE_HOST'),
    'port': int(os.getenv('CLICKHOUSE_PORT', 9000)),
    'user': os.getenv('CLICKHOUSE_USER'),
    'password': os.getenv('CLICKHOUSE_PASSWORD'),
    'database': os.getenv('CLICKHOUSE_DATABASE'),
    'table': os.getenv('CLICKHOUSE_TABLE')
}
