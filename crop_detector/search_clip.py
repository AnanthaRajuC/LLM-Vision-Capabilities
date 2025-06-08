import os
import torch
from PIL import Image
from torchvision import transforms
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model and processor
print("🔄 Loading CLIP model and processor...")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
print(f"✅ Model loaded on device: {device}")

# Load a single image and prepare it
def load_image(image_path):
    print(f"📷 Loading image: {image_path}")
    image = Image.open(image_path).convert("RGB")
    return image

# Load and encode all images in folder
def encode_images(folder_path):
    print(f"📂 Scanning folder: {folder_path}")
    image_embeddings = []
    image_paths = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(folder_path, filename)
            image = load_image(image_path)
            inputs = processor(images=image, return_tensors="pt").to(device)

            print(f"🔎 Encoding image: {filename}")
            with torch.no_grad():
                embedding = model.get_image_features(**inputs)
                embedding = embedding / embedding.norm(p=2, dim=-1, keepdim=True)

            image_embeddings.append(embedding.cpu().numpy()[0])  # Shape: (512,)
            image_paths.append(image_path)

    print(f"✅ Encoded {len(image_paths)} images.")
    return image_paths, np.array(image_embeddings)  # Shape: (num_images, 512)

# Encode text query
def encode_text(text):
    print(f"📝 Encoding text query: \"{text}\"")
    inputs = processor(text=[text], return_tensors="pt", padding=True).to(device)

    with torch.no_grad():
        embedding = model.get_text_features(**inputs)
        embedding = embedding / embedding.norm(p=2, dim=-1, keepdim=True)

    print("✅ Text encoded.")
    return embedding.cpu().numpy()

# Perform search
def search_images(text_query, image_folder, top_k=5, min_score=0.25):
    print(f"\n🔍 Starting image search for: '{text_query}'")
    image_paths, image_embeddings = encode_images(image_folder)
    text_embedding = encode_text(text_query)

    print("🔗 Calculating cosine similarity...")
    similarities = cosine_similarity(text_embedding, image_embeddings).flatten()
    top_indices = similarities.argsort()[::-1][:top_k]

    print(f"\n🏆 Top {top_k} matches (above score {min_score}):")
    any_good_match = False

    for idx in top_indices:
        score = similarities[idx]
        if score < min_score:
            print(f"⚠️ Ignoring low-score match: {image_paths[idx]} (score: {score:.4f})")
            continue
        print(f"→ {image_paths[idx]} (score: {score:.4f})")
        any_good_match = True

    if not any_good_match:
        print(f"❌ No relevant match found for query: '{text_query}' (all scores < {min_score})")


# Run it
if __name__ == "__main__":
    search_images(
        text_query="sugarcane",
        image_folder="/home/anantharajuc/PycharmProjects/LLM-Vision-Capabilities/crop_detector/assets/images",
        top_k=3,
        min_score=0.25
    )

