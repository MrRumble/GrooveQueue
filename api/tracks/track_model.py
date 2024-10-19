from datetime import datetime

class Track:
    def __init__(self, track_id=None, name=None, artist=None,
                 album=None, duration=None, musicbrainz_id=None,
                 created_at=None, updated_at=None):
        self.track_id = track_id  # Unique track_id
        self.name = name          # Track name
        self.artist = artist      # Artist name
        self.album = album        # Album name
        self.duration = duration  # Track duration in seconds
        self.musicbrainz_id = musicbrainz_id  # Unique MusicBrainz ID
        self.created_at = created_at or datetime.now()  # Timestamp when track was added
        self.updated_at = updated_at or datetime.now()  # Timestamp when track was last updated

    def to_dict(self):
        return {
            "track_id": self.track_id,
            "name": self.name,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration,
            "musicbrainz_id": self.musicbrainz_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def __repr__(self):
        return (f"Track(track_id={self.track_id}, name={self.name}, "
                f"artist={self.artist}, album={self.album}, "
                f"duration={self.duration}, musicbrainz_id={self.musicbrainz_id}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})")
    
    def __eq__(self, other):
        if not isinstance(other, Track):
            return NotImplemented
        # Compare all relevant fields except timestamps
        return (self.track_id == other.track_id and
                self.name == other.name and
                self.artist == other.artist and
                self.album == other.album and
                self.duration == other.duration and
                self.musicbrainz_id == other.musicbrainz_id)
