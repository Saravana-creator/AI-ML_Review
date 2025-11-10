import os
import shutil

# Move fake images from real folder to fake folder
real_folder = "dataset/real"
fake_folder = "dataset/fake"

for filename in os.listdir(real_folder):
    if filename.startswith("fake_"):
        src = os.path.join(real_folder, filename)
        dst = os.path.join(fake_folder, filename)
        shutil.move(src, dst)

print("Dataset fixed - fake images moved to fake folder!")