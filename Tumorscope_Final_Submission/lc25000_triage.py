import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import os
import sys

class LungClassifier:
    def __init__(self, model_path='lung_triage_v1.pth'):
        self.model = models.resnet18(weights=None)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 3)
        
        # Explicit mapping to match ImageFolder default alphabetical order
        self.classes = ['LUNG_ACA', 'LUNG_N', 'LUNG_SCC']
        
        if os.path.exists(model_path):
            # Map to CPU or MPS depending on availability
            device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
            self.model.load_state_dict(torch.load(model_path, map_location=device))
            print(f"[INFO] Loaded weights from {model_path}")
        else:
            print("[WARNING] No weights found. Using random initialization.")
        
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, tile_path):
        img = Image.open(tile_path).convert('RGB')
        img_t = self.transform(img).unsqueeze(0)
        
        with torch.no_grad():
            outputs = self.model(img_t)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            conf, predicted = torch.max(probabilities, 1)
            label = self.classes[predicted.item()]
        
        return label, conf.item()

def run_integrated_pipeline(tile_path):
    print(f"\n[TRIAGE] Scanning: {tile_path}")
    triage = LungClassifier()
    diagnosis, confidence = triage.predict(tile_path)
    
    print(f"PREDICTION: {diagnosis} ({confidence*100:.2f}% confidence)")
    
    if diagnosis == 'LUNG_N':
        print("STATUS: Cleared. No malignancy detected.")
    else:
        print("STATUS: MALIGNANCY DETECTED. Proceeding to Spatial Suite...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_integrated_pipeline(sys.argv[1])
    else:
        print("Usage: python3 lc25000_triage.py <path_to_image>")
