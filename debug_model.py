import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load model
model = load_model('backend/model/deepfake_model.h5')

# Test the problematic image
def test_image(img_path):
    print(f"\n=== Testing: {img_path} ===")
    
    # Load and preprocess image
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Get raw prediction
    pred = model.predict(img_array, verbose=0)[0][0]
    
    print(f"Raw prediction value: {pred}")
    print(f"Interpreted as: {'Real' if pred > 0.5 else 'Fake'}")
    print(f"Confidence: {pred * 100:.1f}%")
    
    return pred

# Check training data class mapping
print("=== Checking Training Data ===")
datagen = ImageDataGenerator(rescale=1./255)
train_gen = datagen.flow_from_directory(
    'dataset/',
    target_size=(128, 128),
    batch_size=1,
    class_mode='binary',
    shuffle=False
)
print("Class indices:", train_gen.class_indices)

# Test the specific image
test_image(r"C:\Users\Saravana Perumal\Downloads\person1_fake.jpg")

# Test a few images from your dataset
import os
fake_dir = 'dataset/fake'
real_dir = 'dataset/real'

if os.path.exists(fake_dir):
    fake_files = os.listdir(fake_dir)[:2]
    for f in fake_files:
        test_image(os.path.join(fake_dir, f))

if os.path.exists(real_dir):
    real_files = os.listdir(real_dir)[:2]
    for f in real_files:
        test_image(os.path.join(real_dir, f))