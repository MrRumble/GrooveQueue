from flask import Blueprint, request, jsonify, current_app
from api.tracks.track_repository import TrackRepository  # Adjust the import path as needed
from api.tracks.track_service import TrackService  # Adjust the import path as needed
from api.tracks.music_brainz_api import MusicBrainzAPI  # Adjust the import path as needed
from api.common.db import get_flask_database_connection

tracks_bp = Blueprint('tracks_bp', __name__)

@tracks_bp.route('/tracks/search', methods=['GET'])
def search_tracks():
    connection = get_flask_database_connection(current_app)
    track_repo = TrackRepository(connection)
    musicbrainz_api = MusicBrainzAPI()  # Assuming this is your MusicBrainz API integration
    track_service = TrackService(track_repo, musicbrainz_api)

    track_name = request.args.get('track_name')
    artist_name = request.args.get('artist_name')  # Get artist name from query parameters
    
    if not track_name:
        return jsonify(error="Track name is required"), 400

    # Search tracks using TrackService
    tracks = track_service.search_track(track_name, artist_name)  # Pass artist_name as well

    if not tracks:
        return jsonify(error="No tracks found"), 404

    # Format the results
    tracks_list = [track.to_dict() for track in tracks]  # Assuming Track has a `to_dict` method
    return jsonify(tracks_list), 200
