import os
import tempfile
import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
import ollama

from CropSemanticSearch import semantic_crop_search
from crop_detector.Search.Others.kokoroTTS import generate_audio

def record_audio(duration=5, samplerate=16000):
    print("🎙️ Speak now...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        wav.write(temp_audio.name, samplerate, recording)
        print("✅ Recorded:", temp_audio.name)
        return temp_audio.name

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    print("📝 Transcribed Text:", result["text"])
    return result["text"]

def detect_language(text):
    lang_code = "en"
    print("🌐 Language forced to:", lang_code)
    return lang_code

def get_qwen_response(prompt):
    response = ollama.chat(
        model="qwen:7b-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response["message"]["content"].strip()
    print("🤖 Qwen says:", reply)
    return reply

def run_voice_chatbot():
    audio_path = record_audio(duration=6)
    user_text = transcribe_audio(audio_path)
    lang = detect_language(user_text)
    #reply = get_qwen_response(user_text)
    os.remove(audio_path)

    if not user_text.strip():
        print("❗ No speech detected.")
        return

    # 🌾 Run semantic search
    try:
        results = semantic_crop_search(user_text, top_k=3)
        print("\n🔍 Top Matches:")
        for idx, row in enumerate(results, 1):
            print(f"\n📌 Result #{idx}")
            print(f"Crop: {row[0]}")
            print(f"Confidence: {row[1]}")
            print(f"Context: {row[2]}")
            print(f"Description: {row[3]}")

        # 🗣️ TTS for the context of result #1
        if results:
            top_context = results[0][2]  # row[2] is the "Context"
            generate_audio(
                text=top_context,
                voice="af_heart",
                output_file="/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/Search/context_speech.wav"
            )
    except Exception as e:
        print("❌ Search failed:", e)

if __name__ == "__main__":
    run_voice_chatbot()
