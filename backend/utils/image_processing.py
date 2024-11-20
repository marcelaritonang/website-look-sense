import os
from PIL import Image
import numpy as np
from werkzeug.utils import secure_filename
from config.config import Config

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def preprocess_image(file):
    """Preprocess image for model prediction"""
    try:
        # Save file with secure filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Open and preprocess image
        img = Image.open(filepath)
        img = img.convert('RGB')
        img = img.resize(Config.IMAGE_SIZE)
        
        # Convert to array and normalize
        img_array = np.array(img)
        img_array = img_array.astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array, filepath
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")