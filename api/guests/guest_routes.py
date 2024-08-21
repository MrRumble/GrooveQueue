from flask import Blueprint, request, jsonify, current_app
from api.guests.guest_model import Guest
from api.guests.guest_repository import GuestRepository
from api.common.db import get_flask_database_connection

# Blueprint setup
guest_bp = Blueprint('guest_bp', __name__)

# Route to get all guests
@guest_bp.route('/guests', methods=['GET'])
def get_all_guests():
    connection = get_flask_database_connection(current_app)
    guest_repo = GuestRepository(connection)
    all_guests = guest_repo.find_all()

    # Convert list of Guest objects to list of dictionaries
    guests_dict = [guest.to_dict() for guest in all_guests]

    return jsonify(guests_dict), 200 