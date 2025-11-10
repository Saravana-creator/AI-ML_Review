"""
Model Accuracy Measurement Tool
Run this in terminal to measure model performance on test images
"""
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import glob

def load_test_images(test_dir, target_size=(128, 128)):
    """Load test images and their true labels"""
    images = []
    labels = []
    
    # Load fake images (label = 0)
    fake_dir = os.path.join(test_dir, 'fake')
    if os.path.exists(fake_dir):
        fake_files = glob.glob(os.path.join(fake_dir, '*'))[:100]  # Limit for speed
        for img_path in fake_files:
            try:
                img = image.load_img(img_path, target_size=target_size)
                img_array = image.img_to_array(img) / 255.0
                images.append(img_array)
                labels.append(0)  # Fake
            except Exception as e:
                print(f"Error loading {img_path}: {e}")
    
    # Load real images (label = 1)
    real_dir = os.path.join(test_dir, 'real')
    if os.path.exists(real_dir):
        real_files = glob.glob(os.path.join(real_dir, '*'))[:100]  # Limit for speed
        for img_path in real_files:
            try:
                img = image.load_img(img_path, target_size=target_size)
                img_array = image.img_to_array(img) / 255.0
                images.append(img_array)
                labels.append(1)  # Real
            except Exception as e:
                print(f"Error loading {img_path}: {e}")
    
    return np.array(images), np.array(labels)

def measure_accuracy():
    """Measure model accuracy on test dataset"""
    
    print("MODEL ACCURACY MEASUREMENT")
    print("=" * 50)
    
    # Load model
    model_paths = [
        'backend/model/deepfake_model_advanced.h5',
        'backend/model/deepfake_model_basic.h5',
        'backend/model/deepfake_model_quick.h5',
        'backend/model/deepfake_model.h5'
    ]
    
    model_path = None
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if not model_path:
        print("ERROR: No model found! Train a model first.")
        return
    
    print(f"Loading model: {model_path}")
    model = load_model(model_path)
    
    # Load test data
    print("Loading test images from dataset...")
    test_images, true_labels = load_test_images('dataset')
    
    if len(test_images) == 0:
        print("ERROR: No test images found in dataset/fake and dataset/real folders")
        return
    
    print(f"Loaded {len(test_images)} test images")
    print(f"   - Fake images: {np.sum(true_labels == 0)}")
    print(f"   - Real images: {np.sum(true_labels == 1)}")
    
    # Make predictions
    print("\nMaking predictions...")
    predictions = model.predict(test_images, verbose=0)
    predicted_labels = (predictions > 0.5).astype(int).flatten()
    
    # Calculate metrics
    accuracy = accuracy_score(true_labels, predicted_labels)
    
    print("\nACCURACY RESULTS")
    print("=" * 30)
    print(f"Overall Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
    
    # Detailed classification report
    print("\nDETAILED CLASSIFICATION REPORT")
    print("-" * 40)
    target_names = ['Fake', 'Real']
    report = classification_report(true_labels, predicted_labels, target_names=target_names)
    print(report)
    
    # Confusion matrix
    print("\nCONFUSION MATRIX")
    print("-" * 20)
    cm = confusion_matrix(true_labels, predicted_labels)
    print("           Predicted")
    print("         Fake  Real")
    print(f"Actual Fake  {cm[0,0]:4d}  {cm[0,1]:4d}")
    print(f"       Real  {cm[1,0]:4d}  {cm[1,1]:4d}")
    
    # Calculate specific metrics
    tn, fp, fn, tp = cm.ravel()
    
    print(f"\nPERFORMANCE METRICS")
    print("-" * 25)
    print(f"True Positives (Real correctly identified):  {tp}")
    print(f"True Negatives (Fake correctly identified): {tn}")
    print(f"False Positives (Fake labeled as Real):     {fp}")
    print(f"False Negatives (Real labeled as Fake):     {fn}")
    
    # Calculate rates
    if tp + fn > 0:
        sensitivity = tp / (tp + fn)  # True Positive Rate
        print(f"Sensitivity (Real detection rate): {sensitivity:.3f} ({sensitivity*100:.1f}%)")
    
    if tn + fp > 0:
        specificity = tn / (tn + fp)  # True Negative Rate
        print(f"Specificity (Fake detection rate): {specificity:.3f} ({specificity*100:.1f}%)")
    
    # Confidence analysis
    print(f"\nCONFIDENCE ANALYSIS")
    print("-" * 25)
    predictions_flat = predictions.flatten()
    avg_confidence = np.mean(np.maximum(predictions_flat, 1 - predictions_flat))
    print(f"Average Confidence: {avg_confidence:.3f} ({avg_confidence*100:.1f}%)")
    
    # High confidence predictions
    predictions_flat = predictions.flatten()
    high_conf_mask = np.maximum(predictions_flat, 1 - predictions_flat) > 0.8
    if np.any(high_conf_mask):
        high_conf_accuracy = accuracy_score(
            true_labels[high_conf_mask], 
            predicted_labels[high_conf_mask]
        )
        print(f"High Confidence (>80%) Accuracy: {high_conf_accuracy:.3f} ({high_conf_accuracy*100:.1f}%)")
        print(f"High Confidence Predictions: {np.sum(high_conf_mask)}/{len(predictions_flat)}")

def test_external_image(img_path):
    """Test accuracy on a single external image"""
    
    print(f"\nTESTING EXTERNAL IMAGE: {img_path}")
    print("=" * 50)
    
    if not os.path.exists(img_path):
        print("ERROR: Image file not found!")
        return
    
    # Load model
    model_paths = [
        'backend/model/deepfake_model_advanced.h5',
        'backend/model/deepfake_model_basic.h5',
        'backend/model/deepfake_model_quick.h5',
        'backend/model/deepfake_model.h5'
    ]
    
    model_path = None
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if not model_path:
        print("ERROR: No model found!")
        return
    
    model = load_model(model_path)
    
    # Process image
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    prediction = model.predict(img_array, verbose=0)[0][0]
    result = "Real" if prediction > 0.5 else "Fake"
    confidence = prediction if prediction > 0.5 else (1 - prediction)
    
    print(f"Raw prediction value: {prediction:.6f}")
    print(f"Result: {result}")
    print(f"Confidence: {confidence*100:.1f}%")
    
    # Determine expected result from filename
    filename = os.path.basename(img_path).lower()
    if 'fake' in filename:
        expected = "Fake"
    elif 'real' in filename:
        expected = "Real"
    else:
        expected = "Unknown"
    
    if expected != "Unknown":
        correct = (result == expected)
        print(f"Expected: {expected}")
        print(f"{'CORRECT' if correct else 'INCORRECT'}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test single image
        test_external_image(sys.argv[1])
    else:
        # Measure overall accuracy
        measure_accuracy()
        
        # Test external image if available
        external_img = r"C:\Users\Saravana Perumal\Downloads\person1_fake.jpg"
        if os.path.exists(external_img):
            test_external_image(external_img)