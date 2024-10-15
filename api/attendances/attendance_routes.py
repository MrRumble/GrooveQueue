from flask import Blueprint, request, jsonify, current_app
from api.attendances.attendance_repository import AttendanceRepository
from api.attendances.attendance_model import Attendance
from api.events.event_create import create_event as create_new_event
from api.common.db import get_flask_database_connection
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Blueprint setup
attendace_bp = Blueprint('attendance_bp', __name__)

"""
Change create_attendance to take Attendence object as parameter.
"""
@attendace_bp.route('/attendance', methods=['POST'])
@jwt_required()
def post_attendance():
    data = request.json
    print(data)

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