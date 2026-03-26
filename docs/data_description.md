# Dataset: Chest X-ray Images (Pneumonia)

## 📁 Dataset Information
**Source**: [Kaggle - Chest X-ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)  
**Total Images**: 5,856  
**Format**: JPEG  
**Resolution**: Varying (typically 1024×1024 to 2000×2000)  
**Classes**: 2 (NORMAL, PNEUMONIA)

## 🗂️ Original Organization
chest_xray/
├── train/
│ ├── NORMAL/ # 1,341 images
│ └── PNEUMONIA/ # 3,875 images
├── test/
│ ├── NORMAL/ # 234 images
│ └── PNEUMONIA/ # 390 images
└── val/
├── NORMAL/ # 8 images (problematic!)
└── PNEUMONIA/ # 8 images (too small)


## 🔄 my Modified Structure
i fixed the validation set by moving 20% of training images.

**Final Distribution**:
Dataset Split NORMAL PNEUMONIA TOTAL %Pneumonia
Train 1,073 3,101 4,174 74.3%
Validation 276 782 1,058 73.9%
Test 234 390 624 62.5%
TOTAL 1,583 4,273 5,856 73.0%


## ⚠️ Dataset Characteristics

### 1. **Class Imbalance**
- **Overall**: 73% Pneumonia, 27% Normal
- **Medical Reason**: Hospitals typically take more X-rays of sick patients
- **Impact**: Models tend to be biased toward Pneumonia class

### 2. **Image Quality Variations**
- Different hospitals/equipment
- Varying brightness and contrast
- Some images have annotations/text overlays

### 3. **Validation Set Issue**
**Original Problem**: Only 16 validation images (8 per class)  
**Our Solution**: Created proper validation set (1,058 images)  
**Method**: Stratified 20% split from training data


##  Preprocessing Steps

### Applied to All Images:
1. **Resizing**: 224×224 pixels (standard for CNNs)
2. **Normalization**: Mean=0.5, Std=0.5
3. **Format**: Converted to PyTorch tensors

### Training Set Augmentation:
- **Random Horizontal Flip**: p=0.5
- *(Future: More augmentations planned)*

### Validation/Test Sets:
- No augmentation (only resizing & normalization)
- Ensures fair evaluation

##  Medical Context

### Pneumonia in X-rays:
- **Normal**: Clear lung fields, visible bronchial structures
- **Pneumonia**: Opacities/consolidation, air bronchograms
- **Challenge**: Similar patterns can appear in other conditions

### Dataset Limitations:
1. **Binary Classification Only**: Real pneumonia has subtypes
2. **No Patient Demographics**: Age, gender, symptoms unknown
3. **Single View**: Only posterior-anterior (PA) views
4. **Validation Labels**: Assumed accurate but not verified by multiple radiologists
