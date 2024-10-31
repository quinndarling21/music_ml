import pytest
import requests
from flask import Flask
from unittest.mock import patch, MagicMock
from music_ml.api.generate_playlist import playlist_bp
from music_ml.models.track import Track
from music_ml.models.artist import Artist
from music_ml.models.playlist import Playlist

@pytest.fixture
def client():
    # Create a test Flask app and register the blueprint
    app = Flask(__name__)
    app.register_blueprint(playlist_bp)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@patch('music_ml.api.generate_playlist.get_track_by_id')
@patch('music_ml.api.generate_playlist.ArtistMatcher')
def test_generate_playlist_success(mock_artist_matcher_class, mock_get_track_by_id, client):
    # Mock the get_track_by_id to return an input track
    input_track = Track(
        spotify_track_id='track1',
        track_name='Input Track',
        artist=Artist(spotify_artist_id='artist123', name='Test Artist')
    )
    mock_get_track_by_id.return_value = input_track

    # Mock the matcher's match method to return mock tracks
    mock_artist_matcher = MagicMock()
    mock_track_1 = Track(
        spotify_track_id='track2',
        track_name='Test Track 2',
        artist=Artist(spotify_artist_id='artist123', name='Test Artist')
    )
    mock_track_2 = Track(
        spotify_track_id='track3',
        track_name='Test Track 3',
        artist=Artist(spotify_artist_id='artist123', name='Test Artist')
    )
    mock_track_3 = Track(
        spotify_track_id='track4',
        track_name='Test Track 4',
        artist=Artist(spotify_artist_id='artist123', name='Test Artist')
    )
    # Mock the match method to return matching tracks
    mock_matching_tracks = [mock_track_1, mock_track_2, mock_track_3]
    mock_artist_matcher.match.return_value = mock_matching_tracks
    mock_artist_matcher_class.return_value = mock_artist_matcher

    # Make a GET request to the /generate_playlist endpoint
    response = client.get('/generate_playlist?spotify_track_id=track1')

    # Check that the response is 200 OK
    assert response.status_code == 200

    # Parse the JSON response
    json_data = response.get_json()

    # Assert that the response contains the expected playlist data
    playlist_data = json_data['playlist']
    tracks = playlist_data['tracks']
    assert len(tracks) == 4  # Original track + 3 matching tracks
    assert tracks[0]['spotify_track_id'] == 'track1'  # Original track
    assert tracks[1]['spotify_track_id'] == 'track2'
    assert tracks[2]['spotify_track_id'] == 'track3'
    assert tracks[3]['spotify_track_id'] == 'track4'

@patch('music_ml.api.generate_playlist.get_track_by_id')
def test_generate_playlist_missing_track_id(mock_get_track_by_id, client):
    # Send a GET request without 'spotify_track_id' in the query parameters
    response = client.get('/generate_playlist')

    # Check that the response is 400 Bad Request
    assert response.status_code == 400

    # Parse the JSON response
    json_data = response.get_json()

    # Assert that the error message is returned
    assert json_data['error'] == 'spotify_track_id is required'

@patch('music_ml.api.generate_playlist.get_track_by_id')
def test_generate_playlist_api_error(mock_get_track_by_id, client):
    # Mock get_track_by_id to raise an exception
    mock_get_track_by_id.side_effect = Exception('Spotify API error')

    # Make a GET request to the /generate_playlist endpoint
    response = client.get('/generate_playlist?spotify_track_id=track1')

    # Check that the response is 500 Internal Server Error
    assert response.status_code == 500

    # Parse the JSON response
    json_data = response.get_json()

    # Assert that the error message is returned
    assert 'error' in json_data
    assert json_data['error'] == 'Spotify API error'