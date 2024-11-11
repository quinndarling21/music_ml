import pytest
from flask import Flask, session
from unittest.mock import patch, MagicMock
from music_ml.api.auth import auth_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret_key'
    app.config['TESTING'] = True
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_endpoint(client):
    """Test that login endpoint returns correct Spotify authorization URL"""
    response = client.get('/api/auth/login')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'auth_url' in data
    assert 'accounts.spotify.com/authorize' in data['auth_url']
    assert 'client_id=' in data['auth_url']
    assert 'scope=' in data['auth_url']

def test_callback_error(client):
    """Test callback endpoint with error parameter"""
    response = client.get('/api/auth/callback?error=access_denied')
    assert response.status_code == 400
    
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'access_denied'

@patch('music_ml.api.auth.requests.post')
def test_callback_success(mock_post, client):
    """Test successful callback flow"""
    # Mock the token response from Spotify
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'access_token': 'test_access_token',
        'refresh_token': 'test_refresh_token',
        'expires_in': 3600
    }
    mock_post.return_value = mock_response

    # Test the callback endpoint
    response = client.get('/api/auth/callback?code=test_code')
    assert response.status_code == 302  # Redirect status code
    
    # Check that session was updated
    with client.session_transaction() as sess:
        assert sess['access_token'] == 'test_access_token'
        assert sess['refresh_token'] == 'test_refresh_token'
        assert sess['token_expiry'] == 3600

def test_check_auth_authenticated(client):
    """Test check_auth when user is authenticated"""
    with client.session_transaction() as sess:
        sess['access_token'] = 'test_token'

    response = client.get('/api/auth/check-auth')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['authenticated'] is True

def test_check_auth_not_authenticated(client):
    """Test check_auth when user is not authenticated"""
    response = client.get('/api/auth/check-auth')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['authenticated'] is False

def test_logout(client):
    """Test logout endpoint"""
    with client.session_transaction() as sess:
        sess['access_token'] = 'test_token'
        sess['refresh_token'] = 'test_refresh'

    response = client.get('/api/auth/logout')
    assert response.status_code == 200
    
    # Verify session is cleared
    with client.session_transaction() as sess:
        assert 'access_token' not in sess
        assert 'refresh_token' not in sess 