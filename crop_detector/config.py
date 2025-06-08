import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

OLLAMA_URL = "http://localhost:11434"

DEFAULT_MODEL_NAME = "qwen2.5vl:latest"
DEFAULT_IMAGE_PATH = os.path.join(SCRIPT_DIR,"assets","images","demo2.jpg")

PROMPT_TYPE = "detailed"

PROMPT_FILE = {
    "basic": "crop_detection.txt",
    "detailed": "crop_analysis.txt"
}.get(PROMPT_TYPE, "crop_detection.txt")

PROMPT_PATH = os.path.join(SCRIPT_DIR, "assets", "prompts", PROMPT_FILE)

# Load prompt from file
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    PROMPT = f.read()

CLICKHOUSE_CONFIG = {
    'host': os.getenv('CLICKHOUSE_HOST'),
    'port': int(os.getenv('CLICKHOUSE_PORT', 9000)),
    'user': os.getenv('CLICKHOUSE_USER'),
    'password': os.getenv('CLICKHOUSE_PASSWORD'),
    'database': os.getenv('CLICKHOUSE_DATABASE'),
    'table_crop_analysis': os.getenv('CLICKHOUSE_CROP_ANALYSIS_TABLE'),
    'table_crop_detection': os.getenv('CLICKHOUSE_CROP_DETECTION_TABLE')
}
