from dataclasses import dataclass
from music_ml.models.track import Track
from typing import List

@dataclass
class Playlist:
    tracks: List[Track]