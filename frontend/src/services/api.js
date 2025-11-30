import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHotels = async () => {
  try {
    const response = await api.get('/hotels');
    return response.data;
  } catch (error) {
    console.error('API error loading hotels:', error);
    throw error;
  }
};

export const getRecommendations = async (ratings) => {
  try {
    const response = await api.post('/recommend', {
      user_ratings: ratings,
    });
    // backend returns { recommendations: [...] }
    // return the array directly so callers receive an array
    return response.data && response.data.recommendations ? response.data.recommendations : [];
  } catch (error) {
    console.error('API error getting recommendations:', error);
    throw error;
  }
};