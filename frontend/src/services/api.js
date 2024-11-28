const API_URL = 'http://localhost:5000/api';

export const predictImage = async (imageFile) => {
    try {
        const formData = new FormData();
        formData.append('image', imageFile);

        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Prediction failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Error predicting image:', error);
        throw error;
    }
};

export const checkHealth = async () => {
    try {
        const response = await fetch(`${API_URL}/health`);
        return await response.json();
    } catch (error) {
        console.error('Error checking health:', error);
        throw error;
    }
};