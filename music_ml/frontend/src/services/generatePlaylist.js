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

export const exportPlaylist = async (tracks) => {
  try {
    const response = await axios.post(
      "http://127.0.0.1:5000/api/auth/export-playlist",
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