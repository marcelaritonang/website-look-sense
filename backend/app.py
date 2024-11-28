from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import torch
from PIL import Image
import io
import base64
import numpy as np

app = Flask(__name__)
CORS(app)  # Ini penting untuk mengizinkan request dari frontend

# Load model dan kelas
model = None
classes = [
    "Bags",
    "Bottomwear",
    "Dress",
    "Headwear",
    "Shoes",
    "Topwear",
    "Watches"
]

def load_model():
    global model
    try:
        # Sesuaikan path dengan lokasi model Anda
        model_path = os.path.join('model_penyimpanan', 'model_v3', 'model.json')
        if os.path.exists(model_path):
            print("Model found at:", model_path)
        else:
            print("Model not found at:", model_path)
        # Load model logic here
    except Exception as e:
        print("Error loading model:", str(e))

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Get the image from the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        image = Image.open(file.stream)
        
        # Preprocess the image
        image = image.resize((128, 128))
        image = np.array(image) / 255.0
        
        # Make prediction
        with torch.no_grad():
            # Add batch dimension and convert to tensor
            image_tensor = torch.FloatTensor(image).unsqueeze(0)
            outputs = model(image_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities).item()
            
        # Get all probabilities
        probs = probabilities[0].numpy().tolist()
        
        return jsonify({
            'predicted_class': classes[predicted_class],
            'class_probabilities': {
                classes[i]: float(prob) 
                for i, prob in enumerate(probs)
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    load_model()
    app.run(debug=True, port=5000)