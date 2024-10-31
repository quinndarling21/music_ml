import os
import requests
from dotenv import load_dotenv
from base64 import b64encode
import json
from typing import List

from music_ml.models.track import Track
from music_ml.models.artist import Artist


# Load environment variables from the .env file
load_dotenv()

# Fetch Spotify credentials from environment variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_spotify_access_token():
    """
    Request a new Spotify access token using the Client Credentials Flow.
    """
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        raise EnvironmentError("Spotify Client ID or Secret not set in environment variables")

    # Spotify token URL
    auth_url = "https://accounts.spotify.com/api/token"
    
    # Prepare the authorization header by encoding client_id:client_secret in Base64
    auth_header = b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Data for requesting access token
    data = {
        "grant_type": "client_credentials"
    }
    
    # Make the request to get the access token
    response = requests.post(auth_url, headers=headers, data=data)
    
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        raise Exception(f"Failed to retrieve access token: {response.status_code} - {response.text}")
    
def load_spotify_artist(spotify_artist_json: json) -> Artist:
    return Artist(
        name=spotify_artist_json['name'],
        spotify_artist_id=spotify_artist_json['id']
    )
    
def load_spotify_tracks(spotify_response_json: json) -> List[Track]:
    tracks = [
            Track(
                spotify_track_id=item['id'],
                track_name=item['name'],
                artist=load_spotify_artist(item['artists'][0]),
                genre="",  # Spotify API doesn't return genre directly, so you may add a placeholder
                tempo=0.0,  # Placeholder, update if this info is available
                energy=0.0,
                valence=0.0,
                danceability=0.0
            )
            for item in spotify_response_json['tracks']['items']
        ]
    return tracks