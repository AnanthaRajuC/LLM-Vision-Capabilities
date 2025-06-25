## Database Schema

This document provides complete technical documentation of the ClickHouse database schema used by the LLM Vision Capabilities system. It covers the table structures, data types, indexing strategies, and embedding vector storage for both basic crop detection and comprehensive agricultural analysis workflows.

## Overview

The system uses ClickHouse as its primary database with two main tables designed for different levels of agricultural analysis. The schema supports both simple crop detection results and comprehensive multi-modal analysis with embedding vectors for semantic search capabilities.

## Storage Engine and Configuration

Both tables use ClickHouse's MergeTree engine optimized for analytical workloads and time-series data. 

## ClickHouse Table Configuration

| Configuration       | crop_detection_results | crop_analysis_results     |
|---------------------|------------------------|----------------------------|
| Engine              | MergeTree              | MergeTree                  |
| Primary Key         | startDateTime          | (crop, startDateTime)      |
| Index Granularity   | 8192 (default)         | 8192                       |
| Partitioning        | None                   | None                       |

The `crop_analysis_results` table uses a compound primary key to enable efficient queries by both crop type and temporal ranges, while `crop_detection_results` uses a simple temporal ordering for basic detection workflows.

## Data Type Specifications

The schema employs ClickHouse-specific data types optimized for agricultural analysis and embedding storage:

## ClickHouse Data Type Reference

| Data Type           | Usage                         | Examples                                               |
|---------------------|-------------------------------|--------------------------------------------------------|
| String              | Text fields, crop names        | `crop`, `growth_stage`, `overall_health`               |
| Array(String)       | Multi-value text fields        | `alternate_names`, `disease_indicators`, `semantic_tags` |
| Array(Float32)      | Embedding vectors              | `text_embedding`, `image_embedding`, `hybrid_embedding` |
| Float32             | Numerical scores, confidence   | `confidence`, `vigor_score`, `duration`                |
| Bool                | Boolean flags                  | `people_present`, `equipment_present`, `animals_present` |
| DateTime            | Timestamps                     | `startDateTime`, `endDateTime`                         |
| Nullable(Float32)   | Optional numerical fields      | `estimated_age_months`, `estimated_months_to_harvest`  |
| UInt32              | Count fields                   | `people_count`, `equipment_count`, `total_animal_count` |

### Basic Detection Table Structure

## Field Specifications

| Field         | Type           | Description                        | Constraints                 |
|---------------|----------------|------------------------------------|-----------------------------|
| crop          | String         | Primary crop name identified       | Required, indexed           |
| alternate_names | Array(String) | Alternative/common names           | Optional                    |
| color         | Array(String)  | Dominant crop colors observed      | Optional                    |
| confidence    | Float32        | Model confidence score             | 0.0 to 1.0                  |
| startDateTime | DateTime       | Analysis start timestamp           | Required, primary key       |
| endDateTime   | DateTime       | Analysis completion timestamp      | Required                    |
| duration      | Float32        | Processing duration in seconds     | Calculated field            |

This table serves as the foundation for simple crop identification workflows and provides a lightweight storage option for basic detection results.

### Comprehensive Analysis Table

The `crop_analysis_results` table stores detailed agricultural analysis with multi-modal embeddings and extensive metadata categorized into logical groupings.

**Comprehensive Analysis Table Categories**

**Crop Identification Fields**  
Core identification data with enhanced description capabilities:

- `crop (String)`: Primary crop name
- `alternate_names (Array(String))`: Alternative crop names
- `color (Array(String))`: Dominant colors observed
- `confidence (Float32)`: Model confidence (0-1)
- `overall_description (String)`: Comprehensive 2-3 sentence image description

**Growth Stage Analysis**  
Temporal and developmental assessment:

- `growth_stage (String)`: Development phase (seedling/vegetative/flowering/fruiting)
- `estimated_age_months (Nullable(Float32))`: Approximate crop age
- `growth_description (String)`: Detailed growth stage indicators

**Health Assessment System**  
Comprehensive plant health evaluation:

- `overall_health (String)`: Health rating (excellent/good/fair/poor)
- `vigor_score (Float32)`: Quantitative vigor assessment (0-1)
- `disease_indicators (Array(String))`: Detected diseases
- `pest_indicators (Array(String))`: Pest damage signs
- `stress_indicators (Array(String))`: Environmental stress signs
- `health_description (String)`: Detailed health analysis

## Embedding Vectors for Semantic Search

The table stores three types of embedding vectors enabling hybrid semantic search:

## Embedding Specifications

| Embedding Type | Field            | Dimensions | Source                                       |
|----------------|------------------|------------|----------------------------------------------|
| Text           | `text_embedding` | 384        | SentenceTransformer (all-MiniLM-L6-v2)       |
| Image          | `image_embedding`| 512        | CLIP (openai/clip-vit-base-patch32)          |
| Hybrid         | `hybrid_embedding`| Variable   | Combined text + image features               |

Additional semantic fields:

- `semantic_tags` (Array(String)): Agricultural keywords for tagging
- `search_context` (String): Natural language summary for search indexing