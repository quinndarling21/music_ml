import pytest
import requests
from unittest.mock import patch, MagicMock, call
from music_ml.services.spotify_service import (
    search_spotify_tracks,
    get_artist_top_tracks,
    get_track_by_id
)

# Mocking the access token retrieval function
@patch('music_ml.services.spotify_service.get_spotify_access_token')
@patch('music_ml.services.spotify_service.requests.get')
def test_search_spotify_tracks_success(mock_requests_get, mock_get_access_token):
    # Mock access token
    mock_get_access_token.return_value = 'mock_access_token'
    
    # Mock successful response from Spotify API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'tracks': {
            'items': [
                {
                    'id': 'track123',
                    'name': 'Test Track',
                    'artists': [{'name': 'Test Artist', 'id':'id'}]
                }
            ]
        }
    }
    mock_requests_get.return_value = mock_response
    
    # Call the function
    result = search_spotify_tracks('test_query', 1)
    
    # Assert that the access token was fetched
    mock_get_access_token.assert_called_once()
    
    # Assert that the request was made with the correct URL
    mock_requests_get.assert_called_once_with(
        'https://api.spotify.com/v1/search?q=test_query&type=track&limit=1',
        headers={'Authorization': 'Bearer mock_access_token'}
    )
    
    # Assert the function returns the expected result
    assert result[0].spotify_track_id == 'track123'
    assert result[0].track_name == 'Test Track'
    assert result[0].artist.name == 'Test Artist'
    assert result[0].artist.spotify_artist_id == 'id'   

# Test for token refresh if the first request fails with 401
@patch('music_ml.services.spotify_service.get_spotify_access_token')
@patch('music_ml.services.spotify_service.requests.get')
def test_search_spotify_tracks_token_refresh(mock_requests_get, mock_get_access_token):
    # Mock initial access token and a refreshed token
    mock_get_access_token.side_effect = ['expired_token', 'refreshed_token']

    # Mock the first response to be 401 Unauthorized
    mock_response_401 = MagicMock()
    mock_response_401.status_code = 401
    
    # Mock the second response to be successful
    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        'tracks': {
            'items': [
                {
                    'id': 'track123',
                    'name': 'Test Track After Refresh',
                    'artists': [{'name': 'Test Artist', 'id':'id'}]
                }
            ]
        }
    }

    # First call returns 401, second call returns 200
    mock_requests_get.side_effect = [mock_response_401, mock_response_200]

    # Call the function
    result = search_spotify_tracks('test_query', 1)
    
    # Assert that the access token was fetched twice (due to refresh)
    assert mock_get_access_token.call_count == 2

    # Assert the second request was made with the refreshed token
    mock_requests_get.assert_called_with(
        'https://api.spotify.com/v1/search?q=test_query&type=track&limit=1',
        headers={'Authorization': 'Bearer refreshed_token'}
    )

    # Assert the function returns the expected result after token refresh
    assert result[0].spotify_track_id == 'track123'
    assert result[0].track_name == 'Test Track After Refresh'
    assert result[0].artist.name == 'Test Artist'

# Test for non-200 responses
@patch('music_ml.services.spotify_service.get_spotify_access_token')
@patch('music_ml.services.spotify_service.requests.get')
def test_search_spotify_tracks_non_200_response(mock_requests_get, mock_get_access_token):
    # Mock access token
    mock_get_access_token.return_value = 'mock_access_token'

    # Mock a non-200 response (e.g., 404 Not Found)
    mock_response = MagicMock()
    mock_response.status_code = 404
    # Set raise_for_status to raise HTTPError when called
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
    mock_requests_get.return_value = mock_response

    # Call the function and expect it to raise an HTTPError exception
    with pytest.raises(requests.exceptions.HTTPError):
        search_spotify_tracks('test_query', 1)

    # Assert that the request was made
    mock_requests_get.assert_called_once_with(
        'https://api.spotify.com/v1/search?q=test_query&type=track&limit=1',
        headers={'Authorization': 'Bearer mock_access_token'}
    )

    # Assert that the access token was fetched
    mock_get_access_token.assert_called_once()

