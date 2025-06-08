import requests
import base64
import os

def qwen_describe_image(image_path, prompt="What crop is in this image?", model="qwen2.5vl:latest"):
    print("Starting Qwen describe function")

    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return None

    # Read and encode image to base64
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # Embed image base64 inside text prompt with <image> tags
    message_content = f"<image>{image_b64}</image> {prompt}"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": message_content
            }
        ],
        "stream": False
    }

    print(f"📤 Sending '{os.path.basename(image_path)}' to Qwen with prompt: \"{prompt}\"")

    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        response.raise_for_status()
        print("✅ Received response from Ollama")
        print("Full response JSON:", response.json())

        answer = response.json()["message"]["content"]
        print(f"📝 Qwen says: {answer}")
        return answer
    except requests.RequestException as e:
        print(f"❌ Failed to query Ollama: {e}")
        if e.response is not None:
            print("Response content:", e.response.text)
        return None

if __name__ == "__main__":
    image_path = "/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/assets/images/demo.jpg"
    qwen_describe_image(image_path)
