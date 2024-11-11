from flask import session
import requests
from typing import List, Optional
from music_ml.models.track import Track
from music_ml.models.playlist import Playlist
from music_ml.utils.spotify_utils import get_spotify_access_token, load_spotify_tracks

# Configure request timeouts
TIMEOUT = 10  # seconds

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

def create_spotify_playlist(name: str, tracks: List[Track], description: str = None) -> dict:
    """Create a new playlist in user's Spotify account and add tracks to it."""
    if 'access_token' not in session:
        raise Exception('User not authenticated')

    headers = {
        "Authorization": f"Bearer {session['access_token']}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get user ID first
        user_response = requests.get(
            'https://api.spotify.com/v1/me',
            headers=headers,
            timeout=TIMEOUT
        )
        user_response.raise_for_status()
        user_id = user_response.json()['id']
        
        # Create playlist
        create_url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
        playlist_data = {
            'name': name,
            'description': description or 'Created by Musaic',
            'public': True
        }
        
        playlist_response = requests.post(
            create_url,
            json=playlist_data,
            headers=headers,
            timeout=TIMEOUT
        )
        playlist_response.raise_for_status()
        playlist_info = playlist_response.json()
        playlist_id = playlist_info['id']
        
        # Add tracks in batches of 50 (Spotify's limit)
        tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        track_uris = [f"spotify:track:{track.spotify_track_id}" for track in tracks]
        
        # Split tracks into batches
        batch_size = 50
        for i in range(0, len(track_uris), batch_size):
            batch = track_uris[i:i + batch_size]
            add_tracks_response = requests.post(
                tracks_url,
                json={'uris': batch},
                headers=headers,
                timeout=TIMEOUT
            )
            add_tracks_response.raise_for_status()
        
        # Create a Playlist object
        playlist = Playlist(tracks=tracks)
        
        # Add the Spotify URL and playlist object to the response
        response = {
            'id': playlist_info['id'],
            'external_urls': playlist_info['external_urls'],
            'playlist': playlist
        }
        
        return response
        
    except requests.Timeout:
        raise Exception('Request timed out while creating playlist. Please try again.')
    except requests.RequestException as e:
        error_message = str(e)
        try:
            error_data = e.response.json()
            if 'error' in error_data:
                error_message = error_data['error'].get('message', str(e))
        except:
            pass
        raise Exception(f'Failed to create playlist: {error_message}')