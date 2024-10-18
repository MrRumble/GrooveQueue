from datetime import datetime

class Track:
    def __init__(self, track_id=None, name=None, artist=None,
                 album=None, duration=None, spotify_url=None,
                 created_at=None, updated_at=None):
        self.track_id = track_id  # Unique Spotify track ID
        self.name = name          # Track name
        self.artist = artist      # Artist name
        self.album = album        # Album name
        self.duration = duration  # Track duration in seconds
        self.spotify_url = spotify_url  # Link to the Spotify track
        self.created_at = created_at or datetime.now()  # Timestamp when track was added
        self.updated_at = updated_at or datetime.now()  # Timestamp when track was last updated

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return (self.track_id == other.track_id and
                self.name == other.name and
                self.artist == other.artist and
                self.album == other.album and
                self.duration == other.duration)

    def __repr__(self):
        return (f"Track(track_id={self.track_id}, name={self.name}, "
                f"artist={self.artist}, album={self.album}, "
                f"duration={self.duration}, spotify_url={self.spotify_url}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})")

    def to_dict(self):
        return {
            "track_id": self.track_id,
            "name": self.name,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration,
            "spotify_url": self.spotify_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
