import pytest
import requests
from flask import Flask
from music_ml.api.search import search_bp
from unittest.mock import patch
from music_ml.models.track import Track
from music_ml.models.artist import Artist


@pytest.fixture
def client():
    # Create a test Flask app and register the blueprint
    app = Flask(__name__)
    app.register_blueprint(search_bp)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@patch('music_ml.api.search.search_spotify_tracks')
def test_search_tracks_success(mock_search_spotify_tracks, client):
    # Mock the response from the search_spotify_tracks function
    mock_search_spotify_tracks.return_value = [
        Track(
            spotify_track_id='track123',
            track_name='Test Track',
            artist=Artist(spotify_artist_id='id', name='Test Artist')
        )
    ]

    # Make a request to the /search endpoint
    response = client.get('/search?query=test&limit=1')

    # Check that the response is 200 OK
    assert response.status_code == 200

    # Parse the JSON response
    json_data = response.get_json()

    # Assert that the response contains the expected data
    assert json_data['tracks'][0]['spotify_track_id'] == 'track123'
    assert json_data['tracks'][0]['track_name'] == 'Test Track'
    assert json_data['tracks'][0]['artist']['name'] == 'Test Artist'
    assert json_data['total_results'] == 1

@patch('music_ml.api.search.search_spotify_tracks')
def test_search_tracks_missing_query(mock_search_spotify_tracks, client):
    # Test the case where query is missing
    response = client.get('/search')

    # Check that the response is 400 Bad Request
    assert response.status_code == 400

    # Parse the JSON response
    json_data = response.get_json()

    # Assert that the error message is returned
    assert json_data['error'] == 'Query parameter is required'

@patch('music_ml.api.search.search_spotify_tracks')
def test_search_tracks_api_error(mock_search_spotify_tracks, client):
    # Simulate an error when calling the Spotify API
    mock_search_spotify_tracks.side_effect = requests.exceptions.RequestException("Spotify API error")

    # Make a request to the /search endpoint
    response = client.get('/search?query=test')

    # Check that the response is 500 Internal Server Error
    assert response.status_code == 500

    # Parse the JSON response
    json_data = response.get_json()

    # Assert that the error message is returned
    assert 'error' in json_data
    assert json_data['error'] == "Spotify API error"