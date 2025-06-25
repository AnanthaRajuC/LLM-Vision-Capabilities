1. Model and Image Setup

- Reads the model name and image path from CLI args (defaults if none).
- Loads crop detection prompt from assets/prompts/.

---

2. Ollama Check

- Checks if Ollama is running at http://localhost:11434.
- If not, exits with error.

---

3. Image → Base64

- Uses encode_image() to convert the image to base64 (JPEG format).

---

4. Send Image to Qwen 2.5 Vision

- Sends image + prompt to call_model()
- Qwen returns structured JSON with crop info:
  - Crop type
  - Alternate names
  - Color, confidence
  - Growth stage, health, environment, etc.

--- 

5. Parse + Enrich Response

- Parses JSON
- Adds startDateTime, endDateTime, duration

--- 

6. Save Result to ClickHouse

- If PROMPT_TYPE == "basic", saves a short summary to crop_detection table.
- Else (default: "detailed"), saves full result to crop_analysis table.

---

🧠 Outcome of Running main.py

| Output                  | Description                                                   |
| ----------------------- | ------------------------------------------------------------- |
| `result_json` printed   | Human-readable crop analysis                                  |
| ✅ ClickHouse (2 tables) | `crop_analysis` (detailed info), `image_embeddings` (vectors) |
| ⏱ Timings               | Embedded in metadata (`duration`, `timestamps`)               |

---

📂 Result in ClickHouse

You will now have:

- crop_analysis → info like "crop": "rice", "confidence": 0.92, etc.
- image_embeddings → same image’s vector representation for semantic search

---