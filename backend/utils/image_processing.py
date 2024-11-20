# utils/image_processing.py
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import os
from config.config import Config
from werkzeug.utils import secure_filename

def allowed_file(filename):
    """
    Check if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def preprocess_image(file):
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Open and preprocess image
        img = Image.open(filepath)
        img = img.convert('RGB')
        
        # Enhanced preprocessing
        img = ImageOps.autocontrast(img, cutoff=2)
        
        # Brightness adjustment
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        
        # Contrast adjustment
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Resize
        img = img.resize((177, 177))
        
        # Convert to array and normalize
        img_array = np.array(img)
        img_array = img_array.astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        print(f"Preprocessed image shape: {img_array.shape}")
        print(f"Value range: {img_array.min():.3f} to {img_array.max():.3f}")
        
        return img_array, filepath
        
    except Exception as e:
        raise Exception(f"Image processing error: {str(e)}")