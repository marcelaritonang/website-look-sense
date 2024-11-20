from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from config.config import Config
from models.model_utils import FashionClassifier
from utils.image_processing import preprocess_image, allowed_file

app = Flask(__name__)
app.config.from_object(Config)

# Setup CORS
CORS(app, resources={
   r"/api/*": {
       "origins": Config.CORS_ORIGINS,
       "methods": ["GET", "POST", "OPTIONS"],
       "allow_headers": ["Content-Type"]
   }
})

# Initialize classifier
print("Loading model...")
classifier = FashionClassifier()
print("Model loaded successfully!")

# Create upload folder if it doesn't exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/predict', methods=['POST'])
def predict():
   """
   Endpoint untuk memprediksi gambar fashion
   """
   # Validasi request
   if 'file' not in request.files:
       print("No file in request")
       return jsonify({'error': 'No file uploaded'}), 400
   
   file = request.files['file']
   if file.filename == '':
       print("Empty filename")
       return jsonify({'error': 'No file selected'}), 400
       
   if not allowed_file(file.filename):
       print(f"Invalid file type: {file.filename}")
       return jsonify({'error': 'Invalid file type. Allowed types: jpg, jpeg, png'}), 400
   
   try:
       # Preprocessing gambar
       print(f"Processing image: {file.filename}")
       img_array, filepath = preprocess_image(file)
       
       # Validasi array gambar
       if img_array.shape != (1, 177, 177, 3):
           raise ValueError(f"Invalid image dimensions. Expected (1, 177, 177, 3), got {img_array.shape}")
           
       if img_array.min() < 0 or img_array.max() > 1:
           raise ValueError(f"Invalid pixel values. Expected range [0,1], got [{img_array.min():.3f}, {img_array.max():.3f}]")
       
       # Prediksi
       print("Making prediction...")
       predictions = classifier.predict(img_array)
       
       # Filter prediksi dengan confidence rendah
       CONFIDENCE_THRESHOLD = 5.0  # 5%
       filtered_predictions = [
           p for p in predictions 
           if p['probability'] >= CONFIDENCE_THRESHOLD
       ]
       
       # Sort berdasarkan probability
       filtered_predictions.sort(key=lambda x: x['probability'], reverse=True)
       
       print(f"Predictions: {filtered_predictions}")
       
       return jsonify({
           'success': True,
           'predictions': filtered_predictions,
           'image_path': filepath
       }), 200
       
   except Exception as e:
       print(f"Error during prediction: {str(e)}")
       return jsonify({
           'success': False,
           'error': str(e)
       }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
   """
   Endpoint untuk mengecek status server
   """
   try:
       return jsonify({
           'status': 'healthy',
           'model_loaded': classifier is not None
       }), 200
   except Exception as e:
       return jsonify({
           'status': 'unhealthy',
           'error': str(e)
       }), 500

@app.route('/api/classes', methods=['GET'])
def get_classes():
   """
   Endpoint untuk mendapatkan daftar kelas
   """
   try:
       return jsonify({
           'success': True,
           'classes': Config.CLASS_NAMES
       }), 200
   except Exception as e:
       return jsonify({
           'success': False,
           'error': str(e)
       }), 500

@app.errorhandler(404)
def not_found(e):
   return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
   return jsonify({'error': 'Internal server error'}), 500

# Custom error handler untuk file terlalu besar
@app.errorhandler(413)
def request_entity_too_large(e):
   return jsonify({
       'error': 'File too large',
       'max_size': f"{Config.MAX_CONTENT_LENGTH / (1024 * 1024)}MB"
   }), 413

if __name__ == '__main__':
   print(f"Starting server... Model will be loaded with classes: {Config.CLASS_NAMES}")
   app.run(
       host='0.0.0.0',  # Bisa diakses dari luar
       port=5000,
       debug=True  # Set False untuk production
   )