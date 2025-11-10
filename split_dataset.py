import os
import shutil
import random

# Create train/test structure
for split in ['train', 'test']:
    os.makedirs(f'dataset/{split}/real', exist_ok=True)
    os.makedirs(f'dataset/{split}/fake', exist_ok=True)

# Split real images (80% train, 20% test)
real_files = os.listdir('dataset/real')
random.shuffle(real_files)
split_idx = int(0.8 * len(real_files))

for i, file in enumerate(real_files):
    src = f'dataset/real/{file}'
    dst = f'dataset/{"train" if i < split_idx else "test"}/real/{file}'
    shutil.move(src, dst)

# Split fake images
fake_files = os.listdir('dataset/fake')
random.shuffle(fake_files)
split_idx = int(0.8 * len(fake_files))

for i, file in enumerate(fake_files):
    src = f'dataset/fake/{file}'
    dst = f'dataset/{"train" if i < split_idx else "test"}/fake/{file}'
    shutil.move(src, dst)

print("Dataset split into train/test folders")