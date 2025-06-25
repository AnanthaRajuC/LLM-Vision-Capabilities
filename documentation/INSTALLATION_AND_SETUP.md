## Installation and Setup

This document provides step-by-step instructions for installing and configuring the LLM Vision Capabilities system. It covers all prerequisites, dependencies, and configuration steps required to run the multi-modal crop intelligence system locally.

## Prerequisites

The system requires three core external dependencies that must be installed before setting up the Python application:

## Component Versions

| Component   | Version | Purpose                       |
|-------------|---------|-------------------------------|
| Python      | 3.8+    | Application runtime           |
| ClickHouse  | Latest  | Vector storage and search     |
| Ollama      | Latest  | Local LLM inference server    |

## System Requirements

- **RAM**: Minimum 8GB (16GB+ recommended for larger vision models)
- **Storage**: 10GB+ free space for model downloads
- **Network**: Internet access for initial model downloads

## Ollama Installation and Configuration

### Server Setup

1. Download and Install Ollama

> Visit [https://ollama.com/download](https://ollama.com/download) for platform-specific installer

2. Start Ollama Server

```bash
ollama serve
```

The server will run on **http://localhost:11434** by default.

3. Download Vision Models

```bash
ollama pull llama3.2-vision
ollama pull qwen2.5vl
```

### Model Configuration

The system uses **qwen2.5vl:latest** as the default model, configured in 
`crop_detector/config.py`. The model selection can be changed by modifying the **DEFAULT_MODEL_NAME** constant.

### Model Characteristics:

- **qwen2.5vl**: Primary model, optimized for JSON output
- **llama3.2-vision**: Alternative vision model

## ClickHouse Database Setup

### Database Schema Creation

The system requires two ClickHouse tables for data persistence:

### Table Creation Steps

1. **Install ClickHouse Server** Follow the official ClickHouse installation guide for your platform.  

2. **Create Database Tables** Execute the SQL scripts located in the assets directory:  

   - crop_detector/assets/sql/crop_detection_results.sql
   - crop_detector/assets/sql/crop_analysis_results.sql

3. **Verify Table Structure** Use DBeaver or ClickHouse console to confirm tables are created correctly.

## Environment Configuration

Create and configure the `.env` file in the project root:

```bash
# ClickHouse Database Configuration
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_PORT_HTTP=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=root
CLICKHOUSE_DATABASE=default
CLICKHOUSE_CROP_ANALYSIS_TABLE=crop_analysis_results
CLICKHOUSE_CROP_DETECTION_TABLE=crop_detection_results
```

### Configuration Loading

The system loads environment variables through `crop_detector/config.py` using the `python-dotenv` package. The `CLICKHOUSE_CONFIG` dictionary at `crop_detector/config.py` maps environment variables to application settings.

## Validation Steps

### System Verification Checklist

Verification Commands

1. **Check Ollama Server**

~~~bash
curl http://localhost:11434/api/version
~~~

2. **List Available Models**

~~~bash
ollama list
~~~

3. **Test Python Dependencies**

~~~bash
python -c "import requests, ollama, clickhouse_connect; print('Dependencies OK')"
~~~

4. **Verify Configuration Loading**

~~~bash
python -c "from crop_detector.config import CLICKHOUSE_CONFIG, DEFAULT_MODEL_NAME; print(f'Model: {DEFAULT_MODEL_NAME}'); print(f'DB Host: {CLICKHOUSE_CONFIG[\"host\"]}')"
~~~

5. **Test ClickHouse Connection**

~~~bash
python -c "import clickhouse_connect; client = clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='root'); print('ClickHouse connected')"
~~~

## Common Installation Issues and Solutions

| Issue                          | Symptom                    | Solution                                  |
|-------------------------------|----------------------------|-------------------------------------------|
| Ollama not found              | `Connection refused`          | Ensure `ollama serve` is running          |
| Model not available           | `Model not found`             | Run `ollama pull qwen2.5vl`               |
| ClickHouse connection failed  | `Connection error`            | Verify ClickHouse server and credentials  |
| Import errors                 | `ModuleNotFoundError`         | Install missing Python packages           |
| Environment variables not loaded | `None` values in config    | Check `.env` file location and syntax     |

The system is now ready for basic usage. 
