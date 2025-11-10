import kagglehub
import os
import shutil

# Download deepfake dataset from Kaggle
dataset_path = kagglehub.dataset_download("manjilkarki/deepfake-and-real-images")
print(f"Dataset downloaded to: {dataset_path}")

# Create dataset structure
os.makedirs("dataset/real", exist_ok=True)
os.makedirs("dataset/fake", exist_ok=True)

# Move files to proper structure
for root, dirs, files in os.walk(dataset_path):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            src = os.path.join(root, file)
            if 'real_' in file.lower():
                dst = os.path.join("dataset/real", file)
            elif 'fake_' in file.lower():
                dst = os.path.join("dataset/fake", file)
            shutil.copy2(src, dst)

print("✅ Dataset organized successfully!")