import axios from 'axios';

export const generatePlaylist = async (spotifyTrackId) => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/generate_playlist", {
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