"""
Show how categorical variables are encoded in the deepfake dataset
"""
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Create data generator
datagen = ImageDataGenerator(rescale=1./255)

# Load data and show encoding
train_gen = datagen.flow_from_directory(
    'dataset/',
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary',
    shuffle=False
)

print("🏷️  CATEGORICAL ENCODING")
print("=" * 30)
print(f"Class indices: {train_gen.class_indices}")
print(f"Classes: {train_gen.classes[:10]}...")  # First 10 labels
print(f"Total samples: {train_gen.samples}")

# Show encoding mapping
print("\n📊 ENCODING MAPPING:")
for folder, label in train_gen.class_indices.items():
    print(f"  '{folder}' folder → Label {label}")

print("\n✅ Encoding is automatic - no separate file needed!")