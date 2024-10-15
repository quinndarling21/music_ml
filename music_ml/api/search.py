import requests

from flask import Blueprint, request, jsonify
from music_ml.services.spotify_service import search_spotify_tracks
from music_ml.models.track import Track

# Blueprint for search API routes
search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search_tracks():
    query = request.args.get('query')
    limit = request.args.get('limit', 20)

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    # Use the Spotify search service to get track data
    try:
        search_results = search_spotify_tracks(query, limit)

        # Convert the results into Track objects
        tracks = [
            Track(
                spotify_track_id=item['id'],
                track_name=item['name'],
                artist=item['artists'][0]['name'],
                genre="",  # Spotify API doesn't return genre directly, so you may add a placeholder
                tempo=0.0,  # Placeholder, update if this info is available
                energy=0.0,
                valence=0.0,
                danceability=0.0
            )
            for item in search_results['tracks']['items']
        ]

        # Convert Track objects to dicts for JSON response
        tracks_dict = [track.__dict__ for track in tracks]

        return jsonify({'tracks': tracks_dict, 'total_results': search_results['tracks']['total']})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500