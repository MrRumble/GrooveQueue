import unittest
from datetime import datetime
from api.tracks.track_model import Track  # Adjust the import based on your project structure

class TestTrackModel(unittest.TestCase):

    def setUp(self):
        # This method will run before each test
        self.track = Track(
            track_id="12345",
            name="Test Song",
            artist="Test Artist",
            album="Test Album",
            duration=210,
            spotify_url="http://spotify.com/test_song"
        )

    def test_initialization(self):
        """Test that the Track object is initialized correctly."""
        self.assertEqual(self.track.track_id, "12345")
        self.assertEqual(self.track.name, "Test Song")
        self.assertEqual(self.track.artist, "Test Artist")
        self.assertEqual(self.track.album, "Test Album")
        self.assertEqual(self.track.duration, 210)
        self.assertEqual(self.track.spotify_url, "http://spotify.com/test_song")
        self.assertIsInstance(self.track.created_at, datetime)  # Check created_at is a datetime instance
        self.assertIsInstance(self.track.updated_at, datetime)  # Check updated_at is a datetime instance

    def test_equality(self):
        """Test the equality comparison between two Track objects."""
        track2 = Track(
            track_id="12345",
            name="Test Song",
            artist="Test Artist",
            album="Test Album",
            duration=210,
            spotify_url="http://spotify.com/test_song"
        )
        track3 = Track(
            track_id="54321",
            name="Different Song",
            artist="Different Artist",
            album="Different Album",
            duration=180,
            spotify_url="http://spotify.com/different_song"
        )
        
        self.assertEqual(self.track, track2)  # Should be equal
        self.assertNotEqual(self.track, track3)  # Should not be equal

    def test_repr(self):
        """Test the string representation of the Track object."""
        expected_repr = ("Track(track_id=12345, name=Test Song, "
                         "artist=Test Artist, album=Test Album, "
                         "duration=210, spotify_url=http://spotify.com/test_song, "
                         "created_at={}, updated_at={})".format(
                             self.track.created_at, self.track.updated_at))
        self.assertEqual(repr(self.track), expected_repr)

    def test_to_dict(self):
        """Test the to_dict method of the Track object."""
        expected_dict = {
            "track_id": "12345",
            "name": "Test Song",
            "artist": "Test Artist",
            "album": "Test Album",
            "duration": 210,
            "spotify_url": "http://spotify.com/test_song",
            "created_at": self.track.created_at.isoformat(),
            "updated_at": self.track.updated_at.isoformat()
        }
        self.assertEqual(self.track.to_dict(), expected_dict)


