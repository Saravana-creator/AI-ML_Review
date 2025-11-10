import sys
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model = load_model('model/deepfake_model.h5')

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