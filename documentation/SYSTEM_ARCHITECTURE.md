## System Architecture

This document provides an overview of the multi-modal crop intelligence system architecture, detailing how vision-language models, semantic search, and voice processing components interact to deliver three distinct interaction modes: image analysis, text-based search, and voice-enabled querying.

## Core Processing Components

The system's processing layer consists of specialized controllers that handle different input modalities while sharing common infrastructure components.

### Component File Responsibilities

| Component                | File Path                                      | Primary Responsibility                                       |
|--------------------------|------------------------------------------------|--------------------------------------------------------------|
| Image Analysis Controller| `crop_detector/main.py`                        | Orchestrates VLM-based crop detection and analysis           |
| Text Search Controller   | `crop_detector/search/CropSemanticSearch.py`   | Handles semantic similarity search queries                   |
| Voice Search Controller  | `crop_detector/search/speech_input.py`         | Processes voice input and routes to text search              |
| Configuration Manager    | `crop_detector/config.py`                      | Centralizes environment and prompt configuration             |
| LLM Interface            | `crop_detector/ollama_client.py`               | Manages communication with Ollama server                     |
| Image Processing         | `crop_detector/images_util.py`                 | Handles image encoding and preprocessing                     |
| Database Interface       | `crop_detector/db/clickhouse_client.py`        | Manages ClickHouse operations and embeddings                 |

## AI Model Integration Architecture

The system integrates multiple specialized AI models through standardized interfaces, with Ollama serving as the primary model orchestration layer.

### Model Overview

| Model Type         | Model Name                 | Dimensions | Usage                      |
|--------------------|----------------------------|------------|-----------------------------|
| Vision-Language    | `qwen2.5vl:latest`         | N/A        | Primary crop analysis model |
| Vision-Language    | `llama3.2-vision:latest`   | N/A        | Alternative VLM option      |
| Text Embedding     | `all-MiniLM-L6-v2`         | 384        | Text semantic search        |
| Image Embedding    | `clip-vit-base-patch32`    | 512        | Image semantic search       |
| Speech Recognition | `whisper-base`             | N/A        | Voice input transcription   |

## Data Persistence Architecture

The system employs ClickHouse as the primary data store, supporting both structured crop analysis results and high-dimensional embedding vectors for semantic search.