import grpc
from concurrent import futures
import music_ml.protobuf.services.search.search_pb2 as search_pb2
from music_ml.protobuf.services.search.search_pb2_grpc import (
    SearchServiceServicer,
    add_SearchServiceServicer_to_server
)
from music_ml.protobuf.common.track_pb2 import Track
import requests
from music_ml.utils.spotify_utils import get_spotify_access_token
from grpc_reflection.v1alpha import reflection

_SEARCH_TRACKS_DEFAULT_REQUEST_LIMIT = 20

class SearchService(SearchServiceServicer):
    def __init__(self):
        # Fetch an access token to authenticate with Spotify
        self.access_token = get_spotify_access_token()

    def SearchTracks(self, request: search_pb2.SearchServiceRequest, context):
        query = request.query
        limit = request.limit if request.limit else _SEARCH_TRACKS_DEFAULT_REQUEST_LIMIT

        # Fetch search results from the Spotify API
        search_results = self._search_spotify_tracks(query, limit, context)

        # Create a list of Track objects based on the search results
        tracks = [
            Track(
                spotify_track_id=item['id'],
                track_name=item['name'],
                artist=item['artists'][0]['name'],  # Get the first artist's name
            )
            for item in search_results['tracks']['items']
        ]

        # Create and return a SearchServiceResponse
        return search_pb2.SearchServiceResponse(
            tracks=tracks,
            total_results=search_results['tracks']['total']
        )

    def _search_spotify_tracks(self, query, limit, context):
        # Define the Spotify Search API URL
        url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit={limit}"

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)

        # Check for authorization errors (token expired, etc.)
        if response.status_code == 401:
            print("Access token expired, fetching new token...")
            self.access_token = get_spotify_access_token()
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(url, headers=headers)  # Retry with new token

        # Handle response
        if response.status_code == 200:
            return response.json()

        # For other non-successful status codes, raise a gRPC error
        context.abort(grpc.StatusCode.INTERNAL, f"Spotify API error: {response.status_code} - {response.text}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SearchServiceServicer_to_server(SearchService(), server)

    # Enable reflection
    SERVICE_NAMES = (
        search_pb2.DESCRIPTOR.services_by_name['SearchService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50052')  # Listen on a different port, e.g., 50052
    server.start()
    print("Search gRPC server is running on port 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()