[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Pneumonia Detection from Chest X-rays

## Project Overview
This project implements deep learning models for binary classification of chest X-ray images into **NORMAL** vs **PNEUMONIA** categories. The goal is to assist radiologists in early pneumonia detection using computer vision techniques.

---

## Dataset
We use the [Chest X-ray Images (Pneumonia) dataset](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) from Kaggle, containing 5,856 chest X-ray images in JPEG format.

**Original Distribution:**
- Train: 1,341 Normal, 3,875 Pneumonia
- Val: 8 Normal, 8 Pneumonia *(Too small!)*
- Test: 234 Normal, 390 Pneumonia

**Our Modified Distribution:**
We moved 20% of training images to validation for better model evaluation:
- Train: 1,073 Normal, 3,101 Pneumonia
- Validation: 276 Normal, 782 Pneumonia
- Test: 234 Normal, 390 Pneumonia *(unchanged)*

---

## Project Structure

```
pneumonia_ai_v1/
├── model/                          # Main project folder
│   ├── 01_data_loading.ipynb       # Data preparation
│   ├── 02_baseline_cnn.ipynb       # Baseline CNN training
│   └── artifacts/
│       └── models/
│           └── baseline_cnn_best.pth  # Saved model
├── data/                           # Dataset folder (separate)
│   └── chest_xray/
│       ├── train/
│       │   ├── NORMAL/
│       │   └── PNEUMONIA/
│       ├── val/
│       │   ├── NORMAL/
│       │   └── PNEUMONIA/
│       └── test/
│           ├── NORMAL/
│           └── PNEUMONIA/
├── README.md                       # This file
├── progress.md                     # Project tracking
└── DATA_DESCRIPTION.md             # Dataset documentation
```

---

## Quick Start

**1. Clone the repository:**
```bash
git clone https://github.com/RaouaNouioua/pneumonia-detection-ai.git
cd pneumonia-detection-ai
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

---

## Current Results

### Baseline CNN (3-layer)
- **Validation Accuracy:** 97.64%
- **Test Accuracy:** 79.0%
- **Pneumonia Recall:** 98% ✅ *(Excellent for medical safety)*
- **Normal Recall:** 47% ⚠️ *(Needs improvement)*

### Confusion Matrix (Test Set)
```
              Predicted
              Normal  Pneumonia
Actual Normal   110       124
Actual Pneumonia  8       382
```

---

## Key Features
- **Class Imbalance Handling:** Weighted loss function
- **Data Augmentation:** Random horizontal flips
- **Model Checkpointing:** Saves best model automatically
- **Visualization:** Training curves & confusion matrices

---

## Final Results

### Model Comparison Summary

| Metric | Baseline CNN | ResNet18 (Transfer Learning) | Improvement |
|--------|-------------|------------------------------|-------------|
| **Test Accuracy** | 79.0% | **86.1%** | **+7.1%** |
| **Normal Recall** | 47% | **67%** | **+20%** |
| **Pneumonia Recall** | 98.5% | 97.4% | -1.1% *(acceptable trade-off)* |
| **False Positives** | 154 | **77** | **50% reduction** |
| **Training Time** | 15 min | 25 min | +10 min *(worth it!)* |

### Clinical Impact Analysis
**With 1,000 patients (estimated):**
- **Before (Baseline):** 340 correctly sent home, 660 false alarms ❌
- **After (ResNet18):** 670 correctly sent home, 330 false alarms ✅
- **Pneumonia detection:** 985 vs 974 correctly treated *(excellent both)*

---

## Key Learnings
1. **Transfer learning works:** Pre-trained models significantly improve medical AI
2. **Class imbalance matters:** Weighted loss function is crucial
3. **Explainability is key:** Grad-CAM builds doctor trust
4. **Medical AI requires balance:** Safety vs. accuracy trade-offs

---

## Project Completion
- ✅ Phase 1: Baseline CNN implementation
- ✅ Phase 2: Transfer learning with ResNet18
- ✅ Phase 3: Model explainability (Grad-CAM)
- ✅ Phase 4: Comprehensive documentation
- ✅ Phase 5: Interface development

---

## Workflow
**Data Preparation → Baseline Model → Transfer Learning → Model Comparison → Deployment**

---

## Technical Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React with Tailwind CSS |
| Backend | FastAPI (Python) |
| AI Model | PyTorch + ResNet18 (transfer learning) |
| Deployment | Local server setup |

---

## Technologies
- Python 3.11+
- PyTorch 2.0+
- TorchVision
- Scikit-learn
- Matplotlib / Seaborn
- Jupyter Notebook

---

## How to Run the Complete System

### Prerequisites
- Python 3.11+
- Node.js (for frontend)
- 8GB RAM minimum

### Step 1: Clone the Repository
```bash
git clone https://github.com/RaouaNouioua/pneumonia-detection-ai.git
cd pneumonia-detection-ai
```

### Step 2: Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

**Root:**
```bash
pip install -r requirements.txt
```

**Frontend (optional):**
```bash
cd frontend
npm install
cd ..
```

### Step 3: Download the Dataset
1. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
2. Extract to `data/chest_xray/` folder

```
data/chest_xray/
├── train/
│   ├── NORMAL/
│   └── PNEUMONIA/
├── val/
│   ├── NORMAL/
│   └── PNEUMONIA/
└── test/
    ├── NORMAL/
    └── PNEUMONIA/
```

### Step 4: Run the Backend API
```bash
cd backend
python app.py
```

The server will start at: `http://localhost:8000`

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     ✅ Model loaded successfully
INFO:     Application startup complete.
```

### Step 5: Run the Frontend
```bash
cd frontend
npm start
```
Then open: `http://localhost:3000`

### Step 6: Test the System
1. Open the frontend in your browser
2. Drag & drop a chest X-ray image or click to upload
3. Wait 1–2 seconds for AI analysis
4. View results:
   - Diagnosis (Normal or Pneumonia Detected)
   - Confidence score (0–100%)
   - Severity level (for pneumonia cases)
   - Clinical recommendations
   - Heatmap visualization (shows where AI is looking)

### Step 7: API Endpoints (for developers)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `http://localhost:8000/health` | Check if API is running |
| GET | `http://localhost:8000/model-info` | Model performance metrics |
| POST | `http://localhost:8000/api/analyze` | Upload and analyze X-ray |
| GET | `http://localhost:8000/docs` | Interactive API documentation |

---

## Troubleshooting

**Port already in use:**
```bash
# Change port in backend/app.py (line 134)
port=8000  # Change to 8001 or any available port
```

**Model not found:**
- Ensure you have trained the model first
- Check path in `backend/model_loader.py`
- Models are excluded from git (too large) — you need to train them locally

**CORS errors:**
- Make sure backend CORS settings allow your frontend origin
- Current settings allow all origins (`"*"`)

**Memory issues:**
- Run on CPU if GPU memory is limited
- Reduce batch size in training notebooks

---

## 🧪 Training Your Own Models

**Train Baseline CNN:**
```bash
jupyter notebook model/02_baseline_cnn.ipynb
```

**Train ResNet18 with Transfer Learning:**
```bash
jupyter notebook model/03_transfer_learning.ipynb
```

**Generate Grad-CAM Visualizations:**
```bash
jupyter notebook model/04_grad_cam_visualization.ipynb
```

Trained models will be saved to `model/artifacts/models/`
