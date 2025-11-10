"""
Advanced Transfer Learning Model
- EfficientNet backbone
- Two-phase training
- Enhanced data augmentation
"""
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

def create_advanced_model():
    """Create EfficientNet-based model"""
    base_model = EfficientNetB0(
        weights='imagenet',
        include_top=False,
        input_shape=(128, 128, 3)
    )
    
    base_model.trainable = False
    
    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    return model, base_model

# Enhanced data augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    validation_split=0.2
)

# Data generators
train_gen = datagen.flow_from_directory(
    '../dataset/',
    target_size=(128, 128),
    batch_size=16,
    class_mode='binary',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    '../dataset/',
    target_size=(128, 128),
    batch_size=16,
    class_mode='binary',
    subset='validation'
)

# Create model
print("🏗️  Creating Advanced Model...")
model, base_model = create_advanced_model()
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Callbacks
callbacks = [
    EarlyStopping(patience=10, restore_best_weights=True),
    ReduceLROnPlateau(patience=5, factor=0.2, min_lr=1e-7),
    ModelCheckpoint('../backend/model/best_model.h5', save_best_only=True)
]

# Phase 1: Transfer Learning
print("🚀 Phase 1: Transfer Learning (30 epochs)")
history1 = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=30,
    callbacks=callbacks
)

# Phase 2: Fine-tuning
print("🔧 Phase 2: Fine-tuning (20 epochs)")
base_model.trainable = True
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

history2 = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=20,
    callbacks=callbacks
)

# Save final model
model.save('../backend/model/deepfake_model_advanced.h5')
print("✅ Advanced model saved as deepfake_model_advanced.h5")