from flask import Blueprint, request, jsonify, current_app
from api.requests.request_model import Request
from api.requests.request_repository import RequestRepository
from api.attendances.attendance_repository import AttendanceRepository
from api.notifications.notification_repository import NotificationRepository
from api.notifications.notification_model import Notification
from api.guests.guest_repository import GuestRepository
from api.common.db import get_flask_database_connection
from datetime import datetime
from api.events.event_repository import EventRepository
from flask_jwt_extended import jwt_required, get_jwt_identity

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
@jwt_required()
def create_request(event_id):
    connection = get_flask_database_connection(current_app)
    request_repo = RequestRepository(connection)
    event_repo = EventRepository(connection)
    attendance_repo = AttendanceRepository(connection)
    guest_id = get_jwt_identity()
    data = request.get_json()

    # Check if the event exists
    event = event_repo.find(event_id)
    if not event:
        return jsonify(error="Invalid event ID: event not found"), 400
    
    # Check if the guest is attending the event
    if not attendance_repo.is_attending_event(guest_id=guest_id, event_id=event_id):
        return jsonify(error="You must be attending the event to make a request."), 403

    max_requests = event.max_requests_per_user

    # Check if guest has reached the max requests limit for the event
    guests_requests_count = request_repo.requests_by_guest(guest_id=guest_id, event_id=event_id)
    if guests_requests_count >= max_requests:
        return jsonify(error="You have reached the maximum number of requests for this event."), 400

    # Validate input fields
    if not data or not all(key in data for key in ['song_name', 'artist']):
        return jsonify(error="Missing required fields"), 400
    
    # Create the new request
    new_request = Request(
        song_name=data['song_name'],  # Changed from track_id to song_name
        artist=data['artist'],         # Added artist
        guest_id=guest_id,
        event_id=event_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    new_request_id = request_repo.create(new_request)

    # Send Notification to band
    guest_repo = GuestRepository(connection)
    guest = guest_repo.find(guest_id)
    notification_repo = NotificationRepository(connection)
    notification = Notification(
        recipient_id=event.band_id,
        recipient_type='band',
        event_id=event_id,
        notification_type='song_request',
        message=f'{guest.name} has requested the song "{new_request.song_name}" by {new_request.artist} for your show: {event.event_name}'
    )

    notification_repo.create(notification)

    return jsonify({"request_id": new_request_id}), 201

@request_bp.route('/events/<int:event_id>/requests', methods=['GET'])
def get_requests_by_event_id(event_id):
    connection = get_flask_database_connection(current_app)
    request_repo = RequestRepository(connection)
    
    requests = request_repo.find_requests_by_event_id(event_id)
    
    if not requests:
        return jsonify(error="No requests found for this event"), 404

    requests_list = [req.to_dict() for req in requests]
    
    return jsonify(requests_list), 200
