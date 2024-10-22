from flask import Blueprint, request, jsonify, current_app
from api.events.event_model import Event
from api.events.event_repository import EventRepository
from api.bands.band_repository import BandRepository
from api.events.validate_event import validate_event
from api.common.db import get_flask_database_connection
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

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
@jwt_required()
def create_event():
    data = request.json

    # Validate the input data
    if not data or not all(key in data for key in ['event_name', 'location', 'event_start', 'event_end']):
        return jsonify(error="Missing required fields"), 400

    # Attempt to parse event start and end times
    try:
        event_start = datetime.fromisoformat(data['event_start'])
        event_end = datetime.fromisoformat(data['event_end'])
    except ValueError:
        return jsonify(error="Invalid date format. Use ISO 8601 format."), 400

    # Create the Event instance
    event = Event(
        event_name=data.get('event_name'),
        location=data.get('location'),
        event_start=event_start,  # Use the parsed datetime object
        event_end=event_end,      # Use the parsed datetime object
        qr_code_content=data.get('qr_code_content'),
        band_id=get_jwt_identity(),
        max_requests_per_user=data.get('max_requests_per_user', 1),  # Default value if not provided
        created_at=datetime.now(),  # Set created_at to now
        updated_at=datetime.now()     # Set updated_at to now
    )

    # Validate the event using the boolean function
    is_valid, error_message = validate_event(event)
    if not is_valid:
        return jsonify(error=error_message), 400

    # If the event is valid, create it
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)
    
    try:
        created_event_id = event_repo.create(event)
        return jsonify(event_id=created_event_id), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

# Route to update an existing event
@event_bp.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    data = request.json

    # Validate the input data
    if not data or not all(key in data for key in ['event_name', 'location', 'event_start', 'event_end']):
        return jsonify(error="Missing required fields"), 400

        # Attempt to parse event start and end times
    try:
        event_start = datetime.fromisoformat(data['event_start'])
        event_end = datetime.fromisoformat(data['event_end'])
    except ValueError:
        return jsonify(error="Invalid date format. Use ISO 8601 format."), 400
    
    current_band_id = get_jwt_identity()  # Get the current band's ID from the JWT token
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)

    # Check if the event exists and belongs to the current band
    event = event_repo.find(event_id)
    if event is None:
        return jsonify(error="Event not found"), 404
    
    if event.band_id != current_band_id:
        return jsonify(error="You are not authorized to update this event"), 403

    # Create the updated Event instance
    updated_event = Event(
        event_name=data.get('event_name'),
        location=data.get('location'),
        event_start=event_start,
        event_end=event_end,
        qr_code_content=data.get('qr_code_content'),
        band_id=current_band_id,  # Ensure this is set to the current band ID
        max_requests_per_user=data.get('max_requests_per_user', event.max_requests_per_user),  # Default to existing value if not provided
        created_at=event.created_at,  # Keep existing created_at
        updated_at=datetime.now()  # Update the updated_at timestamp
    )

    # Validate the updated event
    is_valid, error_message = validate_event(updated_event)
    if not is_valid:
        return jsonify(error=error_message), 400

    # Try to update the event in the database
    try:
        event_repo.update(event_id, updated_event)
        return jsonify(message="Event updated successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

@event_bp.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)

    # Get the current band ID from the JWT token
    current_band_id = get_jwt_identity()  

    # Check if the event exists
    event = event_repo.find(event_id)
    if event is None:
        return jsonify(error="Event not found"), 404
    
    # Check if the event belongs to the current band
    if event.band_id != current_band_id:
        return jsonify(error="You are not authorized to delete this event"), 403

    try:
        event_repo.delete(event_id)
        return jsonify(message="Event deleted successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 400


@event_bp.route('/bands/<int:band_id>/events', methods=['GET'])
def get_events_by_band(band_id):
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)
    band_repo = BandRepository(connection)

    try:
        band = band_repo.find(band_id)
    except ValueError:
        return jsonify(error="Band not found"), 404  

    events = event_repo.find_events_by_band_id(band_id)

    if not events:
        return jsonify(error="No events found for this band"), 404
    
    response_data = {
        'band_name': band.band_name,
        'events': [event.to_dict() for event in events]
    }
    return jsonify(response_data), 200


@event_bp.route('/bands/current/events', methods=['GET'])
@jwt_required()
def get_current_band_events():
    current_band_id = get_jwt_identity()
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)
    band_repo = BandRepository(connection)
    band = band_repo.find(current_band_id)
    if not band:
        return jsonify(error="Band not found"), 404
    
    events = event_repo.find_events_by_band_id(current_band_id)
    if not events:
        return jsonify(error="No events found for this band"), 404
    
    response_data = {
        "band_name": band.band_name,  # Include the band's name
        "events": [event.to_dict() for event in events]  # Include the list of events
    }

    return jsonify(response_data), 200