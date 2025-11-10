import os
import requests
from pathlib import Path

# Create directories
os.makedirs('dataset_enhanced/fake', exist_ok=True)
os.makedirs('dataset_enhanced/real', exist_ok=True)

# Download diverse deepfake datasets
datasets = [
    {
        'name': 'FaceForensics++',
        'url': 'https://github.com/ondyari/FaceForensics/releases/download/v1.0/FaceForensics++.zip',
        'type': 'comprehensive'
    },
    {
        'name': 'DFDC',
        'url': 'https://www.kaggle.com/c/deepfake-detection-challenge/data',
        'type': 'competition'
    }
]

print("📥 Enhanced Dataset Sources:")
print("1. FaceForensics++ - Multiple AI methods (DeepFakes, Face2Face, FaceSwap, NeuralTextures)")
print("2. DFDC - Facebook's Deepfake Detection Challenge dataset")
print("3. CelebDF - Celebrity deepfakes")
print("\n⚠️  Manual download required for these datasets due to size/licensing")
print("\nAlternative: Use existing dataset with better training")