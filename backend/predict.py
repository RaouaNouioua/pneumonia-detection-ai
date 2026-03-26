# predict.py
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from model_loader import CLASS_NAMES, preprocess_image

def predict_image(model, image: Image.Image, filename: str = None):
    """
    Make prediction on a single image
    
    Args:
        model: Loaded PyTorch model
        image: PIL Image object
        filename: Optional filename for logging
    
    Returns:
        prediction: Class name
        confidence: Percentage confidence
        probabilities: Array of probabilities for each class
    """
    # Preprocess image
    input_tensor = preprocess_image(image)
    
    # Move to same device as model
    device = next(model.parameters()).device
    input_tensor = input_tensor.to(device)
    
    # Make prediction
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = F.softmax(outputs[0], dim=0)
        confidence, predicted_idx = torch.max(probabilities, 0)
    
    # Convert to percentages
    confidence_percent = confidence.item() * 100
    probabilities_percent = (probabilities.cpu().numpy() * 100).tolist()
    
    # Get class name
    prediction = CLASS_NAMES[predicted_idx.item()]
    
    # Log prediction
    if filename:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Prediction for {filename}:")
        print(f"  -> {prediction} ({confidence_percent:.2f}% confidence)")
        for i, class_name in enumerate(CLASS_NAMES):
            print(f"     {class_name}: {probabilities_percent[i]:.2f}%")
    
    return prediction, confidence_percent, probabilities_percent

def analyze_prediction(prediction: str, confidence: float, probabilities: list):
    """
    Provide analysis based on prediction confidence
    
    Args:
        prediction: Predicted class
        confidence: Confidence percentage
        probabilities: List of probabilities for each class
    
    Returns:
        Dictionary with analysis
    """
    analysis = {
        "certainty": "high" if confidence > 80 else "medium" if confidence > 60 else "low",
        "recommendation": "",
        "notes": []
    }
    
    if prediction == "NORMAL":
        if confidence > 80:
            analysis["recommendation"] = "Low suspicion of pneumonia. Routine follow-up recommended."
            analysis["notes"].append("High confidence normal diagnosis")
        elif confidence > 60:
            analysis["recommendation"] = "Possible normal. Consider clinical correlation."
            analysis["notes"].append("Moderate confidence - radiologist review suggested")
        else:
            analysis["recommendation"] = "Inconclusive. Radiologist review strongly recommended."
            analysis["notes"].append("Low confidence - further evaluation needed")
    
    else:  # PNEUMONIA
        if confidence > 85:
            analysis["recommendation"] = "High suspicion of pneumonia. Immediate clinical evaluation recommended."
            analysis["notes"].append("High confidence pneumonia detection")
        elif confidence > 70:
            analysis["recommendation"] = "Possible pneumonia. Urgent clinical correlation needed."
            analysis["notes"].append("Moderate confidence - confirm with radiologist")
        else:
            analysis["recommendation"] = "Suspicious findings. Requires immediate radiologist review."
            analysis["notes"].append("Low confidence - urgent evaluation required")
    
    # Add probability difference note
    prob_diff = abs(probabilities[0] - probabilities[1])
    if prob_diff < 10:
        analysis["notes"].append("Close probabilities - borderline case")
    
    return analysis

def generate_visualization(image: Image.Image, prediction: str, 
                          confidence: float, probabilities: list,
                          save_path: str = None):
    """
    Generate a visualization of the prediction
    
    Args:
        image: Original image
        prediction: Predicted class
        confidence: Confidence percentage
        probabilities: List of probabilities
        save_path: Path to save visualization
    
    Returns:
        Path to saved visualization
    """
    if save_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"results/visualization_{timestamp}.png"
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Image with prediction
    axes[0].imshow(image)
    axes[0].set_title(f"Prediction: {prediction}\nConfidence: {confidence:.1f}%")
    axes[0].axis('off')
    
    # Plot 2: Probability bar chart
    y_pos = np.arange(len(CLASS_NAMES))
    colors = ['lightgreen' if c == prediction else 'lightcoral' for c in CLASS_NAMES]
    
    axes[1].barh(y_pos, probabilities, color=colors)
    axes[1].set_yticks(y_pos)
    axes[1].set_yticklabels(CLASS_NAMES)
    axes[1].set_xlabel('Probability (%)')
    axes[1].set_title('Class Probabilities')
    
    # Add probability values on bars
    for i, prob in enumerate(probabilities):
        axes[1].text(prob + 1, i, f'{prob:.1f}%', va='center')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return save_path

def batch_predict(model, image_paths: list):
    """
    Make predictions on multiple images
    
    Args:
        model: Loaded PyTorch model
        image_paths: List of image file paths
    
    Returns:
        List of prediction results
    """
    results = []
    
    for image_path in image_paths:
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Make prediction
            prediction, confidence, probabilities = predict_image(model, image, image_path)
            
            # Generate visualization
            viz_path = generate_visualization(
                image, prediction, confidence, probabilities,
                f"results/{os.path.basename(image_path)}_result.png"
            )
            
            results.append({
                "file": image_path,
                "prediction": prediction,
                "confidence": confidence,
                "probabilities": probabilities,
                "visualization": viz_path,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            results.append({
                "file": image_path,
                "error": str(e),
                "prediction": "ERROR"
            })
    
    return results

# Test function
def test_prediction():
    """Test the prediction pipeline with a sample image"""
    from model_loader import load_resnet18_model
    
    print("Testing prediction pipeline...")
    
    # Load model
    model = load_resnet18_model()
    
    # Create a dummy test image (black image)
    test_image = Image.new('RGB', (224, 224), color='white')
    
    # Make prediction
    prediction, confidence, probabilities = predict_image(model, test_image, "test_image")
    
    print(f"\nTest Prediction Result:")
    print(f"Prediction: {prediction}")
    print(f"Confidence: {confidence:.2f}%")
    print(f"Probabilities: {dict(zip(CLASS_NAMES, probabilities))}")
    
    return prediction, confidence, probabilities

if __name__ == "__main__":
    # Run test
    test_prediction()