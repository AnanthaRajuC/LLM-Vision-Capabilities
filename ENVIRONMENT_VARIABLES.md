## Purpose and Scope

This page documents the environment variable configuration system used throughout the LLM Vision Capabilities application. Environment variables provide external configuration for database connectivity, service endpoints, and table naming conventions. The system uses a .env file pattern with centralized loading through the configuration module.

## ClickHouse Configuration Variables

The system requires several environment variables for ClickHouse database connectivity.

## ClickHouse Environment Variable Configuration

| Variable                          | Current Value             | Default Value | Type     | Required | Purpose                                  |
|----------------------------------|---------------------------|----------------|----------|----------|------------------------------------------|
| CLICKHOUSE_HOST                  | localhost                 | None           | String   | Yes      | ClickHouse server hostname               |
| CLICKHOUSE_PORT                  | 9000                      | 9000           | Integer  | No       | Native TCP protocol port                 |
| CLICKHOUSE_PORT_HTTP             | 8123                      | 8123           | Integer  | No       | HTTP API port (documented only)          |
| CLICKHOUSE_USER                  | default                   | None           | String   | Yes      | Database authentication username         |
| CLICKHOUSE_PASSWORD              | root                      | None           | String   | Yes      | Database authentication password         |
| CLICKHOUSE_DATABASE              | default                   | None           | String   | Yes      | Target database schema                   |
| CLICKHOUSE_CROP_ANALYSIS_TABLE   | crop_analysis_results     | None           | String   | Yes      | Detailed analysis results table          |
| CLICKHOUSE_CROP_DETECTION_TABLE  | crop_detection_results    | None           | String   | Yes      | Basic detection results table            |

## Hard-coded Configuration Constants

Several configuration values are hard-coded in crop_detector/config.py and not externally configurable:

- **OLLAMA_URL**: Fixed to `"http://localhost:11434"`
- **DEFAULT_MODEL_NAME**: Set to `"qwen2.5vl:latest"`
- **PROMPT_TYPE**: Configured as `"detailed"`
- **DEFAULT_IMAGE_PATH**: Derived from script directory structure