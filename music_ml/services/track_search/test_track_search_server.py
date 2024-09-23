import pytest
import grpc
from music_ml.protobuf.services.track_search.track_search_pb2 import (
    TrackSearchRequest, 
    TrackSearchResponse,
)
from music_ml.services.track_search.track_search_server import (
    TrackSearchService
)
from music_ml.utils.spotify_utils import get_spotify_access_token
from music_ml.protobuf.common.track_pb2 import Track

# Mock Spotify API success response
def mock_spotify_api_success(*args, **kwargs):
    class MockResponse:
        status_code = 200
        def json(self):
            return {
                "name": "Mock Song",
                "artists": [{"name": "Mock Artist"}],
                "tempo": 120.0,
                "energy": 0.8,
                "valence": 0.6,
                "danceability": 0.7
            }
    return MockResponse()

# Mock Spotify API error response
def mock_spotify_api_error(*args, **kwargs):
    class MockResponse:
        status_code = 401
        def json(self):
            return {"error": "invalid_token", "error_description": "The access token expired"}
        @property
        def text(self):
            return "Invalid token"
    return MockResponse()

# Mock the gRPC context object
class MockContext:
    def abort(self, code, details):
        raise Exception(f"gRPC aborted: {code.name} - {details}")
    
    def is_active(self):
        return True  # Simulate an active context

    def time_remaining(self):
        return 100  # Simulate time remaining for gRPC call

@pytest.fixture
def track_search_service():
    return TrackSearchService()

@pytest.fixture(autouse=True)
def mock_spotify_token(monkeypatch):
    """
    This fixture automatically mocks the get_spotify_access_token function
    for all tests, returning a static token value.
    """
    monkeypatch.setattr("music_ml.utils.spotify_utils.get_spotify_access_token", lambda: "test_token")

def test_search_track_success(track_search_service, monkeypatch):
    # Mock the Spotify API call to return a success response
    monkeypatch.setattr("requests.get", mock_spotify_api_success)

    # Create a TrackSearchRequest
    request = TrackSearchRequest(spotify_track_id="valid_id")
    context = MockContext()

    # Call the SearchTrack method
    response = track_search_service.SearchTrack(request, context)

    # Assert that the response contains the expected track information
    assert response.track.track_name == "Mock Song"
    assert response.track.artist == "Mock Artist"
    assert response.track.tempo == pytest.approx(120.0)
    assert response.track.energy == pytest.approx(0.8)  # Use approx for floating-point precision
    assert response.track.valence == pytest.approx(0.6)
    assert response.track.danceability == pytest.approx(0.7)

def test_search_track_error(track_search_service, monkeypatch):
    # Mock the Spotify API call to return an error response
    monkeypatch.setattr("requests.get", mock_spotify_api_error)

    # Create a TrackSearchRequest
    request = TrackSearchRequest(spotify_track_id="invalid_id")
    context = MockContext()

    # Call the SearchTrack method and expect a gRPC exception due to API failure
    with pytest.raises(Exception) as excinfo:
        track_search_service.SearchTrack(request, context)
    
    # Assert that the exception raised contains the gRPC abort message and details
    assert "gRPC aborted" in str(excinfo.value)
    assert "Invalid or expired Spotify token" in str(excinfo.value)

def test_search_track_token_refresh(track_search_service, monkeypatch):
    # Mock the first Spotify API call to return a 401 (expired token)
    def mock_spotify_api_first_fail(*args, **kwargs):
        class MockResponse:
            status_code = 401
            def json(self):
                return {"error": "invalid_token", "error_description": "The access token expired"}
            @property
            def text(self):
                return "Invalid token"
        return MockResponse()

    # Mock the second Spotify API call (after token refresh) to succeed
    def mock_spotify_api_second_success(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "name": "Mock Song",
                    "artists": [{"name": "Mock Artist"}],
                    "tempo": 120.0,
                    "energy": 0.8,
                    "valence": 0.6,
                    "danceability": 0.7
                }
        return MockResponse()

    # Mock both API calls, failing first then succeeding
    mock_calls = [mock_spotify_api_first_fail, mock_spotify_api_second_success]
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_calls.pop(0)())

    # Mock the token refresh
    monkeypatch.setattr("music_ml.utils.spotify_utils.get_spotify_access_token", lambda: "new_test_token")

    # Create a TrackSearchRequest
    request = TrackSearchRequest(spotify_track_id="valid_id")
    context = MockContext()

    # Call the SearchTrack method and expect it to retry and succeed
    response = track_search_service.SearchTrack(request, context)

    # Assert that the response contains the expected track information
    assert response.track.track_name == "Mock Song"
    assert response.track.artist == "Mock Artist"
    assert response.track.tempo == pytest.approx(120.0)
    assert response.track.energy == pytest.approx(0.8)
    assert response.track.valence == pytest.approx(0.6)
    assert response.track.danceability == pytest.approx(0.7)