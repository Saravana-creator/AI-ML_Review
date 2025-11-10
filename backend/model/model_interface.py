import sys
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

import os

# Auto-select best available model
model_priority = [
    'backend/model/deepfake_model_advanced.h5',
    'backend/model/deepfake_model_basic.h5', 
    'backend/model/deepfake_model_quick.h5',
    'backend/model/deepfake_model.h5'
]

model_path = None
for path in model_priority:
    if os.path.exists(path):
        model_path = path
        break

if not model_path:
    raise FileNotFoundError("No trained model found. Please train a model first.")

model = load_model(model_path)
print(f"Using model: {model_path}")

def predict(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    pred = model.predict(img_array, verbose=0)[0][0]
    return "Real" if pred > 0.5 else "Fake", float(pred)

if __name__ == "__main__":
    img_path = sys.argv[1]
    label, confidence = predict(img_path)
    print(f"{label},{confidence}")
