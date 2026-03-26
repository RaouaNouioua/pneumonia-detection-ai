# model_loader.py
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import warnings
import logging
import os

# Suppress warnings
warnings.filterwarnings('ignore')

# Constants
CLASS_NAMES = ['NORMAL', 'PNEUMONIA']
IMG_SIZE = (224, 224)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "artifacts", "models", "resnet18_best.pth")

def load_resnet18_model(model_path: str = MODEL_PATH, device: str = None):
    """
    Load the trained ResNet18 model
    
    Args:
        model_path: Path to the saved model weights
        device: 'cuda' or 'cpu', defaults to GPU if available
    
    Returns:
        Loaded and configured ResNet18 model
    """
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    logging.info(f"Loading model from {model_path} on {device}")
    
    # Initialize model architecture
    model = models.resnet18(weights=None)  # Don't load ImageNet weights
    
    # Modify final layer for binary classification
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(CLASS_NAMES))
    
    # Load trained weights
    try:
        model.load_state_dict(torch.load(model_path, map_location=device))
    except FileNotFoundError:
        logging.error(f"Model file not found at {model_path}")
        # Try to find it in different locations
        import os
        possible_paths = [
        model_path,
        os.path.join(BASE_DIR, "..", "model", "artifacts", "models", "resnet18_best.pth"),
        r"C:\Users\HP\Desktop\pneumonia_ai_v1\model\artifacts\models\resnet18_best.pth",
        "resnet18_best.pth"  # If copied to backend folder
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                model.load_state_dict(torch.load(path, map_location=device))
                logging.info(f"Found model at {path}")
                break
        else:
            raise FileNotFoundError(f"Could not find model file. Tried: {possible_paths}")
    
    # Move to device and set to evaluation mode
    model = model.to(device)
    model.eval()
    
    logging.info(f" Model loaded successfully")
    logging.info(f"  - Device: {device}")
    logging.info(f"  - Parameters: {sum(p.numel() for p in model.parameters()):,}")
    logging.info(f"  - Classes: {CLASS_NAMES}")
    
    return model

def preprocess_image(image: Image.Image):
    """
    Preprocess image for ResNet18 model
    
    Args:
        image: PIL Image object
    
    Returns:
        Preprocessed tensor ready for model input
    """
    # Define the same transforms used during training
    transform = transforms.Compose([
        transforms.Resize(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])
    
    # Apply transforms
    tensor = transform(image)
    
    # Add batch dimension
    tensor = tensor.unsqueeze(0)
    
    return tensor

def get_class_weights():
    """
    Get class weights used during training
    """
    # These are the weights you calculated
    return {
        'NORMAL': 1.9450,
        'PNEUMONIA': 0.6730
    }

def get_model_performance():
    """
    Return the model's test performance metrics
    """
    return {
        'accuracy': 0.8606,
        'normal_recall': 0.6709,
        'pneumonia_recall': 0.9744,
        'normal_precision': 0.94,
        'pneumonia_precision': 0.83,
        'confusion_matrix': {
            'TN': 157, 'FP': 77,
            'FN': 10, 'TP': 380
        }
    }