from music_ml.matchers.matcher import Matcher
from typing import List
from music_ml.models.track import Track
from music_ml.services.spotify_service import get_artist_top_tracks

class ArtistMatcher(Matcher):
    def match(self, input_track: Track, n: int) -> List[Track]:
        spotify_artist_id = input_track.artist.spotify_artist_id
        top_tracks = get_artist_top_tracks(spotify_artist_id)
        matching_tracks = [track for track in top_tracks if track.spotify_track_id != input_track.spotify_track_id]
        return matching_tracks[:n]