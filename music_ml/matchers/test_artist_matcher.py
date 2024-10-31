import pytest
from unittest.mock import patch, MagicMock
from music_ml.models.track import Track, Artist
from music_ml.matchers.artist_matcher import ArtistMatcher

# Test when get_artist_top_tracks returns multiple tracks including the input track
@patch('music_ml.matchers.artist_matcher.get_artist_top_tracks')
def test_artist_matcher_excludes_input_track(mock_get_top_tracks):
    # Mock tracks returned by get_artist_top_tracks
    mock_track_1 = MagicMock(spec=Track)
    mock_track_1.spotify_track_id = 'track1'  # Same as input track

    mock_track_2 = MagicMock(spec=Track)
    mock_track_2.spotify_track_id = 'track2'

    mock_track_3 = MagicMock(spec=Track)
    mock_track_3.spotify_track_id = 'track3'

    mock_get_top_tracks.return_value = [mock_track_1, mock_track_2, mock_track_3]

    # Input track
    input_artist = Artist(name='Test Artist', spotify_artist_id='artist123')
    input_track = Track(track_name='Input Track', spotify_track_id='track1', artist=input_artist)

    # Instantiate matcher and call match
    matcher = ArtistMatcher()
    result = matcher.match(input_track, n=2)

    # Assertions
    assert len(result) == 2
    assert mock_track_1 not in result  # Input track should be excluded
    assert mock_track_2 in result
    assert mock_track_3 in result

# Test when get_artist_top_tracks returns only the input track
@patch('music_ml.matchers.artist_matcher.get_artist_top_tracks')
def test_artist_matcher_returns_empty_list_when_no_other_tracks(mock_get_top_tracks):
    # Mock tracks returned by get_artist_top_tracks
    mock_track_1 = MagicMock(spec=Track)
    mock_track_1.spotify_track_id = 'track1'  # Same as input track

    mock_get_top_tracks.return_value = [mock_track_1]

    # Input track
    input_artist = Artist(name='Test Artist', spotify_artist_id='artist123')
    input_track = Track(track_name='Input Track', spotify_track_id='track1', artist=input_artist)

    # Instantiate matcher and call match
    matcher = ArtistMatcher()
    result = matcher.match(input_track, n=5)

    # Assertions
    assert len(result) == 0  # No other tracks available

# Test when get_artist_top_tracks returns fewer tracks than requested
@patch('music_ml.matchers.artist_matcher.get_artist_top_tracks')
def test_artist_matcher_returns_all_available_tracks_when_less_than_n(mock_get_top_tracks):
    # Mock tracks returned by get_artist_top_tracks
    mock_track_2 = MagicMock(spec=Track)
    mock_track_2.spotify_track_id = 'track2'

    mock_track_3 = MagicMock(spec=Track)
    mock_track_3.spotify_track_id = 'track3'

    mock_get_top_tracks.return_value = [mock_track_2, mock_track_3]

    # Input track
    input_artist = Artist(name='Test Artist', spotify_artist_id='artist123')
    input_track = Track(track_name='Input Track', spotify_track_id='track1', artist=input_artist)

    # Instantiate matcher and call match
    matcher = ArtistMatcher()
    result = matcher.match(input_track, n=5)

    # Assertions
    assert len(result) == 2
    assert mock_track_2 in result
    assert mock_track_3 in result

# Test when get_artist_top_tracks raises an exception
@patch('music_ml.matchers.artist_matcher.get_artist_top_tracks')
def test_artist_matcher_handles_exception(mock_get_top_tracks):
    # Set the mock to raise an exception
    mock_get_top_tracks.side_effect = Exception('API Error')

    # Input track
    input_artist = Artist(name='Test Artist', spotify_artist_id='artist123')
    input_track = Track(track_name='Input Track', spotify_track_id='track1', artist=input_artist)

    # Instantiate matcher and attempt to call match
    matcher = ArtistMatcher()

    with pytest.raises(Exception) as exc_info:
        matcher.match(input_track, n=5)

    # Assertions
    assert 'API Error' in str(exc_info.value)