# Pneumonia Detection from Chest X-rays

##  Project Overview
This project implements deep learning models for binary classification of chest X-ray images into **NORMAL** vs **PNEUMONIA** categories. The goal is to assist radiologists in early pneumonia detection using computer vision techniques.

##  Dataset
We use the [Chest X-ray Images (Pneumonia) dataset](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) from Kaggle, containing 5,856 chest X-ray images in JPEG format.

**Original Distribution:**
- Train: 1,341 Normal, 3,875 Pneumonia
- Val: 8 Normal, 8 Pneumonia (Too small!)
- Test: 234 Normal, 390 Pneumonia

**Our Modified Distribution:**
We moved 20% of training images to validation for better model evaluation:
- Train: 1,073 Normal, 3,101 Pneumonia
- Validation: 276 Normal, 782 Pneumonia
- Test: 234 Normal, 390 Pneumonia (unchanged)

## Project Structure 
pneumonia_ai_v1/
├── model/ # Main project folder
│ ├── 01_data_loading.ipynb # Data preparation
│ ├── 02_baseline_cnn.ipynb # Baseline CNN training
│ └── artifacts/
│ └── models/
│ └── baseline_cnn_best.pth # Saved model
├── data/ # Dataset folder (separate)
│ └── chest_xray/
│ ├── train/
│ │ ├── NORMAL/
│ │ └── PNEUMONIA/
│ ├── val/
│ │ ├── NORMAL/
│ │ └── PNEUMONIA/
│ └── test/
│ ├── NORMAL/
│ └── PNEUMONIA/
├── README.md # This file
├── progress.md # Project tracking
└── DATA_DESCRIPTION.md # Dataset documentation


##  Quick Start
1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd pneumonia_ai_v1

2. **Install dependencies:
pip install -r requirements.txt

3. Current Results
Baseline CNN (3-layer)
Validation Accuracy: 97.64%
Test Accuracy: 79.0%
Pneumonia Recall: 98% (Excellent for medical safety)
Normal Recall: 47% (Needs improvement)

4. Confusion Matrix (Test Set):
              Predicted
              Normal  Pneumonia
Actual Normal   110       124
Actual Pneumonia  8       382

5. Key Features
Class Imbalance Handling: Weighted loss function
Data Augmentation: Random horizontal flips
Model Checkpointing: Saves best model automatically
Visualization: Training curves & confusion matrices

##  Final Results

### Model Comparison Summary
| Metric | Baseline CNN | ResNet18 (Transfer Learning) | Improvement |
|--------|--------------|------------------------------|-------------|
| **Test Accuracy** | 79.0% | **86.1%** | **+7.1%** |
| **Normal Recall** | 47% | **67%** | **+20%** |
| **Pneumonia Recall** | 98.5% | 97.4% | -1.1% (acceptable trade-off) |
| **False Positives** | 154 | **77** | **50% reduction** |
| **Training Time** | 15 min | 25 min | +10 min (worth it!) |

### Clinical Impact Analysis
**With 1,000 patients (estimated):**
- **Before (Baseline)**: 340 correctly sent home, 660 false alarms 
- **After (ResNet18)**: 670 correctly sent home, 330 false alarms 
- **Pneumonia detection**: 985 vs 974 correctly treated (excellent both)

### Key Learnings
1. **Transfer learning works**: Pre-trained models significantly improve medical AI
2. **Class imbalance matters**: Weighted loss function is crucial
3. **Explainability is key**: Grad-CAM builds doctor trust
4. **Medical AI requires balance**: Safety vs. accuracy trade-offs

## Project Completion
- ✅ Phase 1: Baseline CNN implementation
- ✅ Phase 2: Transfer learning with ResNet18  
- ✅ Phase 3: Model explainability (Grad-CAM)
- ✅ Phase 4: Comprehensive documentation
- ✅ Phase 5: interface developemt 

6. Workflow
Data Preparation → 2. Baseline Model → 3. Transfer Learning → 4. Model Comparison → 5. Deployment


7. Technical Stack Mastered:
Frontend: React with Tailwind CSS
Backend: FastAPI (Python)
AI: PyTorch + ResNet18 (transfer learning)
Deployment: Local server setup
Medical AI: Complete pipeline from data to diagnosis

8. Technologies
Python 3.11+
PyTorch 2.0+
TorchVision
Scikit-learn
Matplotlib/Seaborn
Jupyter Notebook



