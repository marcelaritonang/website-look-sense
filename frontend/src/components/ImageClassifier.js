import React, { useState } from 'react';
import { 
  Box, 
  Button, 
  Card, 
  CircularProgress, 
  Typography, 
  LinearProgress 
} from '@mui/material';
import { styled } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { uploadImage } from '../services/api';

const VisuallyHiddenInput = styled('input')`
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  bottom: 0;
  left: 0;
  white-space: nowrap;
  width: 1px;
`;

const ImageClassifier = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setPredictions(null);
    }
  };

  const handleSubmit = async () => {
    if (!selectedImage) return;

    setLoading(true);
    try {
      const result = await uploadImage(selectedImage);
      setPredictions(result.predictions);
    } catch (error) {
      console.error('Error:', error);
      alert('Error predicting image');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ maxWidth: 600, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom align="center">
        Fashion Classifier
      </Typography>

      <Box sx={{ my: 3, textAlign: 'center' }}>
        <Button
          component="label"
          variant="contained"
          startIcon={<CloudUploadIcon />}
        >
          Choose Image
          <VisuallyHiddenInput
            type="file"
            accept="image/*"
            onChange={handleImageChange}
          />
        </Button>
      </Box>

      {preview && (
        <Box sx={{ my: 2, textAlign: 'center' }}>
          <img
            src={preview}
            alt="Preview"
            style={{ maxWidth: '100%', maxHeight: 300, objectFit: 'contain' }}
          />
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={loading}
            sx={{ mt: 2 }}
            fullWidth
          >
            {loading ? <CircularProgress size={24} /> : 'Predict'}
          </Button>
        </Box>
      )}

    {predictions && (
    <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
        Fashion Classification Results
        </Typography>
        {predictions.map((pred, index) => (
        <Box key={index} sx={{ my: 1 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
            <Typography variant="body1">
                {pred.class}
            </Typography>
            <Typography variant="body1">
                {pred.probability > 1 ? pred.probability.toFixed(2) : '< 1'}%
            </Typography>
            </Box>
            <LinearProgress 
            variant="determinate" 
            value={pred.probability} 
            sx={{ 
                height: 8, 
                borderRadius: 1,
                backgroundColor: 'rgba(0,0,0,0.1)',
                '& .MuiLinearProgress-bar': {
                backgroundColor: index === 0 ? '#1976d2' : '#64b5f6'
                }
            }}
            />
        </Box>
        ))}
    </Box>
    )}
    </Card>
  );
};

export default ImageClassifier;