## Search System

Purpose and Scope
This document covers the search capabilities of the LLM Vision Capabilities system, specifically the text-based semantic search and voice-activated search functionality. The search system enables querying of previously analyzed crop data using natural language queries through two modalities: direct text input and voice commands that are transcribed to text.

## System Overview

The search system consists of two primary components that both leverage semantic similarity matching against stored crop analysis results:

| Component     | File               | Input Method      | Processing                                               |
|---------------|--------------------|-------------------|----------------------------------------------------------|
| Text Search   | `CropSemanticSearch.py` | Direct text query | SentenceTransformer encoding → Vector similarity         |
| Voice Search  | `speech_input.py`      | Audio recording    | Whisper transcription → Text search pipeline             |

Both search methods query the same ClickHouse database tables using cosine distance similarity against pre-computed embeddings.

## Text-Based Semantic Search

The `semantic_crop_search()` function in `crop_detector/Search/CropSemanticSearch.py` implements the core text search logic. It encodes the input query using a pre-loaded SentenceTransformer model and performs cosine distance similarity search against stored embeddings.

### Key Implementation Details:

- **Model**: `sentence-transformers/all-MiniLM-L6-v2` produces 384-dimensional embeddings
- **Similarity Metric**: Cosine distance via ClickHouse's `cosineDistance()` function
- **Embedding Options**: Can search against `text_embedding` or `hybrid_embedding` columns
- **Result Limit**: Configurable `top_k` parameter (default 5)

## Voice-Based Search

The voice search functionality in `crop_detector/Search/speech_input.py` orchestrates the complete voice-to-search pipeline through the `run_voice_chatbot()` function.

### Voice Processing Components:

| Function               | Purpose           | Key Parameters                          |
|------------------------|-------------------|------------------------------------------|
| `record_audio()`       | Audio capture     | `duration=5s`, `samplerate=16000`        |
| `transcribe_audio()`   | Speech-to-text    | Whisper `"base"` model                   |
| `detect_language()`    | Language detection| Forced to `"en"`                         |
| `semantic_crop_search()` | Text search     | `top_k=3` results                        |

## Database Integration

The search system integrates with ClickHouse through the clickhouse_connect client, querying the crop analysis results table:

### Search Query Execution

The core search query uses ClickHouse's vector similarity functions:

~~~sql
SELECT crop, confidence, search_context, overall_description
FROM {CROP_ANALYSIS_TABLE}
ORDER BY cosineDistance({embedding_col}, %(embedding)s) ASC
LIMIT %(top_k)s
~~~

**Query Parameters:**

- `embedding_col`: Either text_embedding or hybrid_embedding
- `embedding`: Query vector (384 dimensions for text)
- `top_k`: Maximum number of results to return

The `use_hybrid` parameter in `semantic_crop_search()` determines whether to search against text-only embeddings or hybrid image-text embeddings stored during the analysis phase.