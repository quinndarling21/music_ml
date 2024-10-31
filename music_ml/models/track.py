from dataclasses import dataclass
from music_ml.models.artist import Artist
from typing import Optional

@dataclass
class Track:
    spotify_track_id: str
    track_name: str
    artist: Artist
    genre: Optional[str] = None
    tempo: Optional[float] = 0.0
    energy: Optional[float]= 0.0
    valence: Optional[float] = 0.0
    danceability: Optional[float] = 0.0
    