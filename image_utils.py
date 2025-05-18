from PIL import Image
from io import BytesIO
import base64

def encode_image(image_path: str) -> str:
    print(f"Encoding image")
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        print("Image encoding complete.\n")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
