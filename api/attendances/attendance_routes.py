from flask import Blueprint, request, jsonify, current_app
from api.attendances.attendance_repository import AttendanceRepository
from api.attendances.attendance_model import Attendance
from api.events.event_repository import EventRepository
from api.events.event_create import create_event as create_new_event
from api.common.db import get_flask_database_connection
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Blueprint setup
attendance_bp = Blueprint('attendance_bp', __name__)

"""
Change create_attendance to take Attendence object as parameter.
"""
@attendance_bp.route('/attendance', methods=['POST'])
@jwt_required()
def post_attendance():
    data = request.json

    # Validate the input data
    if not data or not all(key in data for key in ['guest_id', 'event_id', 'status']):
        return jsonify(error="Missing required fields"), 400

    guest_id = data.get('guest_id')
    event_id = data.get('event_id')
    status = data.get('status')

    try:
        connection = get_flask_database_connection(current_app)
        attendance_repo = AttendanceRepository(connection)
        # Check if attendance already exists
        if attendance_repo.check_attendance_exists(guest_id, event_id):
            return jsonify(error="Attendance request already exists for this event"), 409
        
        created_attendance = attendance_repo.create_attendance(guest_id=guest_id, event_id=event_id, status=status)
        return jsonify(attendance=created_attendance.to_dict()), 201
    except Exception as e:
        return jsonify(error=str(e)), 400
    
@attendance_bp.route('/events/<int:event_id>/attendees', methods=['GET'])
@jwt_required()
def get_attendees_for_event(event_id):
    current_band_id = get_jwt_identity()  # Assuming this is the band ID stored in the JWT token
    
    try:
        connection = get_flask_database_connection(current_app)
        attendance_repo = AttendanceRepository(connection)
        event_repo = EventRepository(connection)

        # Check if the event exists
        event = event_repo.find(event_id)
        if not event:
            return jsonify(error="Event not found"), 404
        
        # Check if the current band is associated with the event
        if event.band_id != current_band_id:
            return jsonify(error="Unauthorized to access this event's attendees"), 403

        # Fetch all attendances for the event
        attendees = attendance_repo.get_attendance_with_guest_details(event_id)
        return jsonify(attendees=attendees), 200

    except Exception as e:
        return jsonify(error=str(e)), 400

# TODO Create a view all attendence for an event by guest, update guests attendece per event
        # only allow guests who have been approved to an event to send requests.
