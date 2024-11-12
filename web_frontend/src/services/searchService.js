import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

export const searchSongs = async (query, limit = 20) => {
  try {
    const response = await axios.get(`${API_URL}/search`, {
      params: {
        query: query,
        limit: limit,
      },
      headers: {
        'Content-Type': 'application/json',
      }
    });

    return response.data;
  } catch (error) {
    console.error("Error fetching search results:", error.response?.data || error.message);
    throw error;
  }
};