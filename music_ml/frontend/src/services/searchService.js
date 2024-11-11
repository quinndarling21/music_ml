import axios from 'axios';

export const searchSongs = async (query, limit = 10) => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/search", {
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