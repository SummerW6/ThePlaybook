import torch
import torchvision.transforms as transforms
from PIL import Image
import pygame

# model = torch.load("", map_location="cpu")
# model.eval()

# transform = transforms.Compose([
#     transforms.Resize((28, 28)),
#     transforms.Grayscale(),
#     transforms.ToTensor(),
#     transforms.Normalize((0.5,), (0.5,))
# ])

# def classify(sketch):
#     raw_str = pygame.image.tostring(sketch, "RGB")
#     image = Image.frombytes("RGB", sketch.get_size(), raw_str).convert('L')

#     image_tensor = transform(image).unsqueeze(0)

#     with torch.no_grad():
#         output = model(image_tensor)
#         # predicted