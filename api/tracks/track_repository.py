from api.tracks.track_model import Track  # Adjust the import based on your project structure
from datetime import datetime

class TrackRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        """Retrieve all tracks from the database."""
        query = "SELECT * FROM tracks"
        rows = self._connection.execute(query)
        tracks = [Track(**row) for row in rows]
        return tracks

    def find(self, track_id):
        """Retrieve a specific track by its ID."""
        query = 'SELECT * FROM tracks WHERE track_id = %s'
        rows = self._connection.execute(query, [track_id])
        if not rows:
            return None
        row = rows[0]
        track = Track(
            track_id=row['track_id'],
            name=row['name'],
            artist=row['artist'],
            album=row['album'],
            duration=row['duration'],
            spotify_url=row['spotify_url'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
        return track

    def create(self, track):
        """Insert a new track into the database."""
        query = """
            INSERT INTO tracks (track_id, name, artist, album, duration, spotify_url, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING track_id, created_at, updated_at
        """
        params = (
            track.track_id,
            track.name,
            track.artist,
            track.album,
            track.duration,
            track.spotify_url,
            track.created_at or datetime.now(),
            track.updated_at or datetime.now()
        )
        result = self._connection.execute(query, params)
        return result[0]['track_id']  # Return the newly created track's ID

    def update(self, track_id, track):
        """Update an existing track's details."""
        query = """
            UPDATE tracks
            SET name = %s,
                artist = %s,
                album = %s,
                duration = %s,
                spotify_url = %s,
                updated_at = %s
            WHERE track_id = %s
            RETURNING track_id, created_at, updated_at
        """
        params = (
            track.name,
            track.artist,
            track.album,
            track.duration,
            track.spotify_url,
            track.updated_at or datetime.now(),
            track_id
        )
        self._connection.execute(query, params)
        return None

    def delete(self, track_id):
        """Delete a track from the database."""
        query = "DELETE FROM tracks WHERE track_id = %s"
        self._connection.execute(query, [track_id])
        return None
