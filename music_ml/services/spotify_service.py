from flask import session
import requests
from typing import List, Optional
from music_ml.models.track import Track
from music_ml.utils.spotify_utils import get_spotify_access_token, load_spotify_tracks

def get_auth_headers() -> dict:
    """Get headers with user token if available, otherwise use client credentials"""
    if 'access_token' in session:
        return {"Authorization": f"Bearer {session['access_token']}"}
    else:
        access_token = get_spotify_access_token()
        return {"Authorization": f"Bearer {access_token}"}

def refresh_token_if_needed(response: requests.Response) -> Optional[dict]:
    """Refresh token if expired and return new headers"""
    if response.status_code == 401 and 'access_token' in session:
        # TODO: Implement token refresh logic
        # For now, we'll fall back to client credentials
        access_token = get_spotify_access_token()
        return {"Authorization": f"Bearer {access_token}"}
    return None

def search_spotify_tracks(query, limit=20) -> List[Track]:
    """Function to search tracks from Spotify API."""
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit={limit}"
    
    headers = get_auth_headers()
    response = requests.get(url, headers=headers)

    # Handle token refresh if needed
    new_headers = refresh_token_if_needed(response)
    if new_headers:
        response = requests.get(url, headers=new_headers)

    if response.status_code == 200:
        return load_spotify_tracks(response.json())
    
    response.raise_for_status()

def get_artist_top_tracks(artist_id) -> List[Track]:
    """Get top tracks of an artist from Spotify API."""
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"

    access_token = get_spotify_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    # Refresh token if expired
    if response.status_code == 401:
        access_token = get_spotify_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

    # Handle response
    if response.status_code == 200:
        tracks = load_spotify_tracks({'tracks':{'items':response.json()['tracks']}})
        return tracks
    else:
        response.raise_for_status()

def get_track_by_id(spotify_track_id) -> Track:
    """Retrieve a single track from Spotify API by its ID."""
    url = f"https://api.spotify.com/v1/tracks/{spotify_track_id}"

    access_token = get_spotify_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    # Refresh token if expired
    if response.status_code == 401:
        access_token = get_spotify_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

    # Handle response
    if response.status_code == 200:
        track_data = {'tracks':{'items':[response.json()]}}
        return load_spotify_tracks(track_data)[0]
    else:
        response.raise_for_status()