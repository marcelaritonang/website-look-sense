import tensorflow as tf
import numpy as np
from config.config import Config
import json
import os

class FashionClassifier:
   def __init__(self):
       # Load model architecture from JSON
       with open(os.path.join(Config.BASE_DIR, 'models', 'model.json'), 'r') as f:
           model_json = json.load(f)
           self.model = tf.keras.models.model_from_json(json.dumps(model_json))
       
       # Load pre-trained weights
       self.model.load_weights(Config.MODEL_PATH)
       
       # Compile model with appropriate settings
       self.model.compile(
           optimizer='adam',
           loss='sparse_categorical_crossentropy',
           metrics=['accuracy']
       )
       
       self.class_names = Config.CLASS_NAMES

   def predict(self, image_array):
    try:
        # Multiple predictions dengan sedikit variasi
        predictions = []
        
        # Original image
        pred1 = self.model.predict(image_array)
        predictions.append(pred1[0])
        
        # Slightly brighter
        bright_img = image_array * 1.1
        bright_img = np.clip(bright_img, 0, 1)
        pred2 = self.model.predict(bright_img)
        predictions.append(pred2[0])
        
        # Slightly darker
        dark_img = image_array * 0.9
        pred3 = self.model.predict(dark_img)
        predictions.append(pred3[0])
        
        # Average predictions
        avg_pred = np.mean(predictions, axis=0)
        probabilities = tf.nn.softmax(avg_pred)
        
        # Confidence thresholding
        MIN_CONFIDENCE = 0.15  # 15%
        result = []
        
        for idx, prob in enumerate(probabilities):
            confidence = float(prob * 100)
            if confidence >= MIN_CONFIDENCE:
                result.append({
                    'class': self.class_names[idx],
                    'probability': round(confidence, 2)
                })
        
        # Sort by probability
        result.sort(key=lambda x: x['probability'], reverse=True)
        
        # Apply smoothing to probabilities
        total_prob = sum(item['probability'] for item in result)
        if total_prob > 0:
            for item in result:
                item['probability'] = (item['probability'] / total_prob) * 100
        
        return result
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        raise Exception(f"Error in prediction: {str(e)}")

   def preprocess_prediction(self, predictions):
       """Helper method to process raw predictions"""
       try:
           # Convert predictions to probabilities
           probabilities = tf.nn.softmax(predictions[0])
           
           # Get the highest probability and its index
           max_prob_index = np.argmax(probabilities)
           confidence = float(probabilities[max_prob_index])
           
           return {
               'class': self.class_names[max_prob_index],
               'confidence': confidence,
               'probabilities': [float(p) for p in probabilities]
           }
       except Exception as e:
           raise Exception(f"Error processing prediction: {str(e)}")

   def get_all_probabilities(self, image_array):
       """Get detailed probabilities for all classes"""
       try:
           predictions = self.model.predict(image_array)
           probabilities = tf.nn.softmax(predictions[0])
           
           detailed_results = []
           for idx, prob in enumerate(probabilities):
               detailed_results.append({
                   'class': self.class_names[idx],
                   'probability': float(prob * 100)  # Convert to percentage
               })
               
           return sorted(detailed_results, key=lambda x: x['probability'], reverse=True)
           
       except Exception as e:
           raise Exception(f"Error getting probabilities: {str(e)}")

   def validate_input(self, image_array):
       """Validate input shape and values"""
       try:
           # Check input shape
           if len(image_array.shape) != 4:
               raise ValueError(f"Expected 4D input (batch, height, width, channels), got shape {image_array.shape}")
           
           # Check value range
           if image_array.min() < 0 or image_array.max() > 1:
               raise ValueError(f"Input values should be in range [0,1], got range [{image_array.min()}, {image_array.max()}]")
               
           # Check data type
           if image_array.dtype != np.float32:
               raise ValueError(f"Expected float32 input, got {image_array.dtype}")
               
           return True
           
       except Exception as e:
           raise Exception(f"Input validation error: {str(e)}")