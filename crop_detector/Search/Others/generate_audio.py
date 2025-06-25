import soundfile as sf
from kokoro import KPipeline
import numpy as np
import argparse


def generate_audio(text, voice='af_heart', output_file='/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/Search/output.wav'):
    # Initialize the Kokoro pipeline

    pipeline = KPipeline(lang_code='a')

    # Generate speech for the given text
    generator = pipeline(text, voice=voice)

    all_audio = []  # List to store all the audio segments

    for i, (gs, ps, audio) in enumerate(generator):
        print(f"Generation {i}:")
        print(f"  Ground truth: {gs}")
        print(f"  Predicted: {ps}")

        # Append the current audio segment to the list
        all_audio.append(audio)

    # Concatenate all audio segments into one
    full_audio = np.concatenate(all_audio)

    # Save the combined audio as a single .wav file
    sf.write(output_file, full_audio, 24000)
    print(f"Combined audio saved to {output_file}")


def parse_args():
    parser = argparse.ArgumentParser(description="Generate TTS audio from text.")
    parser.add_argument('--text', type=str, required=True, help="Text to be converted to speech.")
    parser.add_argument('--voice', type=str, default='af_heart', help="Voice to use for TTS.")
    parser.add_argument('--output', type=str, default='/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/Search/combined_output.wav', help="Path to save the output audio file.")
    return parser.parse_args()


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    # Print all the arguments received
    print("\nArguments received:")
    for arg, value in vars(args).items():
        print(f"{arg}: {value}")

    # Generate and save the combined audio
    generate_audio(args.text, 'af_heart','/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/Search/combined_output.wav')
