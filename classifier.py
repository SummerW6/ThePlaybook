import torch
from torchvision import transforms
import pygame
from PIL import Image
from model import SimpleCNN

model = SimpleCNN()
model.load_state_dict(torch.load("model.pth", map_location="cpu"))

model.eval()

labels = {index: label for label, index in {'asterisk': 0, 'five-circled': 1, 'four-circled': 2, 'one-circled': 3, 'three-circled': 4, 'two-circled': 5}.items()}

transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.Grayscale(),
    transforms.ToTensor(),
])

def classify(surface):
    raw = pygame.image.tostring(surface, 'RGB')
    img = Image.frombytes('RGB', surface.get_size(), raw)

    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(tensor)
        pred = output.argmax(dim=1).item()
    
    return labels[pred]