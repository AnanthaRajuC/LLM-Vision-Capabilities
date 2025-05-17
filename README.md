
# LLM-Vision-Capabilities

This Python script allows you to identify crops in an image using a local [Ollama](https://ollama.com/) server with vision-capable large language models (LLMs) such as `llama3.2-vision` or `qwen2.5vl`.

It sends an image and a predefined JSON-format prompt to a selected vision model running locally via Ollama, and returns structured information about the crop detected in the image.

## Features

- Uses models like `llama3.2-vision` and `qwen2.5vl` via the Ollama API
- Accepts a local image and outputs structured JSON including:
  - Crop name
  - Alternate crop names
  - Color details
  - Confidence score
  - Metadata like inference time

## Requirements

- Python 3.6+
- [Ollama](https://ollama.com) installed and running locally
- Required Python packages:
  - `requests`
  - `Pillow`
  - `ollama` (Ollama Python SDK)

## Installation

```bash
pip install requests pillow ollama
```

Ensure Ollama is installed and running:

```bash
ollama serve
```

Then pull the desired vision model(s):

```bash
ollama pull llama3.2-vision
ollama pull qwen2.5vl
```

## Usage

```bash
python3 LLM-Vision-Capabilities.py <model_name> <image_path>
```

### Examples

```bash
python3 LLM-Vision-Capabilities.py llama3.2-vision:latest /home/user/image.jpg
python3 LLM-Vision-Capabilities.py qwen2.5vl:latest /home/user/image.jpg
```

If no arguments are passed, defaults will be used:
- Model: `qwen2.5vl:latest`
- Image: `/home/anantharajuc/Desktop/ng.jpg`

## Output

The result is a structured JSON response, like:

```json
{
  "crop": "wheat",
  "alternate_names": ["triticum"],
  "color": ["golden", "brown"],
  "confidence": 0.92,
  "metadata": {
    "startDateTime": "2025-05-17T12:00:00",
    "endDateTime": "2025-05-17T12:00:03",
    "duration": 3.0
  }
}
```

## Notes

- Ensure that the Ollama server is running on `http://localhost:11434`
- The script encodes the image in base64 before sending it to the model
- The output strictly follows the expected JSON schema

## License

MIT License

## Author

Anantharaju C
