"""
Dataset Cleaner - Handle missing/corrupted images and data quality issues
"""
import os
import shutil
from PIL import Image
import numpy as np

def clean_corrupted_images():
    """Remove corrupted or unreadable images"""
    
    print("🧹 CLEANING CORRUPTED IMAGES")
    print("=" * 40)
    
    corrupted_count = 0
    total_count = 0
    
    for folder in ['dataset/fake', 'dataset/real']:
        if not os.path.exists(folder):
            continue
            
        print(f"\n📁 Checking {folder}...")
        
        for filename in os.listdir(folder):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            filepath = os.path.join(folder, filename)
            total_count += 1
            
            try:
                # Try to open and verify image
                with Image.open(filepath) as img:
                    img.verify()  # Verify image integrity
                    
                # Reopen for size check (verify() closes the image)
                with Image.open(filepath) as img:
                    width, height = img.size
                    
                    # Remove images that are too small
                    if width < 32 or height < 32:
                        print(f"  ❌ Removing tiny image: {filename} ({width}x{height})")
                        os.remove(filepath)
                        corrupted_count += 1
                        continue
                    
                    # Remove images with unusual aspect ratios
                    aspect_ratio = max(width, height) / min(width, height)
                    if aspect_ratio > 10:  # Very elongated images
                        print(f"  ❌ Removing elongated image: {filename} (ratio: {aspect_ratio:.1f})")
                        os.remove(filepath)
                        corrupted_count += 1
                        continue
                        
            except Exception as e:
                print(f"  ❌ Removing corrupted image: {filename} - {str(e)}")
                os.remove(filepath)
                corrupted_count += 1
    
    print(f"\n✅ Cleaned {corrupted_count} corrupted images out of {total_count} total")
    return corrupted_count

def fix_mislabeled_images():
    """Move mislabeled images to correct folders"""
    
    print("\n🔧 FIXING MISLABELED IMAGES")
    print("=" * 40)
    
    moved_count = 0
    
    # Check for fake images in real folder
    real_folder = "dataset/real"
    fake_folder = "dataset/fake"
    
    if os.path.exists(real_folder):
        for filename in os.listdir(real_folder):
            if filename.lower().startswith("fake_"):
                src = os.path.join(real_folder, filename)
                dst = os.path.join(fake_folder, filename)
                shutil.move(src, dst)
                print(f"  📁 Moved {filename} to fake folder")
                moved_count += 1
    
    # Check for real images in fake folder
    if os.path.exists(fake_folder):
        for filename in os.listdir(fake_folder):
            if filename.lower().startswith("real_"):
                src = os.path.join(fake_folder, filename)
                dst = os.path.join(real_folder, filename)
                shutil.move(src, dst)
                print(f"  📁 Moved {filename} to real folder")
                moved_count += 1
    
    print(f"✅ Fixed {moved_count} mislabeled images")
    return moved_count

def remove_duplicates():
    """Remove duplicate images"""
    
    print("\n🔍 REMOVING DUPLICATES")
    print("=" * 40)
    
    def get_image_hash(filepath):
        """Get simple hash of image for duplicate detection"""
        try:
            with Image.open(filepath) as img:
                # Resize to small size and convert to grayscale for comparison
                img = img.resize((8, 8)).convert('L')
                return hash(tuple(np.array(img).flatten()))
        except:
            return None
    
    removed_count = 0
    seen_hashes = set()
    
    for folder in ['dataset/fake', 'dataset/real']:
        if not os.path.exists(folder):
            continue
            
        print(f"\n📁 Checking duplicates in {folder}...")
        
        for filename in os.listdir(folder):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            filepath = os.path.join(folder, filename)
            img_hash = get_image_hash(filepath)
            
            if img_hash is None:
                continue
                
            if img_hash in seen_hashes:
                print(f"  ❌ Removing duplicate: {filename}")
                os.remove(filepath)
                removed_count += 1
            else:
                seen_hashes.add(img_hash)
    
    print(f"✅ Removed {removed_count} duplicate images")
    return removed_count

def balance_dataset():
    """Balance the number of fake and real images"""
    
    print("\n⚖️  BALANCING DATASET")
    print("=" * 40)
    
    fake_folder = "dataset/fake"
    real_folder = "dataset/real"
    
    fake_count = len([f for f in os.listdir(fake_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    real_count = len([f for f in os.listdir(real_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    print(f"📊 Fake images: {fake_count}")
    print(f"📊 Real images: {real_count}")
    
    if abs(fake_count - real_count) > 1000:  # Significant imbalance
        target_count = min(fake_count, real_count)
        print(f"🎯 Balancing to {target_count} images each")
        
        # Remove excess images from the larger class
        if fake_count > real_count:
            excess_folder = fake_folder
            excess_count = fake_count - target_count
        else:
            excess_folder = real_folder
            excess_count = real_count - target_count
        
        files = [f for f in os.listdir(excess_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        files_to_remove = files[:excess_count]
        
        for filename in files_to_remove:
            os.remove(os.path.join(excess_folder, filename))
        
        print(f"✅ Removed {excess_count} excess images")
    else:
        print("✅ Dataset is already balanced")

def create_backup():
    """Create backup of original dataset"""
    
    if os.path.exists("dataset_backup"):
        print("📦 Backup already exists")
        return
    
    print("📦 Creating backup...")
    shutil.copytree("dataset", "dataset_backup")
    print("✅ Backup created as 'dataset_backup'")

if __name__ == "__main__":
    print("🧹 DATASET CLEANING UTILITY")
    print("=" * 50)
    
    # Create backup first
    create_backup()
    
    # Run all cleaning operations
    clean_corrupted_images()
    fix_mislabeled_images()
    remove_duplicates()
    balance_dataset()
    
    print("\n🎉 DATASET CLEANING COMPLETE!")
    print("=" * 50)
    
    # Final statistics
    fake_count = len([f for f in os.listdir("dataset/fake") if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    real_count = len([f for f in os.listdir("dataset/real") if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    print(f"📊 Final dataset:")
    print(f"   Fake images: {fake_count:,}")
    print(f"   Real images: {real_count:,}")
    print(f"   Total: {fake_count + real_count:,}")
    print(f"   Balance: {fake_count/(fake_count+real_count)*100:.1f}% fake")