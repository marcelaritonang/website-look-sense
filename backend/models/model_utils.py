import tensorflow as tf
from config.config import Config
import numpy as np
import json

class FashionClassifier:
    def __init__(self):
        # Baca JSON model
        with open('models/model.json', 'r') as json_file:
            json_string = json_file.read()
            self.model = tf.keras.models.model_from_json(json_string)
            
        # Load weights
        self.model.load_weights(Config.MODEL_PATH)
        
        # Compile model
        self.model.compile(optimizer='adam',
                         loss='sparse_categorical_crossentropy',
                         metrics=['accuracy'])
        
        self.class_names = Config.CLASS_NAMES

    def predict(self, image_array):
        try:
            predictions = self.model.predict(image_array)
            predicted_class_index = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_index])
            predicted_class = self.class_names[predicted_class_index]
            
            return {
                'class': predicted_class,
                'confidence': confidence,
                'class_index': int(predicted_class_index)
            }
        except Exception as e:
            raise Exception(f"Error making prediction: {str(e)}")