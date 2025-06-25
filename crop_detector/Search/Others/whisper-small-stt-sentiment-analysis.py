import os
import tempfile
import sounddevice as sd
import scipy.io.wavfile as wav
import torch
import json
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

def record_audio(duration=6, samplerate=16000):
    print("🎙️ Speak now...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        wav.write(temp_audio.name, samplerate, recording)
        print("✅ Recorded:", temp_audio.name)
        return temp_audio.name

def transcribe_and_analyze(audio_path):
    device = "cpu"
    torch_dtype = torch.float32
    model_id = "openai/whisper-small"  # use a multilingual model

    print("📥 Loading Whisper model...")
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True
    ).to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

    print("🧠 Detecting language and transcribing...")
    resultTranscription = pipe(audio_path, generate_kwargs={"task": "transcribe"})
    detected_lang = resultTranscription.get("language", "unknown")
    print(f"🌐 Detected Language: {detected_lang}")
    print(f"📝 Transcription: {resultTranscription['text']}")

    print("🌍 Translating to English...")
    resultTranslation = pipe(audio_path, generate_kwargs={"task": "translate"})
    print(f"🔠 Translation: {resultTranslation['text']}")

    print("🔎 Running sentiment analysis...")
    classifier = pipeline("sentiment-analysis",
                          model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
                          revision="af0f99b")
    resultClassifier = classifier(resultTranslation["text"])
    print("📊 Sentiment:", resultClassifier)

    data = {
        "detectedLanguage": detected_lang,
        "resultTranscription": resultTranscription,
        "resultTranslation": resultTranslation,
        "resultClassifier": resultClassifier
    }

    print("\n📦 JSON Output:")
    print(json.dumps(data, indent=2))

    return data

def run_voice_pipeline():
    audio_path = record_audio()
    try:
        transcribe_and_analyze(audio_path)
    finally:
        os.remove(audio_path)
        print("🧹 Temp file deleted.")

if __name__ == "__main__":
    run_voice_pipeline()
