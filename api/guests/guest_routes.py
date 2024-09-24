from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for, flash, session
from api.guests.guest_model import Guest
from api.guests.guest_repository import GuestRepository
from api.guests.guest_signup import sign_up_guest
from api.common.db import get_flask_database_connection
from authlib.integrations.flask_client import OAuth
from werkzeug.security import check_password_hash
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
    
    # Validate the input data
    if not data or not all(key in data for key in ['name', 'email', 'password']):
        flash("Missing required fields", "error")
        return redirect(url_for('guest_bp.sign_up_guest_route'))

    # Validate OAuth2 fields if they are provided
    oauth_provider = data.get('oauth_provider')
    oauth_provider_id = data.get('oauth_provider_id')

    if oauth_provider and not isinstance(oauth_provider, str):
        flash("Invalid OAuth provider format", "error")
        return redirect(url_for('guest_bp.sign_up_guest_route'))

    if oauth_provider_id and not isinstance(oauth_provider_id, str):
        flash("Invalid OAuth provider ID format", "error")
        return redirect(url_for('guest_bp.sign_up_guest_route'))

    guest = Guest(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password'),
        oauth_provider=oauth_provider,
        oauth_provider_id=oauth_provider_id
    )

    try:
        sign_up_guest(guest)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('guest_bp.login_route'))
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('guest_bp.sign_up_guest_route'))
    


# Route to render the signup page
@guest_bp.route('/signupguest', methods=['GET'])
def sign_up_guest_route():
    return render_template('signup_guest.html')

@guest_bp.route('/login', methods=['GET'])
def login_route():
    return render_template('login_guest.html')

@guest_bp.route('/login', methods=['POST'])
def login_guest_route():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    print('entered login', email, password)

    connection = get_flask_database_connection(current_app)
    guest_repo = GuestRepository(connection)
    guest = guest_repo.find_by_email(email)
    print('guest', guest)
    print('guest.password', guest.password)
    
    if guest and check_password_hash(guest.password, password):
        session['guest_id'] = guest.id
        session['guest_name'] = guest.name
        session['guest_email'] = guest.email
        return render_template('login_guest_success.html')
    else:
        flash("Invalid email or password", "error")
        return redirect(url_for('guest_bp.login_route'))
    
@guest_bp.route('/logout', methods=['POST'])
def logout_user():
    session.clear()
    return redirect(url_for('guest_bp.login_route'))
    
