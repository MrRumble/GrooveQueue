from flask import Blueprint, request, jsonify, current_app
from api.guests.guest_model import Guest
from api.guests.guest_repository import GuestRepository
from api.guests.guest_signup import sign_up_guest
from api.common.db import get_flask_database_connection
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

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

# Route to create a new guest
@guest_bp.route('/guests', methods=['POST'])
def create_guest():
    data = request.json

    # Validate the input data
    if not data or not all(key in data for key in ['name', 'email', 'password']):
        return jsonify(error="Missing required fields"), 400
    
    # validate OAuth2 fields if they are provided
    oauth_provider = data.get('oauth_provider')
    oauth_provider_id = data.get('oauth_provider_id')

    if oauth_provider and not isinstance(oauth_provider, str):
        return jsonify(error="Invalid OAuth provider format"), 400

    if oauth_provider_id and not isinstance(oauth_provider_id, str):
        return jsonify(error="Invalid OAuth provider ID format"), 400

    guest = Guest(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password'),
        oauth_provider=oauth_provider,
        oauth_provider_id=oauth_provider_id
    )

    try:
        result = sign_up_guest(guest)
        return jsonify(message=result), 201
    except ValueError as e:
        return jsonify(error=str(e)), 400

@guest_bp.route('/guests/login', methods=['POST'])
def login_guest():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify(error="Missing email or password"), 400

    connection = get_flask_database_connection(current_app)
    guest_repo = GuestRepository(connection)
    try:
        guest = guest_repo.find_by_email(email)
    except ValueError as e:
        return jsonify(error=str(e)), 404

    if not guest or not check_password_hash(guest.password, password):
        return jsonify(error="Invalid email or password"), 401

    access_token = create_access_token(
        identity=guest.id, 
        expires_delta=timedelta(minutes=30),
        additional_claims={"role": "guest"}  # Include role in the token
    )
    return jsonify(access_token=access_token, email=guest.email, guest_id=guest.id, name=guest.name), 200

@guest_bp.route('/guest/current', methods=['GET'])
@jwt_required()
def get_current_guest():
    current_guest_id = get_jwt_identity()
    connection = get_flask_database_connection(current_app)
    guest_repo = GuestRepository(connection)
    guest = guest_repo.find(current_guest_id)

    if not guest:
        return jsonify(error="Guest not found"), 404

    return jsonify(guest.to_dict()), 200

@guest_bp.route('/guest/logout', methods=['POST'])
def logout_guest():
    return jsonify(message="Guest logged out successfully"), 200
