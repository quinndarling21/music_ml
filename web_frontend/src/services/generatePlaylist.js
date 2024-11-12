import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

export const generatePlaylist = async (spotifyTrackId) => {
  try {
    const response = await axios.get(`${API_URL}/generate_playlist`, {
      params: {
        spotify_track_id: spotifyTrackId,
      },
      headers: {
        'Content-Type': 'application/json',
      }
    });

    return response.data;
  } catch (error) {
    console.error("Error generating playlist:", error.response?.data || error.message);
    throw error;
  }
};

export const exportPlaylist = async (tracks) => {
  try {
    const response = await axios.post(
      `${API_URL}/api/auth/export-playlist`,
      { tracks },
      {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error exporting playlist:", error.response?.data || error.message);
    throw error;
  }
};