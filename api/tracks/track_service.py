from datetime import datetime
from api.tracks.music_brainz_api import MusicBrainzAPI 
from api.tracks.track_model import Track 

class TrackService:
    def __init__(self, track_repository, musicbrainz_api):
        self.track_repository = track_repository
        self.musicbrainz_api = musicbrainz_api

    def search_track(self, track_name, artist_name=None):
        # Step 1: Search for track in the local database
        local_tracks = self.track_repository.search_by_name(track_name, artist_name)
        
        # Step 2: If found, return cached results
        if local_tracks:
            return local_tracks

        # Step 3: Otherwise, query MusicBrainz API
        musicbrainz_tracks = self.musicbrainz_api.search_tracks(track_name, artist_name)

        # Step 4: Store the MusicBrainz results in the local database
        cached_tracks = []
        for mb_track in musicbrainz_tracks:
            track = Track(
                name=mb_track['name'],
                artist=mb_track['artist'],
                album=mb_track.get('album'),
                duration=mb_track.get('duration'),
                musicbrainz_id=mb_track['id'],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            track_id = self.track_repository.create(track)
            track.track_id = track_id
            cached_tracks.append(track)
        
        # Return combined local and MusicBrainz results
        return cached_tracks
