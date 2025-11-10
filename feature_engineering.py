"""
STEP 4: Feature Scaling + PCA for Image Data
Traditional ML approach with extracted features
"""
import numpy as np
import os
from PIL import Image
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

def extract_image_features(img_path, size=(64, 64)):
    """Extract basic features from image"""
    try:
        img = Image.open(img_path).convert('RGB')
        img = img.resize(size)
        
        # Convert to array and flatten
        img_array = np.array(img)
        
        # Basic features
        features = []
        
        # 1. Pixel intensities (flattened)
        features.extend(img_array.flatten())
        
        # 2. Color statistics
        for channel in range(3):  # RGB
            channel_data = img_array[:, :, channel]
            features.extend([
                np.mean(channel_data),
                np.std(channel_data),
                np.min(channel_data),
                np.max(channel_data)
            ])
        
        # 3. Texture features (simple)
        gray = np.mean(img_array, axis=2)
        features.extend([
            np.mean(np.gradient(gray)[0]),  # Horizontal gradient
            np.mean(np.gradient(gray)[1]),  # Vertical gradient
        ])
        
        return np.array(features)
    
    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return None

def load_and_extract_features():
    """Load images and extract features"""
    
    print("🔍 EXTRACTING FEATURES FROM IMAGES")
    print("=" * 40)
    
    features = []
    labels = []
    
    # Process fake images
    fake_dir = "dataset/fake"
    fake_files = [f for f in os.listdir(fake_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))][:1000]  # Limit for speed
    
    print(f"Processing {len(fake_files)} fake images...")
    for i, filename in enumerate(fake_files):
        if i % 100 == 0:
            print(f"  Processed {i}/{len(fake_files)} fake images")
        
        img_features = extract_image_features(os.path.join(fake_dir, filename))
        if img_features is not None:
            features.append(img_features)
            labels.append(0)  # Fake = 0
    
    # Process real images
    real_dir = "dataset/real"
    real_files = [f for f in os.listdir(real_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))][:1000]  # Limit for speed
    
    print(f"Processing {len(real_files)} real images...")
    for i, filename in enumerate(real_files):
        if i % 100 == 0:
            print(f"  Processed {i}/{len(real_files)} real images")
        
        img_features = extract_image_features(os.path.join(real_dir, filename))
        if img_features is not None:
            features.append(img_features)
            labels.append(1)  # Real = 1
    
    return np.array(features), np.array(labels)

def apply_scaling_and_pca(X, y, n_components=100):
    """Apply feature scaling and PCA"""
    
    print(f"\n⚖️  FEATURE SCALING + PCA")
    print("=" * 40)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"📊 Original feature dimensions: {X_train.shape[1]}")
    
    # 1. Feature Scaling
    print("🔧 Applying StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 2. PCA
    print(f"🔧 Applying PCA (reducing to {n_components} components)...")
    pca = PCA(n_components=n_components)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    
    print(f"📊 Reduced feature dimensions: {X_train_pca.shape[1]}")
    print(f"📊 Explained variance ratio: {pca.explained_variance_ratio_.sum():.3f}")
    
    # Save preprocessing objects
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(pca, 'pca.pkl')
    print("💾 Saved scaler.pkl and pca.pkl")
    
    return X_train_pca, X_test_pca, y_train, y_test, scaler, pca

def train_traditional_ml(X_train, X_test, y_train, y_test):
    """Train traditional ML model on processed features"""
    
    print(f"\n🤖 TRAINING TRADITIONAL ML MODEL")
    print("=" * 40)
    
    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Predictions
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"📊 Accuracy: {accuracy:.3f}")
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Fake', 'Real']))
    
    # Save model
    joblib.dump(rf, 'traditional_model.pkl')
    print("💾 Saved traditional_model.pkl")
    
    return rf

def predict_with_traditional_ml(img_path):
    """Predict using traditional ML pipeline"""
    
    # Load preprocessing objects
    scaler = joblib.load('scaler.pkl')
    pca = joblib.load('pca.pkl')
    model = joblib.load('traditional_model.pkl')
    
    # Extract features
    features = extract_image_features(img_path)
    if features is None:
        return None
    
    # Preprocess
    features_scaled = scaler.transform([features])
    features_pca = pca.transform(features_scaled)
    
    # Predict
    prediction = model.predict(features_pca)[0]
    probability = model.predict_proba(features_pca)[0]
    
    return {
        'prediction': 'Real' if prediction == 1 else 'Fake',
        'confidence': max(probability)
    }

if __name__ == "__main__":
    print("🔬 TRADITIONAL ML APPROACH WITH FEATURE ENGINEERING")
    print("=" * 60)
    
    # Step 1: Extract features
    X, y = load_and_extract_features()
    
    # Step 2: Apply scaling and PCA
    X_train_pca, X_test_pca, y_train, y_test, scaler, pca = apply_scaling_and_pca(X, y)
    
    # Step 3: Train traditional ML model
    model = train_traditional_ml(X_train_pca, X_test_pca, y_train, y_test)
    
    print("\n✅ Traditional ML pipeline complete!")
    print("📁 Files created: scaler.pkl, pca.pkl, traditional_model.pkl")
    
    # Test on external image
    test_img = r"C:\Users\Saravana Perumal\Downloads\person1_fake.jpg"
    if os.path.exists(test_img):
        result = predict_with_traditional_ml(test_img)
        print(f"\n🧪 Test prediction: {result}")