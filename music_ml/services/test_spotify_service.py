import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, session
from music_ml.services.spotify_service import (
    get_auth_headers,
    refresh_token_if_needed,
    search_spotify_tracks,
    get_track_by_id
)

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
                    'artists': [{'id': 'artist_id', 'name': 'Test Artist'}]
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