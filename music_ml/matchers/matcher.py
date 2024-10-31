from abc import ABC, abstractmethod
from typing import List
from music_ml.models.track import Track

class Matcher(ABC):
    @abstractmethod
    def match(self, input_track: Track, n: int) -> List[Track]:
        """
        Abstract method to find n matching tracks based on the input_track_id.
        """
        pass