import soundfile as sf
from kokoro import KPipeline
import numpy as np


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


if __name__ == "__main__":
    text = '''
    “Everything you are against weakens you. Everything you are for empowers you.”
    '''

    # Set the voice and output file path
    voice = 'af_heart'  # Example voice, change as needed
    output_file = '/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/Search/combined_output.wav'  # Set your desired output path

    # Generate and save the combined audio
    generate_audio(text, voice, output_file)
