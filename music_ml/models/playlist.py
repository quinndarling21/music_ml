from dataclasses import dataclass
from music_ml.models.track import Track
from typing import List

@dataclass
class playlist:
    tracks: List[Track]