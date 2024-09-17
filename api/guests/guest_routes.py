from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for, flash
from api.guests.guest_model import Guest
from api.guests.guest_repository import GuestRepository
from api.guests.guest_signup import sign_up_guest
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

# Route to create a new guest
@guest_bp.route('/guests', methods=['POST'])
def create_guest():
    data = request.form
    
    print(data)

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

# Route to render the signup page
@guest_bp.route('/signupguest', methods=['GET'])
def sign_up_guest_route():
    return render_template('signup_guest.html')
