import os
from pathlib import Path

class Config:
    # Base directory
    BASE_DIR = Path(__file__).parent.parent.absolute()
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Model settings
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model_weights.h5')
    CLASS_NAMES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt']
    
    # Image settings
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    IMAGE_SIZE = (177, 177)

    # CORS settings
    CORS_HEADERS = ['Content-Type']
    CORS_ORIGINS = ["http://localhost:3000"]  # Frontend URL