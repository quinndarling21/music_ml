import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, session
from music_ml.services.spotify_service import (
    get_auth_headers,
    refresh_token_if_needed,
    search_spotify_tracks,
    get_track_by_id,
    create_spotify_playlist
)
from music_ml.models.track import Track
from music_ml.models.artist import Artist
from music_ml.models.playlist import Playlist

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret_key'
    return app

def test_get_auth_headers_with_session(app):
    """Test get_auth_headers when session token exists"""
    with app.test_request_context():
        session['access_token'] = 'test_session_token'
        headers = get_auth_headers()
        assert headers['Authorization'] == 'Bearer test_session_token'

@patch('music_ml.services.spotify_service.get_spotify_access_token')
def test_get_auth_headers_without_session(mock_get_token, app):
    """Test get_auth_headers when no session token exists"""
    mock_get_token.return_value = 'test_client_token'
    
    with app.test_request_context():
        headers = get_auth_headers()
        assert headers['Authorization'] == 'Bearer test_client_token'

def test_refresh_token_if_needed_no_refresh_needed(app):
    """Test refresh_token_if_needed when no refresh is needed"""
    response = MagicMock()
    response.status_code = 200
    
    with app.test_request_context():
        new_headers = refresh_token_if_needed(response)
        assert new_headers is None

@patch('music_ml.services.spotify_service.get_spotify_access_token')
def test_refresh_token_if_needed_with_expired_token(mock_get_token, app):
    """Test refresh_token_if_needed when token is expired"""
    mock_get_token.return_value = 'new_token'
    response = MagicMock()
    response.status_code = 401
    
    with app.test_request_context():
        session['access_token'] = 'old_token'
        new_headers = refresh_token_if_needed(response)
        assert new_headers['Authorization'] == 'Bearer new_token'

@patch('music_ml.services.spotify_service.requests.get')
@patch('music_ml.services.spotify_service.get_auth_headers')
def test_search_spotify_tracks_success(mock_get_headers, mock_get, app):
    """Test successful track search"""
    mock_get_headers.return_value = {'Authorization': 'Bearer test_token'}
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'tracks': {
            'items': [
                {
                    'id': 'test_id',
                    'name': 'Test Track',
                    'artists': [{'id': 'artist_id', 'name': 'Test Artist'}],
                    'album': {
                        'images': [
                            {'url': 'large.jpg', 'height': 640, 'width': 640},
                            {'url': 'medium.jpg', 'height': 300, 'width': 300},
                            {'url': 'small.jpg', 'height': 64, 'width': 64}
                        ]
                    }
                }
            ]
        }
    }
    mock_get.return_value = mock_response

    with app.test_request_context():
        tracks = search_spotify_tracks('test query')
        assert len(tracks) == 1
        assert tracks[0].spotify_track_id == 'test_id'
        assert tracks[0].track_name == 'Test Track'
        assert tracks[0].artist.name == 'Test Artist'
        assert tracks[0].artist.spotify_artist_id == 'artist_id'
        assert tracks[0].album_image_url == 'medium.jpg'  # Verify album image URL

@patch('music_ml.services.spotify_service.requests.post')
@patch('music_ml.services.spotify_service.requests.get')
def test_create_spotify_playlist_success(mock_get, mock_post, app):
    """Test successful playlist creation"""
    # Mock user info response
    mock_user_response = MagicMock()
    mock_user_response.status_code = 200
    mock_user_response.json.return_value = {'id': 'test_user_id'}
    mock_get.return_value = mock_user_response
    
    # Mock playlist creation response
    mock_playlist_response = MagicMock()
    mock_playlist_response.status_code = 201
    mock_playlist_response.json.return_value = {
        'id': 'test_playlist_id',
        'external_urls': {'spotify': 'http://test.url'}
    }
    
    # Mock add tracks response
    mock_tracks_response = MagicMock()
    mock_tracks_response.status_code = 201
    
    mock_post.side_effect = [mock_playlist_response, mock_tracks_response]
    
    with app.test_request_context():
        session['access_token'] = 'test_token'
        tracks = [Track(spotify_track_id='test_id', track_name='Test Track', 
                       artist=Artist(name='Test Artist', spotify_artist_id='test_artist_id'))]
        playlist = Playlist(tracks=tracks)
        
        result = create_spotify_playlist('Test Playlist', playlist.tracks)
        assert result['id'] == 'test_playlist_id'
        assert result['external_urls']['spotify'] == 'http://test.url'
        assert isinstance(result['playlist'], Playlist)

def test_create_spotify_playlist_not_authenticated(app):
    """Test playlist creation when not authenticated"""
    with app.test_request_context():
        with pytest.raises(Exception) as exc_info:
            create_spotify_playlist('Test Playlist', [])
        assert 'User not authenticated' in str(exc_info.value)