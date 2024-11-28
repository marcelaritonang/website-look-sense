import React, { useState, useEffect } from 'react';
import * as tf from '@tensorflow/tfjs';

const ImageClassifier = () => {
  const [model, setModel] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const classes = [
    "Bags",
    "Bottomwear",
    "Dress",
    "Headwear",
    "Shoes",
    "Topwear",
    "Watches"
  ];

  useEffect(() => {
    loadModel();
  }, []);

  const loadModel = async () => {
    try {
      setIsLoading(true);
      const loadedModel = await tf.loadGraphModel('/model/model.json');
      setModel(loadedModel);
      console.log('Model loaded successfully');
    } catch (error) {
      console.error('Error loading model:', error);
      setError('Failed to load model');
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => setImageUrl(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const preprocessImage = async (imageElement) => {
    return tf.tidy(() => {
      return tf.browser.fromPixels(imageElement)
        .resizeBilinear([128, 128])
        .expandDims()
        .toFloat()
        .div(255.0);
    });
  };

  const handlePredict = async () => {
    if (!model || !imageUrl) return;

    try {
      setIsLoading(true);
      setPrediction(null);
      setError(null);

      // Create image element
      const imageElement = document.createElement('img');
      imageElement.src = imageUrl;
      
      await new Promise((resolve) => {
        imageElement.onload = resolve;
      });

      // Preprocess and predict
      const tensor = await preprocessImage(imageElement);
      const predictions = await model.predict(tensor);
      const data = await predictions.data();

      // Apply softmax
      const softmax = tf.softmax(tf.tensor(data));
      const probabilities = await softmax.data();

      // Get results
      const maxProbability = Math.max(...probabilities);
      const classIndex = probabilities.indexOf(maxProbability);

      setPrediction({
        class: classes[classIndex],
        confidence: maxProbability * 100,
        allProbabilities: classes.map((cls, idx) => ({
          class: cls,
          probability: probabilities[idx] * 100
        }))
      });

      // Cleanup
      tensor.dispose();
      predictions.dispose();
      softmax.dispose();
    } catch (error) {
      console.error('Error during prediction:', error);
      setError('Error making prediction');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Fashion Classifier</h1>
      
      <div className="mb-4">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="mb-2"
        />
      </div>

      {imageUrl && (
        <div className="my-4">
          <img
            src={imageUrl}
            alt="Preview"
            className="max-w-sm rounded shadow"
          />
        </div>
      )}

      <button
        onClick={handlePredict}
        disabled={!model || !imageUrl || isLoading}
        className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-300 mb-4"
      >
        {isLoading ? 'Processing...' : 'Predict'}
      </button>

      {error && (
        <div className="text-red-500 mb-4">{error}</div>
      )}

      {prediction && (
        <div className="border rounded p-4">
          <h2 className="text-xl font-semibold mb-2">Results:</h2>
          <p className="mb-2">
            Predicted Class: <strong>{prediction.class}</strong>
          </p>
          <p className="mb-4">
            Confidence: <strong>{prediction.confidence.toFixed(2)}%</strong>
          </p>
          
          <h3 className="font-semibold mb-2">All Probabilities:</h3>
          <div className="space-y-1">
            {prediction.allProbabilities.map(({ class: className, probability }) => (
              <div key={className} className="flex justify-between">
                <span>{className}:</span>
                <span>{probability.toFixed(2)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageClassifier;