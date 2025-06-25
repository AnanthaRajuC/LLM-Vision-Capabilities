import os
import tempfile
import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
import ollama
import subprocess
import generate_audio

# 🎙️ Record audio
def record_audio(duration=5, samplerate=16000):
    print("🎙️ Speak now...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        wav.write(temp_audio.name, samplerate, recording)
        print("✅ Recorded:", temp_audio.name)
        return temp_audio.name

# 📝 Transcribe audio using Whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # offline
    result = model.transcribe(audio_path, language=None)
    print(f"📝 Transcribed Text ({result['language']}):", result["text"])
    return result["text"], result["language"]

# 🌐 Map Whisper language to Coqui-compatible code
def map_language_code(lang):
    return {
        "en": "en",
        "hi": "hi",
        "kn": "kn"
    }.get(lang, "en")


# 🔊 Speak text using Coqui TTS (offline)
def speak_offline(text, lang_code="af_heart",output_path='/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/Search/combined_output.wav'):
    print("------------------------------------------------------")
    print(text)
    try:
        # Define the path for the output file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            output_path = temp_audio.name

        # Call the generate_audio.py script via subprocess, passing the text, voice, and output path
        command = [
            "python", "generate_audio.py",  # Call the script
            "--text", text,  # The text to be converted to speech
            "--voice", "af_heart",  # Set the voice as 'af_heart'
            "--output",
            "/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/Search/combined_output.wav"
            # Path to save the output
        ]

        # Run the command
        subprocess.run(command)

        # Play the generated audio
        subprocess.run(["aplay", output_path])

        # Remove the temporary audio file after playing
        os.remove(output_path)

    except Exception as e:
        print("❌ Offline TTS failed:", e)

# 🤖 Get response from Qwen (via Ollama, offline)
def get_qwen_response(prompt):
    response = ollama.chat(
        model="qwen3:1.7b",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response["message"]["content"].strip()
    print("🤖 Qwen says:", reply)
    return reply

# 🧠 Main chatbot loop
def run_voice_chatbot():
    audio_path = record_audio(duration=6)
    user_text, lang_code = transcribe_audio(audio_path)
    os.remove(audio_path)

    if not user_text.strip():
        print("❗ No speech detected.")
        return

    tts_lang = map_language_code(lang_code)
    reply = get_qwen_response(user_text)
    speak_offline(reply, lang_code=tts_lang,output_path='/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/Search/combined_output.wav')

if __name__ == "__main__":
    run_voice_chatbot()
