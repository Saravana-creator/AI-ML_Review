# Training Scripts

## Available Models

### 1. Quick Train (`quick_train.py`)
- **Time**: ~30 minutes
- **Epochs**: 10
- **Use case**: Fast testing, proof of concept
- **Output**: `deepfake_model_quick.h5`

### 2. Basic Train (`basic_model.py`)
- **Time**: ~1 hour
- **Epochs**: 20 with early stopping
- **Features**: Data augmentation, dropout
- **Output**: `deepfake_model_basic.h5`

### 3. Advanced Train (`advanced_model.py`)
- **Time**: ~3 hours
- **Epochs**: 50 (30 + 20 fine-tuning)
- **Features**: EfficientNet, transfer learning
- **Output**: `deepfake_model_advanced.h5`

## How to Use

### Option 1: Training Manager (Recommended)
```bash
cd training
python train_manager.py
```

### Option 2: Direct Training
```bash
cd training
python quick_train.py      # For quick test
python basic_model.py      # For balanced training
python advanced_model.py   # For best results
```

## Model Selection Guide

- **Testing/Development**: Use Quick Train
- **Production (Good)**: Use Basic Train
- **Production (Best)**: Use Advanced Train

## Output Location
All models are saved to: `../backend/model/`