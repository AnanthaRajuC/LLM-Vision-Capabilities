## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

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
│   ├── config.py                         # Configs and env
│   ├── images_util.py                    # Image encoding
│   ├── main.py                           # Unified entry point
│   └── ollama_client.py
└── .env                                  # ClickHouse credentials
```

### Prerequisites

*	You need to have **ClickHouse** installed on your machine to persist the results. Using `DBeaver` or on any other ClickHouse client/console, create a database/schema/table named `crop_detection_results` and `crop_analysis_results`. 

- ![crop_detection_results.sql](crop_detector/assets/sql/crop_detection_results.sql)
- ![crop_analysis_results.sql](crop_detector/assets/sql/crop_analysis_results.sql)

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

## 🚀 Usage

Once everything is set up, you can run the script to process an image using one of the vision models.

Use the following command:

```bash
python3 LLM-Vision-Capabilities.py <model_name> <image_path>
```

- `<model_name>`: The name of the model you pulled (e.g., `llama3.2-vision:latest` or `qwen2.5vl:latest`).
- `<image_path>`: The full path to the image file you want to analyze.

### ✅ Examples

```bash
python3 LLM-Vision-Capabilities.py llama3.2-vision:latest /home/user/image.jpg
python3 LLM-Vision-Capabilities.py qwen2.5vl:latest /home/user/image.jpg
```

These commands will send the image to the selected model and print the response, which may include image descriptions, object recognition, or other model-specific capabilities.

---

## 🧠 Default Behavior

If you run the script without any arguments, it will use default values:

```bash
python3 LLM-Vision-Capabilities.py
```

- **Default model**: `qwen2.5vl:latest`
- **Default image**: `assets/demo.jpg` (ensure this file is accessible from the script)

This makes it easy to test the script quickly without having to specify parameters.

---

## 📝 Notes

- Ensure that the Ollama server is running on `http://localhost:11434`
- The output strictly follows the expected JSON schema
- The models can take some time to load initially, especially on the first run.
- Model capabilities vary: some may be better at object detection, others at text reading or image captioning.
- Ensure your system has enough RAM and compute resources to run large vision models locally.
