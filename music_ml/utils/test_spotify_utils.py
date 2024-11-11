import os
from music_ml.utils.spotify_utils import (
    get_spotify_access_token,
    load_spotify_artist,
    load_spotify_tracks
)
from music_ml.models.artist import Artist
from music_ml.models.track import Track

from dotenv import load_dotenv
import pytest

# Mock success and error responses for the Spotify API
class MockResponseSuccess:
    status_code = 200

    def json(self):
        return {"access_token": "test_token"}

class MockResponseError:
    status_code = 401

    def json(self):
        return {"error": "invalid_client", "error_description": "Invalid client secret"}
    
    @property
    def text(self):
        return "Invalid client secret"

# Fixture to load environment variables and provide common setup
@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    # Load the environment variables from the .env file
    load_dotenv()

    # Mock environment variables
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "fake_client_id")
    monkeypatch.setenv("SPOTIFY_CLIENT_SECRET", "fake_client_secret")

# Helper function to mock requests.post in different test cases
def mock_spotify_api(monkeypatch, response):
    """
    Helper function to mock the Spotify API with a given response.
    """
    def mock_post(url, headers, data):
        return response
    
    monkeypatch.setattr('requests.post', mock_post)

# Test case for successful token retrieval
def test_get_spotify_access_token_success(monkeypatch):
    # Mock the successful response
    mock_spotify_api(monkeypatch, MockResponseSuccess())

    # Test the access token retrieval
    access_token = get_spotify_access_token()
    assert access_token == "test_token"

# Test case for failed token retrieval
def test_get_spotify_access_token_error(monkeypatch):
    # Mock the error response
    mock_spotify_api(monkeypatch, MockResponseError())

    # Test that an exception is raised on error
    with pytest.raises(Exception) as exc_info:
        get_spotify_access_token()

    assert "Failed to retrieve access token" in str(exc_info.value)

def test_load_spotify_artist():
    artist_json = {'name': 'Test Artist', 'id':'id'}
    artist = load_spotify_artist(artist_json)
    assert artist == Artist(name='Test Artist', spotify_artist_id='id')

def test_load_spotify_tracks_with_images():
    """Test loading tracks with album images"""
    search_response_json = {
        'tracks': {
            'items': [
                {
                    'id': 'track123',
                    'name': 'Test Track',
                    'artists': [{'name': 'Test Artist', 'id':'id'}],
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
    tracks = load_spotify_tracks(search_response_json)
    assert tracks[0].spotify_track_id == 'track123'
    assert tracks[0].track_name == 'Test Track'
    assert tracks[0].artist.name == 'Test Artist'
    assert tracks[0].artist.spotify_artist_id == 'id'
    assert tracks[0].album_image_url == 'medium.jpg'  # Should select medium size image

def test_load_spotify_tracks_with_single_image():
    """Test loading tracks with only one album image"""
    search_response_json = {
        'tracks': {
            'items': [
                {
                    'id': 'track123',
                    'name': 'Test Track',
                    'artists': [{'name': 'Test Artist', 'id':'id'}],
                    'album': {
                        'images': [
                            {'url': 'large.jpg', 'height': 640, 'width': 640}
                        ]
                    }
                }
            ]
        }
    }
    tracks = load_spotify_tracks(search_response_json)
    assert tracks[0].album_image_url == 'large.jpg'  # Should fallback to available image

def test_load_spotify_tracks_without_images():
    """Test loading tracks without album images"""
    search_response_json = {
        'tracks': {
            'items': [
                {
                    'id': 'track123',
                    'name': 'Test Track',
                    'artists': [{'name': 'Test Artist', 'id':'id'}],
                    'album': {
                        'images': []
                    }
                }
            ]
        }
    }
    tracks = load_spotify_tracks(search_response_json)
    assert tracks[0].album_image_url is None  # Should handle missing images gracefully