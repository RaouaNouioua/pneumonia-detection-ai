# app.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import torch
import numpy as np
from PIL import Image
import io
import os
from datetime import datetime
import logging

# Import your model loader
from model_loader import load_resnet18_model, preprocess_image, CLASS_NAMES
from predict import predict_image, analyze_prediction

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Pneumonia Detection API",
    description="API for detecting pneumonia from chest X-ray images using ResNet18",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model on startup
@app.on_event("startup")
async def startup_event():
    try:
        app.state.model = load_resnet18_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Pneumonia Detection API",
        "status": "active",
        "version": "1.0.0",
        "model": "ResNet18",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "batch_test": "/test-batch",
            "model_info": "/model-info"
        }
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": app.state.model is not None
    }

# Model information endpoint
@app.get("/model-info")
async def model_info():
    model = app.state.model
    return {
        "model_name": "ResNet18",
        "classes": CLASS_NAMES,
        "input_size": "224x224",
        "parameters": sum(p.numel() for p in model.parameters()),
        "trainable_parameters": sum(p.numel() for p in model.parameters() if p.requires_grad),
        "training_data": {
            "normal_samples": 1073,
            "pneumonia_samples": 3101,
            "total_samples": 4174
        },
        "test_performance": {
            "accuracy": "86.06%",
            "normal_recall": "67.09%",
            "pneumonia_recall": "97.44%",
            "normal_precision": "94%",
            "pneumonia_precision": "83%"
        }
    }

# Single image prediction endpoint
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict pneumonia from a single chest X-ray image
    
    Returns:
    - prediction: "NORMAL" or "PNEUMONIA"
    - confidence: percentage confidence
    - probabilities: probability for each class
    - analysis: detailed analysis of the prediction
    - timestamp: when prediction was made
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Save upload for testing (optional)
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(upload_dir, filename)
        image.save(filepath)
        
        # Make prediction
        prediction, confidence, probabilities = predict_image(
            app.state.model, 
            image, 
            filepath
        )
        
        # Analyze prediction
        analysis = analyze_prediction(prediction, confidence, probabilities)
        
        # Prepare response
        response = {
            "status": "success",
            "prediction": prediction,
            "confidence": f"{confidence:.2f}%",
            "probabilities": {
                "NORMAL": f"{probabilities[0]:.2f}%",
                "PNEUMONIA": f"{probabilities[1]:.2f}%"
            },
            "analysis": analysis,
            "image_info": {
                "filename": filename,
                "size": f"{image.width}x{image.height}",
                "saved_path": filepath
            },
            "timestamp": datetime.now().isoformat(),
            "model_used": "ResNet18 (transfer learning)"
        }
        
        logger.info(f"Prediction made: {prediction} ({confidence:.2f}%)")
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Batch testing endpoint (for testing with multiple images)
@app.post("/test-batch")
async def test_batch(files: list[UploadFile] = File(...)):
    """
    Test multiple images at once
    
    Returns:
    - summary of all predictions
    - individual results for each image
    - statistics
    """
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No files provided")
    
    results = []
    normal_count = 0
    pneumonia_count = 0
    
    for file in files:
        try:
            # Read image
            contents = await file.read()
            image = Image.open(io.BytesIO(contents)).convert('RGB')
            
            # Make prediction
            prediction, confidence, probabilities = predict_image(
                app.state.model, 
                image, 
                file.filename
            )
            
            # Update counts
            if prediction == "NORMAL":
                normal_count += 1
            else:
                pneumonia_count += 1
            
            # Store result
            results.append({
                "filename": file.filename,
                "prediction": prediction,
                "confidence": f"{confidence:.2f}%",
                "probabilities": {
                    "NORMAL": f"{probabilities[0]:.2f}%",
                    "PNEUMONIA": f"{probabilities[1]:.2f}%"
                }
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e),
                "prediction": "ERROR"
            })
    
    # Summary statistics
    total = len(results)
    success_count = len([r for r in results if "error" not in r])
    
    return {
        "summary": {
            "total_images": total,
            "successful_predictions": success_count,
            "failed_predictions": total - success_count,
            "normal_count": normal_count,
            "pneumonia_count": pneumonia_count,
            "normal_percentage": f"{(normal_count/success_count*100):.1f}%" if success_count > 0 else "0%",
            "pneumonia_percentage": f"{(pneumonia_count/success_count*100):.1f}%" if success_count > 0 else "0%"
        },
        "results": results,
        "timestamp": datetime.now().isoformat()
    }

