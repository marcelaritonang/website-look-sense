from flask import Flask, request, jsonify
from flask_cors import CORS
from config.config import Config
from utils.image_processing import preprocess_image, allowed_file
from models.model_utils import FashionClassifier
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})

# Initialize model
classifier = FashionClassifier()

# Create upload folder if it doesn't exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/predict', methods=['POST'])
def predict():
    # Check if image was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Preprocess image
        img_array, filepath = preprocess_image(file)
        
        # Make prediction
        result = classifier.predict(img_array)
        
        # Add image path to result
        result['image_path'] = filepath
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)