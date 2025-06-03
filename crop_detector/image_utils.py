from PIL import Image   # Import the Image class from the PIL library to work with images
from io import BytesIO  # Import BytesIO to handle in-memory binary streams
import base64           # Import base64 to encode binary data to base64 format


# Define a function to encode an image to a base64 string
def encode_image(image_path: str) -> str:
    # Inform the user that encoding has started
    print(f"Encoding image")

    # Open the image using PIL's Image class
    with Image.open(image_path) as img:
        # Create an in-memory binary stream to hold the image data
        buffered = BytesIO()

        # Save the image to the binary stream in JPEG format
        img.save(buffered, format="JPEG")

        # Inform the user that encoding is done
        print("Image encoding will start now.\n")

        # Encode the binary data to a base64 string and return it
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
