import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import os

# 1. Setup Device (Optimized for Mac M-series)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

# 2. Data Augmentation and Loading
data_transforms = transforms.Compose([
    transforms.Resize(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# UPDATE THIS PATH based on your 'find' command result
data_dir = 'lc25000_data/lung_colon_image_set/lung_image_sets'

if not os.path.exists(data_dir):
    print(f"Error: Data directory {data_dir} not found. Check your path!")
    exit()

dataset = datasets.ImageFolder(data_dir, transform=data_transforms)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# 3. Model Surgery
model = models.resnet18(weights='IMAGENET1K_V1')
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 3) # 3 classes: aca, n, scc
model = model.to(device)

# 4. Loss and Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 5. Training Loop (Simple 2-epoch demo)
print("Starting Training...")
model.train()
for epoch in range(2):
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    print(f"Epoch {epoch+1} - Loss: {running_loss/len(train_loader):.4f}")

# 6. Save the Brain
torch.save(model.state_dict(), 'lung_triage_v1.pth')
print("Model saved as lung_triage_v1.pth")
