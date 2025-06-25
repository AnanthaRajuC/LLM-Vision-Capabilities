## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Technology Stack Integration

| Component            | Technology                                  | Primary Use Case                        |
|----------------------|---------------------------------------------|------------------------------------------|
| Vision-Language Models | Qwen 2.5 Vision, LLaMA 3.2-Vision           | Image analysis and crop identification   |
| Model Serving         | Ollama (localhost:11434)                    | Local VLM inference                      |
| Speech Processing     | Whisper base model                          | Audio transcription                      |
| Text Embeddings       | SentenceTransformer all-MiniLM-L6-v2        | Semantic search encoding                 |
| Image Embeddings      | CLIP openai/clip-vit-base-patch32           | Image feature extraction                 |
| Vector Database       | ClickHouse                                   | Similarity search and metadata storage   |
| Audio Processing      | sounddevice, scipy.io.wavfile               | Voice input recording                    |

## Feature Comparison Matrix

| Feature             | Image Analysis                            | Text Search                              | Voice Search                             |
|---------------------|--------------------------------------------|-------------------------------------------|-------------------------------------------|
| Primary Function    | Crop identification and analysis           | Semantic similarity search                | Voice-to-text search                      |
| Input Type          | Image files                                | Natural language text                     | Audio recording                           |
| Processing Model    | Qwen 2.5 Vision / LLaMA 3.2-Vision          | SentenceTransformer embeddings            | Whisper + SentenceTransformer             |
| Output Format       | Structured JSON with analysis              | Ranked similarity results                 | Search results via transcription          |
| Data Storage        | Stores new analysis results                | Queries existing data                     | Queries existing data                     |
| Typical Use Case    | "Analyze this crop photo"                  | "Find crops with red flowers"             | "Show me green leafy vegetables"          |


## Files and Directories Structure

The project (a.k.a. project directory) has a particular directory structure. A representative project is shown below:

### Project Structure

```text
.
├── crop_detector
│   ├── assets/
│   │  ├── images/
│   │  │   └── demo.jpg
│   │  ├── prompts/
│   │  │   ├── crop_analysis.txt
│   │  │   └── crop_detection.txt
│   │  └── sql/
│   │      ├── crop_analysis_results.sql
│   │      └── crop_detection_results.sql
│   ├── db/
│   │   └── clickhouse_client.py          # ClickHouse storage functions
│   ├── search/
│   │   ├── CropSemanticSearch.py
│   │   └── speech_input.py
│   ├── config.py                         # Configs and env
│   ├── images_util.py                    # Image encoding
│   ├── main.py                           # Unified entry point
│   └── ollama_client.py
└── .env                                  # ClickHouse credentials
```

### Prerequisites

The system requires three core external dependencies that must be installed before setting up the Python application:

## Component Versions

| Component   | Version | Purpose                        |
|-------------|---------|--------------------------------|
| Python      | 3.8+    | Application runtime            |
| ClickHouse  | Latest  | Vector storage and search      |
| Ollama      | Latest  | Local LLM inference server     |

**System Requirements**

- **RAM**: Minimum 8GB (16GB+ recommended for larger vision models)
- **Storage**: 10GB+ free space for model downloads
- **Network**: Internet access for initial model downloads

*	You need to have **ClickHouse** installed on your machine to persist the results. Using `DBeaver` or on any other ClickHouse client/console, create a database/schema/table named `crop_detection_results` and `crop_analysis_results`. 

- crop_detector/assets/sql/crop_detection_results.sql
- crop_detector/assets/sql/crop_analysis_results.sql

We need to specify our Environment variables for the application. Open up the **`.env`** file in crop_detector directory and update the fields with appropriate values.

~~~txt
CLICKHOUSE_HOST= 
CLICKHOUSE_PORT= 
CLICKHOUSE_USER= 
CLICKHOUSE_PASSWORD= 
CLICKHOUSE_DATABASE= 
CLICKHOUSE_TABLE= 
~~~

## 📦 Installation

To get started, you'll need Python installed on your machine (preferably Python 3.8 or later).

1. **Install the required Python packages**  
   Run the following command in your terminal to install the dependencies:

   ```bash
   pip install requests pillow ollama
   ```

   - `requests`: For making HTTP requests to the Ollama server.
   - `pillow`: For opening and manipulating image files.
   - `ollama`: A Python client to interact with Ollama models.

2. **Install and run Ollama**  
   If you haven’t already, [download and install Ollama](https://ollama.com/download) for your platform.

   Once installed, start the Ollama server:

   ```bash
   ollama serve
   ```

   This runs a local server that allows your Python script to communicate with the models.

3. **Pull the vision-enabled models**  
   Ollama needs to download the specific models you'll be using. Pull the vision-capable models with:

   ```bash
   ollama pull llama3.2-vision
   ollama pull qwen2.5vl
   ```

   This downloads the models and makes them available for use in your local environment.

---

## 🧠 Prompt Configuration

The app uses two levels of prompt complexity, stored externally as text files under `assets/prompts/`:

### Available Prompts

| Prompt Level | File Path                             | Description                                  |
|--------------|---------------------------------------|----------------------------------------------|
| Basic        | `assets/prompts/crop_detection.txt`   | Identifies crop, colors, and confidence only |
| Detailed     | `assets/prompts/crop_analysis.txt`    | Full image-based agricultural assessment     |

---

## 🚀 Quick Start Guide

Get up and running with the core features of this multimodal crop assistant:

### 🖼️ Image Analysis
- Add your crop image to: `crop_detector/assets/images/`
- Open `crop_detector/config.py` and update **`image_name`** (Line 11) with your file name.
- Run the main script:  
  ```bash
  python crop_detector/main.py
  ```

### 📝 Text-Based Image Search
- Open `crop_detector/Search/CropSemanticSearch.py`
- Update the search query at **Line 63** with your desired text (e.g., `"crops with red flowers"`)
- Run the script:
  ```bash
  python crop_detector/Search/CropSemanticSearch.py
  ```

### 🎤 Voice-Based Image Search
- Run the voice input script:
  ```bash
  python crop_detector/Search/speech_input.py
  ```
- Speak your search query naturally — results will appear based on semantic similarity.

---

### 🛠️ Coming Soon
In the next version:
- API endpoints for programmatic access  
- Batch processing support  
- Simple web UI for non-developers  
- Modular enhancements for easier integration



---

## 📝 Notes

- Ensure that the Ollama server is running on `http://localhost:11434`
- The output strictly follows the expected JSON schema
- The models can take some time to load initially, especially on the first run.
- Model capabilities vary: some may be better at object detection, others at text reading or image captioning.
- Ensure your system has enough RAM and compute resources to run large vision models locally.

## Common Issues and Solutions

| Issue                          | Symptom                    | Solution                                  |
|-------------------------------|----------------------------|-------------------------------------------|
| Ollama not found              | Connection refused          | Ensure `ollama serve` is running          |
| Model not available           | Model not found             | Run `ollama pull qwen2.5vl`               |
| ClickHouse connection failed  | Connection error            | Verify ClickHouse server and credentials  |
| Import errors                 | ModuleNotFoundError         | Install missing Python packages           |
| Environment variables not loaded | None values in config    | Check `.env` file location and syntax     |

