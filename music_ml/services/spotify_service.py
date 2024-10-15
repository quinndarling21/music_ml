import requests
from music_ml.utils.spotify_utils import get_spotify_access_token

def search_spotify_tracks(query, limit=20):
    """Function to search tracks from Spotify API."""
    # Spotify Search API URL
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit={limit}"

    # Get access token
    access_token = get_spotify_access_token()

    # Set headers for Spotify API request
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    # Check if token expired and refresh if necessary
    if response.status_code == 401:
        access_token = get_spotify_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

    # Handle response
    if response.status_code == 200:
        return response.json()
    
    # Raise an exception for non-200 responses
    response.raise_for_status()