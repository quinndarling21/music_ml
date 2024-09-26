import pytest
import grpc
from music_ml.protobuf.services.search.search_pb2 import (
    SearchServiceRequest, 
    SearchServiceResponse
)
from music_ml.services.search.search_server import (
    SearchService
)
from music_ml.protobuf.common.track_pb2 import Track

# Mock Spotify Search API success response
def mock_spotify_search_api_success(*args, **kwargs):
    class MockResponse:
        status_code = 200
        def json(self):
            return {
                "tracks": {
                    "items": [
                        {
                            "id": "mock_track_id_1",
                            "name": "Mock Song 1",
                            "artists": [{"name": "Mock Artist 1"}]
                        },
                        {
                            "id": "mock_track_id_2",
                            "name": "Mock Song 2",
                            "artists": [{"name": "Mock Artist 2"}]
                        }
                    ],
                    "total": 2
                }
            }
    return MockResponse()

# Mock Spotify Search API error response
def mock_spotify_search_api_error(*args, **kwargs):
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
def search_service():
    return SearchService()

@pytest.fixture(autouse=True)
def mock_spotify_token(monkeypatch):
    """
    This fixture automatically mocks the get_spotify_access_token function
    for all tests, returning a static token value.
    """
    monkeypatch.setattr("music_ml.utils.spotify_utils.get_spotify_access_token", lambda: "test_token")

def test_search_tracks_success(search_service, monkeypatch):
    # Mock the Spotify API call to return a success response
    monkeypatch.setattr("requests.get", mock_spotify_search_api_success)

    # Create a SearchServiceRequest
    request = SearchServiceRequest(query="mock query", limit=2)
    context = MockContext()

    # Call the SearchTracks method
    response = search_service.SearchTracks(request, context)

    # Assert that the response contains the expected track information
    assert len(response.tracks) == 2
    assert response.tracks[0].track_name == "Mock Song 1"
    assert response.tracks[0].artist == "Mock Artist 1"
    assert response.tracks[1].track_name == "Mock Song 2"
    assert response.tracks[1].artist == "Mock Artist 2"
    assert response.total_results == 2

def test_search_tracks_error(search_service, monkeypatch):
    # Mock the Spotify API call to return an error response
    monkeypatch.setattr("requests.get", mock_spotify_search_api_error)

    # Create a SearchServiceRequest
    request = SearchServiceRequest(query="invalid query")
    context = MockContext()

    # Call the SearchTracks method and expect a gRPC exception due to API failure
    with pytest.raises(Exception) as excinfo:
        search_service.SearchTracks(request, context)
    
    # Assert that the exception raised contains the gRPC abort message and details
    assert "gRPC aborted" in str(excinfo.value)

def test_search_tracks_token_refresh(search_service, monkeypatch):
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
                    "tracks": {
                        "items": [
                            {
                                "id": "mock_track_id_1",
                                "name": "Mock Song 1",
                                "artists": [{"name": "Mock Artist 1"}]
                            }
                        ],
                        "total": 1
                    }
                }
        return MockResponse()

    # Mock both API calls, failing first then succeeding
    mock_calls = [mock_spotify_api_first_fail, mock_spotify_api_second_success]
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_calls.pop(0)())

    # Mock the token refresh
    monkeypatch.setattr("music_ml.utils.spotify_utils.get_spotify_access_token", lambda: "new_test_token")

    # Create a SearchServiceRequest
    request = SearchServiceRequest(query="mock query", limit=1)
    context = MockContext()

    # Call the SearchTracks method and expect it to retry and succeed
    response = search_service.SearchTracks(request, context)

    # Assert that the response contains the expected track information
    assert len(response.tracks) == 1
    assert response.tracks[0].track_name == "Mock Song 1"
    assert response.tracks[0].artist == "Mock Artist 1"
    assert response.total_results == 1