from flask import Blueprint, request, jsonify, current_app
from api.requests.request_model import Request
from api.requests.request_repository import RequestRepository
from api.common.db import get_flask_database_connection
from datetime import datetime
from api.events.event_repository import EventRepository

request_bp = Blueprint('request_bp', __name__)

@request_bp.route('/requests/<int:request_id>', methods=['GET'])
def get_request_by_id(request_id: int):
    connection = get_flask_database_connection(current_app)
    request_repo = RequestRepository(connection)
    
    request_item = request_repo.find(request_id)
    
    if request_item is None:
        return jsonify(error="Request not found"), 404

    return jsonify(request_item.to_dict()), 200  

@request_bp.route('/events/<int:event_id>/requests', methods=['POST'])
def create_request(event_id):
    connection = get_flask_database_connection(current_app)
    request_repo = RequestRepository(connection)
    event_repo = EventRepository(connection)

    data = request.get_json()

    # Check if the event exists
    event = event_repo.find(event_id)
    if not event:
        return jsonify(error="Invalid event ID: event not found"), 400

    max_requests = event.max_requests_per_user

    # Check if guest has reached the max requests limit for the event
    guests_requests_count = request_repo.requests_by_guest(data['guest_id'], event_id)
    if guests_requests_count >= max_requests:
        return jsonify(error="You have reached the maximum number of requests for this event."), 400

    # Validate input fields
    if not data or not all(key in data for key in ['song_name', 'guest_id']):
        return jsonify(error="Missing required fields"), 400
    
    if data['song_name'].strip() == "":
        return jsonify(error="Song name cannot be empty"), 400

    # Create the new request
    new_request = Request(
        song_name=data['song_name'],
        guest_id=data['guest_id'],
        event_id=event_id,  # Now we use the event_id from the URL
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    new_request_id = request_repo.create(new_request)
    return jsonify({"request_id": new_request_id}), 201


@request_bp.route('/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    connection = get_flask_database_connection(current_app)
    request_repo = RequestRepository(connection)
    
    data = request.get_json()
    
    # Ensure at least one field is provided
    if not data or not any(key in data for key in ['song_name', 'guest_id', 'event_id']):
        return jsonify(error="At least one field (song_name, guest_id, event_id) is required"), 400
    
    existing_request = request_repo.find(request_id)
    if not existing_request:
        return jsonify(error="Request not found"), 404

    if 'song_name' in data:
        if data['song_name'].strip() == "":
            return jsonify(error="Song name cannot be empty"), 400
        existing_request.song_name = data['song_name']
    if 'guest_id' in data:
        existing_request.guest_id = data['guest_id']
    if 'event_id' in data:
        existing_request.event_id = data['event_id']
    
    existing_request.updated_at = datetime.now()  # Update timestamp
    
    request_repo.update(request_id, existing_request)
    
    return jsonify({"message": "Request updated successfully"}), 200

@request_bp.route('/events/<int:event_id>/requests', methods=['GET'])
def get_requests_by_event_id(event_id):
    connection = get_flask_database_connection(current_app)
    request_repo = RequestRepository(connection)
    
    requests = request_repo.find_requests_by_event_id(event_id)
    
    if not requests:
        return jsonify(error="No requests found for this event"), 404

    requests_list = [req.to_dict() for req in requests]
    
    return jsonify(requests_list), 200