# Test for successful retrieval of artist's top tracks
@patch('music_ml.services.spotify_service.load_spotify_tracks')
@patch('music_ml.services.spotify_service.get_spotify_access_token')
@patch('music_ml.services.spotify_service.requests.get')
def test_get_artist_top_tracks_success(mock_requests_get, mock_get_access_token, mock_load_tracks):
    # Mock access token
    mock_get_access_token.return_value = 'mock_access_token'
    
    # Mock successful response from Spotify API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'tracks': [
            {
                'id': 'track123',
                'name': 'Test Track',
                'artists': [{'name': 'Test Artist', 'id': 'artist_id'}]
            }
        ]
    }
    mock_requests_get.return_value = mock_response
    
    # Call the function
    get_artist_top_tracks('artist123')
    
    # Assert that the access token was fetched
    mock_get_access_token.assert_called_once()
    
    # Assert that the request was made with the correct URL
    mock_requests_get.assert_called_once_with(
        'https://api.spotify.com/v1/artists/artist123/top-tracks?market=US',
        headers={'Authorization': 'Bearer mock_access_token'}
    )
    
    # Assert that load_spotify_tracks was called with the correct data
    mock_load_tracks.assert_called_once_with({'tracks':{'items':mock_response.json.return_value['tracks']}})

# Test for token refresh if the first request fails with 401
@patch('music_ml.services.spotify_service.load_spotify_tracks')
@patch('music_ml.services.spotify_service.get_spotify_access_token')
@patch('music_ml.services.spotify_service.requests.get')
def test_get_artist_top_tracks_token_refresh(mock_requests_get, mock_get_access_token, mock_load_tracks):
    # Mock initial access token and a refreshed token
    mock_get_access_token.side_effect = ['expired_token', 'refreshed_token']
    
    # Mock the first response to be 401 Unauthorized
    mock_response_401 = MagicMock()
    mock_response_401.status_code = 401
    
    # Mock the second response to be successful
    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        'tracks': [
            {
                'id': 'track123',
                'name': 'Test Track After Refresh',
                'artists': [{'name': 'Test Artist', 'id': 'artist_id'}]
            }
        ]
    }
    
    # First call returns 401, second call returns 200
    mock_requests_get.side_effect = [mock_response_401, mock_response_200]
    
    # Call the function
    get_artist_top_tracks('artist123')
    
    # Assert that the access token was fetched twice (due to refresh)
    assert mock_get_access_token.call_count == 2
    
    # Assert the requests were made with the correct URLs and headers
    expected_url = 'https://api.spotify.com/v1/artists/artist123/top-tracks?market=US'
    calls = [
        call(expected_url, headers={'Authorization': 'Bearer expired_token'}),
        call(expected_url, headers={'Authorization': 'Bearer refreshed_token'})
    ]
    mock_requests_get.assert_has_calls(calls)
    
    # Assert that load_spotify_tracks was called with the correct data after token refresh
    {'tracks':{'items':mock_response_200.json.return_value['tracks']}}
    mock_load_tracks.assert_called_once_with({'tracks':{'items':mock_response_200.json.return_value['tracks']}})

# Test for non-200 responses
@patch('music_ml.services.spotify_service.load_spotify_tracks')
@patch('music_ml.services.spotify_service.get_spotify_access_token')
@patch('music_ml.services.spotify_service.requests.get')
def test_get_artist_top_tracks_non_200_response(mock_requests_get, mock_get_access_token, mock_load_tracks):
    # Mock access token
    mock_get_access_token.return_value = 'mock_access_token'
    
    # Mock a non-200 response (e.g., 404 Not Found)
    mock_response = MagicMock()
    mock_response.status_code = 404
    # Set raise_for_status to raise HTTPError when called
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
    mock_requests_get.return_value = mock_response
    
    # Call the function and expect it to raise an HTTPError exception
    with pytest.raises(requests.exceptions.HTTPError):
        get_artist_top_tracks('artist123')
    
    # Assert that the request was made
    mock_requests_get.assert_called_once_with(
        'https://api.spotify.com/v1/artists/artist123/top-tracks?market=US',
        headers={'Authorization': 'Bearer mock_access_token'}
    )
    
    # Assert that the access token was fetched
    mock_get_access_token.assert_called_once()
    
    # Assert that load_spotify_tracks was not called
    mock_load_tracks.assert_not_called()

