import requests
from urllib.parse import quote

class MusicBrainzAPI:
    BASE_URL = "https://musicbrainz.org/ws/2"

    def search_tracks(self, track_name, artist_name=None):
        url = f"{self.BASE_URL}/recording/"
        
        # Construct the query properly
        query = f"{quote(track_name)}"
        if artist_name:
            query += f" AND artist:{quote(artist_name)}"
        
        params = {
            "query": query,
            "fmt": "json",
            "limit": 10
        }

        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for any bad response
        data = response.json()

        tracks = []
        for recording in data.get('recordings', []):
            # Optionally check if the recording is not live
            if 'live' not in recording.get('disambiguation', '').lower():
                track_info = {
                    'id': recording['id'],
                    'name': recording['title'],
                    'artist': recording['artist-credit'][0]['name'],
                    'album': recording.get('releases', [{}])[0].get('title'),
                    'duration': recording.get('length')
                }
                tracks.append(track_info)

        return tracks
