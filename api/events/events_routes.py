from flask import Blueprint, request, jsonify, current_app
from api.events.event_model import Event
from api.events.event_repository import EventRepository
from api.bands.band_repository import BandRepository
from api.events.event_create import create_event as create_new_event
from api.common.db import get_flask_database_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

# Blueprint setup
event_bp = Blueprint('event_bp', __name__)

# Route to get all events
@event_bp.route('/events', methods=['GET'])
def get_all_events():
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)
    all_events = event_repo.find_all()

    # Convert list of Event objects to list of dictionaries
    events_dict = [event.to_dict() for event in all_events]

    return jsonify(events_dict), 200

@event_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)
    event = event_repo.find(event_id)
    
    if event is None:
        return jsonify(error="Event not found"), 404
    
    band_repo = BandRepository(connection)
    band_details = band_repo.find(event.band_id)

    response_data = {
        **event.to_dict(),  
        'band_name': band_details.band_name  
    }

    return jsonify(response_data), 200

# Route to create a new event
@event_bp.route('/events', methods=['POST'])
def create_event():
    data = request.json

    # Validate the input data
    if not data or not all(key in data for key in ['event_name', 'location', 'event_start', 'event_end']):
        return jsonify(error="Missing required fields"), 400

    event = Event(
        event_name=data.get('event_name'),
        location=data.get('location'),
        event_start=data.get('event_start'),
        event_end=data.get('event_end'),
        qr_code_content=data.get('qr_code_content'),
        band_id=data.get('band_id'),
        created_at=data.get('created_at'),
        updated_at=data.get('updated_at')
    )

    try:
        created_event_id = create_new_event(event)
        return jsonify(event_id=created_event_id), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

# Route to update an existing event
@event_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json

    # Validate the input data
    if not data or not all(key in data for key in ['event_name', 'location', 'event_start', 'event_end']):
        return jsonify(error="Missing required fields"), 400

    event = Event(
        event_name=data.get('event_name'),
        location=data.get('location'),
        event_start=data.get('event_start'),
        event_end=data.get('event_end'),
        qr_code_content=data.get('qr_code_content'),
        band_id=data.get('band_id'),
        created_at=data.get('created_at'),
        updated_at=data.get('updated_at')
    )

    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)

    try:
        event_repo.update(event_id, event)
        return jsonify(message="Event updated successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

# Route to delete an event by ID
@event_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)

    try:
        event_repo.delete(event_id)
        return jsonify(message="Event deleted successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

# Route to get events by band ID
@event_bp.route('/bands/<int:band_id>/events', methods=['GET'])
def get_events_by_band(band_id):
    print("I AM CALLED!")
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)
    events = event_repo.find_events_by_band_id(band_id)
    print(band_id)

    if not events:
        return jsonify(error="No events found for this band"), 404

    events_dict = [event.to_dict() for event in events]
    return jsonify(events_dict), 200

@event_bp.route('/bands/current/events', methods=['GET'])
@jwt_required()
def get_current_band_events():
    current_band_id = get_jwt_identity()
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)
    events = event_repo.find_events_by_band_id(current_band_id)

    if not events:
        return jsonify(error="No events found for this band"), 404

    return jsonify([event.to_dict() for event in events]), 200