import requests
import logging

from flask import Blueprint, request, jsonify
from music_ml.models.track import Track
from music_ml.models.playlist import Playlist
from music_ml.matchers.artist_matcher import ArtistMatcher
from music_ml.services.spotify_service import get_track_by_id

# Blueprint for playlist API routes
playlist_bp = Blueprint('playlist', __name__)

@playlist_bp.route('/generate_playlist', methods=['GET'])
def generate_playlist():
    spotify_track_id = request.args.get('spotify_track_id')

    if not spotify_track_id:
        return jsonify({'error': 'spotify_track_id is required'}), 400

    try:
        # Use the new service to get the Track object
        input_track = get_track_by_id(spotify_track_id)

        # Instantiate ArtistMatcher
        artist_matcher = ArtistMatcher()

        # Get matching tracks
        matching_tracks = artist_matcher.match(input_track, n=9)

        # Create playlist including the original track
        playlist_tracks = [input_track] + matching_tracks

        # Create a Playlist object
        playlist = Playlist(tracks=playlist_tracks)

        return jsonify({'playlist': playlist})

    except requests.exceptions.RequestException as e:
        logging.exception("RequestException occurred.")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return jsonify({'error': str(e)}), 500