@patch('music_ml.services.spotify_service.load_spotify_tracks')
@patch('music_ml.services.spotify_service.get_spotify_access_token')
@patch('music_ml.services.spotify_service.requests.get')
def test_get_track_by_id_success(mock_requests_get, mock_get_access_token, mock_load_tracks):
    # Mock access token
    mock_get_access_token.return_value = 'mock_access_token'

    # Mock successful response from Spotify API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
                'id': 'track123',
                'name': 'Test Track',
                'artists': [{'name': 'Test Artist', 'id': 'artist_id'}]
    }
    mock_requests_get.return_value = mock_response

    # Mock the load_spotify_tracks function to return a Track object
    mock_track = MagicMock()
    mock_load_tracks.return_value = [mock_track]

    # Call the function
    result = get_track_by_id('track123')

    # Assert that the access token was fetched
    mock_get_access_token.assert_called_once()

    # Assert that the request was made with the correct URL
    mock_requests_get.assert_called_once_with(
        'https://api.spotify.com/v1/tracks/track123',
        headers={'Authorization': 'Bearer mock_access_token'}
    )

    # Assert that load_spotify_tracks was called with the correct data
    mock_load_tracks.assert_called_once_with({'tracks':{'items':[mock_response.json.return_value]}})

    # Assert that the result is the Track object returned by load_spotify_tracks
    assert result == mock_track

# Test for token refresh if the first request fails with 401
@patch('music_ml.services.spotify_service.load_spotify_tracks')
@patch('music_ml.services.spotify_service.get_spotify_access_token')
@patch('music_ml.services.spotify_service.requests.get')
def test_get_track_by_id_token_refresh(mock_requests_get, mock_get_access_token, mock_load_tracks):
    # Mock initial access token and a refreshed token
    mock_get_access_token.side_effect = ['expired_token', 'refreshed_token']

    # Mock the first response to be 401 Unauthorized
    mock_response_401 = MagicMock()
    mock_response_401.status_code = 401

    # Mock the second response to be successful
    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        'id': 'track123',
        'name': 'Test Track After Refresh',
        'artists': [{'name': 'Test Artist', 'id': 'artist_id'}]
    }

    # First call returns 401, second call returns 200
    mock_requests_get.side_effect = [mock_response_401, mock_response_200]

    # Mock the load_spotify_tracks function to return a Track object
    mock_track = MagicMock()
    mock_load_tracks.return_value = [mock_track]

    # Call the function
    result = get_track_by_id('track123')

    # Assert that the access token was fetched twice (due to refresh)
    assert mock_get_access_token.call_count == 2

    # Assert the requests were made with the correct URLs and headers
    expected_url = 'https://api.spotify.com/v1/tracks/track123'
    calls = [
        call(expected_url, headers={'Authorization': 'Bearer expired_token'}),
        call(expected_url, headers={'Authorization': 'Bearer refreshed_token'})
    ]
    mock_requests_get.assert_has_calls(calls)

    # Assert that load_spotify_tracks was called with the correct data after token refresh
    mock_load_tracks.assert_called_once_with({'tracks':{'items':[mock_response_200.json.return_value]}})

    # Assert that the result is the Track object returned by load_spotify_tracks
    assert result == mock_track

# Test for non-200 responses
@patch('music_ml.services.spotify_service.load_spotify_tracks')
@patch('music_ml.services.spotify_service.get_spotify_access_token')
@patch('music_ml.services.spotify_service.requests.get')
def test_get_track_by_id_non_200_response(mock_requests_get, mock_get_access_token, mock_load_tracks):
    # Mock access token
    mock_get_access_token.return_value = 'mock_access_token'

    # Mock a non-200 response (e.g., 404 Not Found)
    mock_response = MagicMock()
    mock_response.status_code = 404
    # Set raise_for_status to raise HTTPError when called
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('404 Client Error: Not Found for url')
    mock_requests_get.return_value = mock_response

    # Call the function and expect it to raise an HTTPError exception
    with pytest.raises(requests.exceptions.HTTPError):
        get_track_by_id('nonexistent_track_id')

    # Assert that the request was made
    mock_requests_get.assert_called_once_with(
        'https://api.spotify.com/v1/tracks/nonexistent_track_id',
        headers={'Authorization': 'Bearer mock_access_token'}
    )

    # Assert that the access token was fetched
    mock_get_access_token.assert_called_once()

    # Assert that load_spotify_tracks was not called
    mock_load_tracks.assert_not_called()