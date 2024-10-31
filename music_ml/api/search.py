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
        tracks = search_spotify_tracks(query, limit)

        return jsonify({'tracks': tracks, 'total_results': len(tracks)})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500