import grpc
from concurrent import futures
import music_ml.protobuf.services.track_search.track_search_pb2 as track_search_pb2
from music_ml.protobuf.services.track_search.track_search_pb2_grpc import (
    TrackSearchServiceServicer,
    add_TrackSearchServiceServicer_to_server
)
from music_ml.protobuf.common.track_pb2 import Track
import requests
from music_ml.utils.spotify_utils import get_spotify_access_token
from grpc_reflection.v1alpha import reflection

MAX_AUTHENTICATION_ERROR_ATTEMPTS = 2

class TrackSearchService(TrackSearchServiceServicer):
    def __init__(self):
        # Fetch an access token to authenticate with Spotify
        self.access_token = get_spotify_access_token()

    def SearchTrack(self, request: track_search_pb2.TrackSearchRequest, context):
        track_id = request.spotify_track_id
        print(f"Received request for Spotify track ID: {track_id}")

        # Fetch track details from the Spotify API
        track_info = self._get_spotify_track_info(track_id, context)

        # Create and return a TrackSearchResponse
        track = Track(
            track_name=track_info['name'],
            artist=track_info['artists'][0]['name'],
            tempo=track_info.get('tempo', 0),  # Default to 0 if not available
            energy=track_info.get('energy', 0),
            valence=track_info.get('valence', 0),
            danceability=track_info.get('danceability', 0)
        )
        return track_search_pb2.TrackSearchResponse(track=track)

    def _get_spotify_track_info(self, track_id, context):
        # Define the Spotify API URL
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        
        attempts = 0

        while attempts < MAX_AUTHENTICATION_ERROR_ATTEMPTS:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(url, headers=headers)

            # If the token has expired (401), try refreshing the token and retry
            if response.status_code == 401:
                if attempts == 0:
                    print("Access token expired, fetching new token...")
                    self.access_token = get_spotify_access_token()
                    attempts += 1
                    continue  # Retry the request with the new token
                else:
                    print("Failed after refreshing the token.")
                    context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid or expired Spotify token")

            # If the request is successful (200), return the JSON response
            if response.status_code == 200:
                return response.json()

            # For other non-successful status codes, raise a gRPC error
            context.abort(grpc.StatusCode.INTERNAL, f"Spotify API error: {response.status_code} - {response.text}")

        # If we exit the loop without success, something went wrong
        context.abort(grpc.StatusCode.INTERNAL, "Failed to fetch track info after retries")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TrackSearchServiceServicer_to_server(TrackSearchService(), server)

    # Enable reflection
    SERVICE_NAMES = (
        track_search_pb2.DESCRIPTOR.services_by_name['TrackSearchService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')  # Listen on port 50051
    server.start()
    print("TrackSearch gRPC server is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()