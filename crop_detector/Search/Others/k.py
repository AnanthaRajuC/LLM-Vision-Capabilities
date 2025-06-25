import soundfile as sf
from kokoro import KPipeline


def generate_audio(text, voice='af_heart', output_dir='/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/Search'):
    # Initialize the Kokoro pipeline
    pipeline = KPipeline(lang_code='a')

    # Generate speech for the given text
    generator = pipeline(text, voice=voice)

    for i, (gs, ps, audio) in enumerate(generator):
        print(f"Generation {i}:")
        print(f"  Ground truth: {gs}")
        print(f"  Predicted: {ps}")

        # Save the audio as a .wav file
        output_file = f'{output_dir}/{i}.wav'
        sf.write(output_file, audio, 24000)
        print(f"Audio saved to {output_file}")


if __name__ == "__main__":
    text = '''
    [Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters.
    Despite its lightweight architecture, it delivers comparable quality to larger models
    while being significantly faster and more cost-efficient. With Apache-licensed weights,
    [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects.
    '''

    # Set the voice and output directory
    voice = 'af_heart'  # Example voice, change as needed
    output_dir = '/crop_detector/Search'  # Make sure this folder exists or create it

    # Generate and save the audio
    generate_audio(text, voice, output_dir)
