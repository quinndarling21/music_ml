import os
from flask import Blueprint, redirect, request, session, url_for, jsonify
import requests
from urllib.parse import urlencode
import logging
from dotenv import load_dotenv
from music_ml.models.track import Track
from music_ml.models.artist import Artist
from music_ml.models.playlist import Playlist
from music_ml.services.spotify_service import create_spotify_playlist

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)  # Force reload environment variables

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Get these from your Spotify Developer Dashboard
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
FRONTEND_URL = os.getenv('FRONTEND_URL')

@auth_bp.route('/login')
def login():
    """Redirect users to Spotify's authorization page"""
    if not CLIENT_ID:
        logger.error("SPOTIFY_CLIENT_ID not set")
        return jsonify({'error': 'Spotify client ID not configured'}), 500
    
    if not REDIRECT_URI:
        logger.error("SPOTIFY_REDIRECT_URI not set")
        return jsonify({'error': 'Redirect URI not configured'}), 500
        
    # Debug log the environment variables
    logger.debug(f"Using CLIENT_ID: {CLIENT_ID}")
    logger.debug(f"Using REDIRECT_URI: {REDIRECT_URI}")
    
    scope = 'playlist-modify-public playlist-modify-private'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }
    
    auth_url = f'https://accounts.spotify.com/authorize?{urlencode(params)}'
    logger.debug(f"Generated auth URL: {auth_url}")
    return jsonify({'auth_url': auth_url})

@auth_bp.route('/callback')
def callback():
    """Handle the callback from Spotify"""
    error = request.args.get('error')
    code = request.args.get('code')
    
    logger.debug(f"Callback received - Code: {code}, Error: {error}")
    logger.debug(f"Environment variables - REDIRECT_URI: {REDIRECT_URI}, FRONTEND_URL: {FRONTEND_URL}")
    
    if error:
        logger.error(f"Spotify auth error: {error}")
        return redirect(f"{FRONTEND_URL}/callback?error={error}")

    if not code:
        logger.error("No code received from Spotify")
        return redirect(f"{FRONTEND_URL}/callback?error=no_code")

    try:
        # Exchange the code for access token
        token_url = 'https://accounts.spotify.com/api/token'
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }

        logger.debug(f"Making token request with payload: {payload}")
        
        response = requests.post(token_url, data=payload)
        logger.debug(f"Token response status: {response.status_code}")
        logger.debug(f"Token response content: {response.text}")
        
        response.raise_for_status()
        token_info = response.json()
        
        # Store tokens in session
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['token_expiry'] = token_info['expires_in']

        logger.debug("Successfully stored tokens in session")
        
        # Redirect to frontend with success
        redirect_url = f"{FRONTEND_URL}/callback?success=true"
        logger.debug(f"Redirecting to: {redirect_url}")
        return redirect(redirect_url)

    except requests.exceptions.RequestException as e:
        logger.error(f"Token exchange error: {str(e)}")
        logger.error(f"Response content: {getattr(response, 'text', 'No response content')}")
        return redirect(f"{FRONTEND_URL}/callback?error=token_exchange_failed")
    except Exception as e:
        logger.error(f"Unexpected error in callback: {str(e)}", exc_info=True)
        return redirect(f"{FRONTEND_URL}/callback?error=unexpected_error")

@auth_bp.route('/check-auth')
def check_auth():
    """Check if user is authenticated"""
    is_authenticated = 'access_token' in session
    logging.info(f"Auth check - authenticated: {is_authenticated}")
    return jsonify({'authenticated': is_authenticated})

@auth_bp.route('/logout')
def logout():
    """Clear user session"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@auth_bp.route('/me')
def get_user_info():
    """Get authenticated user's Spotify profile"""
    if 'access_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to get user info'}), response.status_code

@auth_bp.route('/export-playlist', methods=['POST'])
def export_playlist():
    """Export a playlist to user's Spotify account"""
    if 'access_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    if not data or 'tracks' not in data:
        return jsonify({'error': 'No tracks provided'}), 400
    
    try:
        # Convert the JSON data back to Track objects
        tracks = []
        for track_data in data['tracks']:
            artist_data = track_data.pop('artist')
            artist = Artist(**artist_data)
            track = Track(artist=artist, **track_data)
            tracks.append(track)
        
        # Create a Playlist object
        playlist = Playlist(tracks=tracks)
        
        # Generate playlist name based on seed track
        playlist_name = f"Inspired by {playlist.tracks[0].track_name}"
        description = f"A playlist inspired by {playlist.tracks[0].track_name} by {playlist.tracks[0].artist.name}"
        
        # Create the playlist
        result = create_spotify_playlist(playlist_name, playlist.tracks, description)
        
        return jsonify({
            'success': True,
            'playlist_url': result['external_urls']['spotify']
        })
        
    except Exception as e:
        logging.error(f"Failed to export playlist: {str(e)}")
        return jsonify({'error': str(e)}), 500