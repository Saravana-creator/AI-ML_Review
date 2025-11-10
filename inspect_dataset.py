"""
Dataset Inspector - Load and analyze your deepfake dataset
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import random

def inspect_dataset():
    """Inspect dataset structure and samples"""
    
    print("📊 DATASET INSPECTION")
    print("=" * 50)
    
    # Check dataset structure
    fake_dir = "dataset/fake"
    real_dir = "dataset/real"
    
    if not os.path.exists(fake_dir) or not os.path.exists(real_dir):
        print("❌ Dataset not found! Run download_dataset.py first")
        return
    
    # Count files
    fake_count = len([f for f in os.listdir(fake_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    real_count = len([f for f in os.listdir(real_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    print(f"📁 Fake images: {fake_count:,}")
    print(f"📁 Real images: {real_count:,}")
    print(f"📁 Total images: {fake_count + real_count:,}")
    print(f"📊 Balance: {fake_count/(fake_count+real_count)*100:.1f}% fake, {real_count/(fake_count+real_count)*100:.1f}% real")
    
    # Sample file analysis
    print("\n🔍 SAMPLE FILE ANALYSIS")
    print("-" * 30)
    
    # Check fake samples
    fake_files = [f for f in os.listdir(fake_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))][:5]
    real_files = [f for f in os.listdir(real_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))][:5]
    
    print("Fake samples:")
    for f in fake_files:
        img_path = os.path.join(fake_dir, f)
        img = Image.open(img_path)
        print(f"  {f}: {img.size} pixels, {img.mode} mode")
    
    print("\nReal samples:")
    for f in real_files:
        img_path = os.path.join(real_dir, f)
        img = Image.open(img_path)
        print(f"  {f}: {img.size} pixels, {img.mode} mode")

def visualize_samples():
    """Show sample images from dataset"""
    
    print("\n🖼️  VISUALIZING SAMPLES")
    print("-" * 30)
    
    fake_dir = "dataset/fake"
    real_dir = "dataset/real"
    
    # Get random samples
    fake_files = [f for f in os.listdir(fake_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    real_files = [f for f in os.listdir(real_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Create visualization
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    fig.suptitle('Dataset Samples', fontsize=16)
    
    # Show fake samples
    for i in range(4):
        fake_file = random.choice(fake_files)
        img = Image.open(os.path.join(fake_dir, fake_file))
        axes[0, i].imshow(img)
        axes[0, i].set_title(f'FAKE\n{fake_file[:15]}...', fontsize=8)
        axes[0, i].axis('off')
    
    # Show real samples
    for i in range(4):
        real_file = random.choice(real_files)
        img = Image.open(os.path.join(real_dir, real_file))
        axes[1, i].imshow(img)
        axes[1, i].set_title(f'REAL\n{real_file[:15]}...', fontsize=8)
        axes[1, i].axis('off')
    
    plt.tight_layout()
    plt.savefig('dataset_samples.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("💾 Saved visualization as 'dataset_samples.png'")

def test_data_loading():
    """Test how ImageDataGenerator loads the data"""
    
    print("\n⚙️  TESTING DATA LOADING")
    print("-" * 30)
    
    # Create data generator (same as training)
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    
    train_gen = datagen.flow_from_directory(
        'dataset/',
        target_size=(128, 128),
        batch_size=32,
        class_mode='binary',
        subset='training',
        shuffle=False
    )
    
    val_gen = datagen.flow_from_directory(
        'dataset/',
        target_size=(128, 128),
        batch_size=32,
        class_mode='binary',
        subset='validation',
        shuffle=False
    )
    
    print(f"📊 Training samples: {train_gen.samples}")
    print(f"📊 Validation samples: {val_gen.samples}")
    print(f"📊 Class indices: {train_gen.class_indices}")
    print(f"📊 Batch size: {train_gen.batch_size}")
    
    # Get one batch
    batch_x, batch_y = next(train_gen)
    print(f"📊 Batch shape: {batch_x.shape}")
    print(f"📊 Label shape: {batch_y.shape}")
    print(f"📊 Pixel range: {batch_x.min():.3f} to {batch_x.max():.3f}")
    print(f"📊 Labels in batch: {np.unique(batch_y, return_counts=True)}")

def analyze_image_quality():
    """Analyze image quality and characteristics"""
    
    print("\n🔬 IMAGE QUALITY ANALYSIS")
    print("-" * 30)
    
    fake_dir = "dataset/fake"
    real_dir = "dataset/real"
    
    # Sample random images
    fake_files = random.sample([f for f in os.listdir(fake_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))], 100)
    real_files = random.sample([f for f in os.listdir(real_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))], 100)
    
    fake_sizes = []
    real_sizes = []
    
    # Analyze fake images
    for f in fake_files:
        img = Image.open(os.path.join(fake_dir, f))
        fake_sizes.append(img.size)
    
    # Analyze real images
    for f in real_files:
        img = Image.open(os.path.join(real_dir, f))
        real_sizes.append(img.size)
    
    # Calculate statistics
    fake_widths = [s[0] for s in fake_sizes]
    fake_heights = [s[1] for s in fake_sizes]
    real_widths = [s[0] for s in real_sizes]
    real_heights = [s[1] for s in real_sizes]
    
    print("FAKE images:")
    print(f"  Width: {np.mean(fake_widths):.0f}±{np.std(fake_widths):.0f} pixels")
    print(f"  Height: {np.mean(fake_heights):.0f}±{np.std(fake_heights):.0f} pixels")
    
    print("REAL images:")
    print(f"  Width: {np.mean(real_widths):.0f}±{np.std(real_widths):.0f} pixels")
    print(f"  Height: {np.mean(real_heights):.0f}±{np.std(real_heights):.0f} pixels")

if __name__ == "__main__":
    inspect_dataset()
    test_data_loading()
    analyze_image_quality()
    
    # Ask if user wants to see visualizations
    show_viz = input("\n🖼️  Show sample images? (y/n): ").lower().strip()
    if show_viz == 'y':
        visualize_samples()
    
    print("\n✅ Dataset inspection complete!")