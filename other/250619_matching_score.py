import torch
import clip
import os
from PIL import Image
import torch.nn.functional as F

# Load the CLIP model and preprocessing
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/16", device='cuda:4')

image_dir = "/opt/jinhanz/data/mscoco/val2014/"

image_name = "COCO_val2014_000000347819"
captions = {
    "concrete" : 'there appears to be only a small portion of food, or perhaps most of the meal has been eaten from a plate that still holds what appears to be a cooked potato and a mixture of creamed meat and vegetables',
    # "abstract" : 'the homely lady hugs her teddy bear tightly because she cannot find a man',
}

# Load and preprocess the image
image = preprocess(Image.open(os.path.join(image_dir,f"{image_name}.jpg"))).unsqueeze(0).to(device)
print(f"Image: {image_name}.jpg")

# Prepare the text
for type, caption in captions.items():
    text = clip.tokenize([caption]).to(device)

    # Encode the image and text
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

    # Normalize the features
    image_features = F.normalize(image_features, dim=-1)
    text_features = F.normalize(text_features, dim=-1)

    # Compute cosine similarity
    similarity = (image_features @ text_features.T).item()
    print(f"{type}: {similarity:.4f} {caption}")