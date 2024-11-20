# config/config.py
import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).parent.parent.absolute()
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-fashion-classifier-key')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model_weights.h5')
    
    # Update class names sesuai dengan model
    CLASS_NAMES = [
        'Bags',
        'Bottomwear',
        'Dress',
        'Headwear',
        'Shoes',
        'Topwear',
        'Watches'
    ]
    
    CORS_HEADERS = ['Content-Type']
    CORS_ORIGINS = ["http://localhost:3000"]