from dataclasses import dataclass

@dataclass
class Track:
    spotify_track_id: str
    track_name: str
    artist: str
    genre: str
    tempo: float
    energy: float
    valence: float
    danceability: float