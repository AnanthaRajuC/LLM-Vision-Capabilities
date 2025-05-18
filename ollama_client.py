import requests
import ollama
from config import OLLAMA_URL

def check_ollama_status() -> bool:
    try:
        requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        print(f"Ollama is running at {OLLAMA_URL}\n")
        return True
    except requests.exceptions.RequestException:
        return False

def call_model(model_name: str, prompt: str, image_base64: str) -> dict:
    print(f"Preparing message for chatting with the model")
    messages = [{
        'role': 'user',
        'content': prompt,
        'images': [image_base64]
    }]
    print(f"Starting Ollama chat. Response time is several seconds to a couple of minutes.")
    return ollama.chat(model=model_name, messages=messages)
