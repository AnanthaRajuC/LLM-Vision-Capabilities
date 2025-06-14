import os

from clickhouse_connect import get_client
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# --- Initialize Model and ClickHouse Client ---
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load environment variables
load_dotenv()

# ClickHouse configuration from .env
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_PORT_HTTP = int(os.getenv("CLICKHOUSE_PORT_HTTP"))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE")
CROP_ANALYSIS_TABLE = os.getenv("CLICKHOUSE_CROP_ANALYSIS_TABLE")

client = get_client(
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_PORT_HTTP,
    username=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD,
    database=CLICKHOUSE_DATABASE
)


def semantic_crop_search(query_text: str, top_k: int = 5, use_hybrid: bool = False):
    """
    Search for similar crop descriptions using vector similarity in ClickHouse.
    Uses clickhouse_connect (HTTP client).
    """
    # --- Get embedding ---
    query_embedding = model.encode(query_text).tolist()

    expected_dim = model.get_sentence_embedding_dimension()
    if len(query_embedding) != expected_dim:
        raise ValueError(f"❌ Embedding size mismatch: expected {expected_dim}, got {len(query_embedding)}")

    # --- Choose column based on flag ---
    embedding_col = "hybrid_embedding" if use_hybrid else "text_embedding"

    # --- SQL Query ---
    sql = f"""
        SELECT crop, confidence, search_context, overall_description
        FROM {CROP_ANALYSIS_TABLE}
        ORDER BY cosineDistance({embedding_col}, %(embedding)s) ASC
        LIMIT %(top_k)s
    """

    # --- Execute Query ---
    try:
        result = client.query(sql, parameters={'embedding': query_embedding, 'top_k': top_k})
    except Exception as e:
        raise RuntimeError(f"❌ ClickHouse query failed: {e}")

    return result.result_rows  # or result.named_results for dicts

# --- Example Run ---
if __name__ == "__main__":
    query = "sugarcane"
    try:
        results = semantic_crop_search(query, top_k=3)
        for idx, row in enumerate(results, 1):
            print(f"\n🔍 Result #{idx}")
            print(f"Crop: {row[0]}")
            print(f"Confidence: {row[1]}")
            print(f"Context: {row[2]}")
            print(f"Description: {row[3]}")
    except Exception as err:
        print(err)