# Mock test results endpoint (returns your actual test results)
@app.get("/test-results")
async def get_test_results():
    """
    Returns the actual test results from your model evaluation
    """
    return {
        "test_data_summary": {
            "total_samples": 624,
            "normal_samples": 234,
            "pneumonia_samples": 390,
            "test_accuracy": "86.06%"
        },
        "confusion_matrix": {
            "true_normal_predicted_normal": 157,
            "true_normal_predicted_pneumonia": 77,
            "true_pneumonia_predicted_normal": 10,
            "true_pneumonia_predicted_pneumonia": 380
        },
        "classification_report": {
            "NORMAL": {
                "precision": 0.94,
                "recall": 0.67,
                "f1_score": 0.78,
                "support": 234
            },
            "PNEUMONIA": {
                "precision": 0.83,
                "recall": 0.97,
                "f1_score": 0.90,
                "support": 390
            }
        },
        "key_metrics": {
            "test_accuracy": 0.8606,
            "normal_recall": 0.6709,
            "pneumonia_recall": 0.9744,
            "model_comparison": {
                "baseline_cnn_accuracy": 0.74,
                "resnet18_accuracy": 0.8606,
                "improvement": "12.06%"
            }
        },
        "recommendations": [
            "Use confidence threshold > 80% for reliable predictions",
            "Normal cases might need radiologist confirmation if confidence < 70%",
            "Model is better at detecting pneumonia (97% recall)",
            "Consider chest X-ray quality for better predictions"
        ]
    }

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Endpoint specifically for your React frontend
    Returns format: {
        "diagnosis": "Pneumonia Detected" or "Normal",
        "confidence": 95.5,
        "severity": "high",
        "recommendations": ["rec1", "rec2"],
        "model_used": "ResNet18",
        "processing_time": "1.5s",
        "timestamp": "2024-01-01T12:00:00"
    }
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Make prediction using existing function
        prediction, confidence, probabilities = predict_image(
            app.state.model, 
            image, 
            file.filename
        )
        
        # Analyze prediction
        analysis = analyze_prediction(prediction, confidence, probabilities)
        
        # Convert to frontend expected format
        diagnosis = "Pneumonia Detected" if prediction == "PNEUMONIA" else "Normal"
        
        # Determine severity based on confidence
        if prediction == "PNEUMONIA":
            if confidence > 85:
                severity = "high"
            elif confidence > 70:
                severity = "moderate"
            else:
                severity = "low"
        else:
            severity = "None"  # Normal cases have no severity
        
        # Prepare recommendations array
        recommendations = []
        if analysis["recommendation"]:
            recommendations.append(analysis["recommendation"])
        recommendations.extend(analysis["notes"])
        
        # Add standard medical recommendations
        if prediction == "PNEUMONIA":
            recommendations.append("Consider antibiotic therapy")
            recommendations.append("Monitor oxygen saturation levels")
            recommendations.append("Follow-up chest X-ray in 48-72 hours")
        else:
            recommendations.append("Routine annual check-up recommended")
            recommendations.append("Maintain good respiratory hygiene")
        
        # Prepare response in frontend format
        response = {
            "diagnosis": diagnosis,
            "confidence": round(confidence, 1),  # e.g., 95.5
            "severity": severity,
            "recommendations": recommendations,
            "model_used": "ResNet18 (Transfer Learning)",
            "processing_time": "1.5s",  # You can make this dynamic
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Frontend analysis: {diagnosis} ({confidence:.2f}%)")
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )