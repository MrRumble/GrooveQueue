from flask import Blueprint, request, jsonify, current_app
from api.attendances.attendance_repository import AttendanceRepository
from api.notifications.notification_model import Notification
from api.events.event_repository import EventRepository
from api.guests.guest_repository import GuestRepository
from api.notifications.notification_repository import NotificationRepository
from api.common.db import get_flask_database_connection
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from api.auth.token_fixture import token_required

# Blueprint setup
attendance_bp = Blueprint('attendance_bp', __name__)

@attendance_bp.route('/attendance', methods=['POST'])
@jwt_required()
@token_required
def post_attendance():
    data = request.json
    # Validate the input data
    if not data or not all(key in data for key in ['event_id', 'status']):
        return jsonify(error="Missing required fields"), 400
    
    claims = get_jwt()
    guest_id = claims['sub']
    user_type = claims.get('role')
    
    # Check if the current user is a guest
    if user_type != 'guest':
        return jsonify(error="Only guests can post attendance requests."), 403

    event_id = data.get('event_id')
    status = data.get('status')

    try:
        connection = get_flask_database_connection(current_app)
        attendance_repo = AttendanceRepository(connection)

        # Check if attendance already exists
        if attendance_repo.check_attendance_exists(guest_id, event_id):
            return jsonify(error="Attendance request already exists for this event"), 409
        
        created_attendance = attendance_repo.create_attendance(guest_id=guest_id, event_id=event_id, status=status)

        # Create an attendance request notification
        notification_repo = NotificationRepository(connection)
        event_repo = EventRepository(connection)
        guest_repo = GuestRepository(connection)

        guest = guest_repo.find(guest_id)  # Fetch the guest details using the guest_id from the JWT
        event = event_repo.find(event_id)
        
        notification = Notification(
            recipient_id=event.band_id,
            recipient_type='band',
            event_id=event_id,
            notification_type='attendance_request',
            message=f'Guest {guest.name} has requested to attend your show: {event.event_name}.',
        )
        
        notification_repo.create(notification)
        return jsonify(attendance=created_attendance.to_dict()), 201
    except Exception as e:
        return jsonify(error=str(e)), 400


@attendance_bp.route('/events/<int:event_id>/attendees', methods=['GET'])
@jwt_required()
@token_required
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

@attendance_bp.route('/events/<int:event_id>/attendees/<int:attendance_id>/accept', methods=['POST'])
@jwt_required()
@token_required
def accept_attendee(event_id, attendance_id):
    current_band_id = get_jwt_identity()  # Assuming this is the band ID stored in the JWT token
    
    try:
        connection = get_flask_database_connection(current_app)
        attendance_repo = AttendanceRepository(connection)
        event_repo = EventRepository(connection)
        notification_repo = NotificationRepository(connection)
        guest_repo = GuestRepository(connection)

        # Check if the event exists
        event = event_repo.find(event_id)
        if not event:
            return jsonify(error="Event not found"), 404
        
        # Check if the current band is associated with the event
        if event.band_id != current_band_id:
            return jsonify(error="Unauthorized to accept attendees for this event"), 403

        # Update the attendance status to "attending"
        updated_attendance = attendance_repo.update_attendance_status(attendance_id, "attending")

        # Fetch guest information to send notification
        guest_id = updated_attendance.guest_id
        guest = guest_repo.find(guest_id)

        # Create notification for guest
        notification = Notification(
            recipient_id=guest_id,
            recipient_type='guest',
            event_id=event_id,
            notification_type='attendance_accepted',
            message=f'Your request to attend the event {event.event_name} has been accepted!',
        )
        notification_repo.create(notification)

        return jsonify(attendance=updated_attendance.to_dict()), 200

    except Exception as e:
        return jsonify(error=str(e)), 400

@attendance_bp.route('/events/<int:event_id>/attendees/<int:attendance_id>/reject', methods=['POST'])
@jwt_required()
@token_required
def reject_attendee(event_id, attendance_id):
    current_band_id = get_jwt_identity()  # Assuming this is the band ID stored in the JWT token
    
    try:
        connection = get_flask_database_connection(current_app)
        attendance_repo = AttendanceRepository(connection)
        event_repo = EventRepository(connection)
        notification_repo = NotificationRepository(connection)
        guest_repo = GuestRepository(connection)

        # Check if the event exists
        event = event_repo.find(event_id)
        if not event:
            return jsonify(error="Event not found"), 404
        
        # Check if the current band is associated with the event
        if event.band_id != current_band_id:
            return jsonify(error="Unauthorized to reject attendees for this event"), 403

        # Update the attendance status to "rejected"
        updated_attendance = attendance_repo.update_attendance_status(attendance_id, "rejected")

        # Fetch guest information to send notification
        guest_id = updated_attendance.guest_id
        guest = guest_repo.find(guest_id)

        # Create notification for guest
        notification = Notification(
            recipient_id=guest_id,
            recipient_type='guest',
            event_id=event_id,
            notification_type='attendance_response',
            message=f'Your request to attend the event {event.event_name} has been rejected.',
        )
        notification_repo.create(notification)

        return jsonify(attendance=updated_attendance.to_dict()), 200

    except Exception as e:
        return jsonify(error=str(e)), 400
