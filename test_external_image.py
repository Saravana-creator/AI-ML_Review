from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image, ImageEnhance

def preprocess_external_image(img_path):
    # Load image
    img = Image.open(img_path)
    
    # Enhance contrast (helps with external images)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    # Resize and normalize
    img = img.resize((128, 128))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

# Test with enhanced preprocessing
model = load_model('backend/model/deepfake_model.h5')
img_array = preprocess_external_image(r"C:\Users\Saravana Perumal\Downloads\person1_fake.jpg")
pred = model.predict(img_array, verbose=0)[0][0]

print(f"Enhanced prediction: {pred:.4f}")
print(f"Result: {'Real' if pred > 0.5 else 'Fake'}")
print(f"Confidence: {pred * 100:.1f}%")