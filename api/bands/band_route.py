from flask import Blueprint, request, jsonify, current_app, render_template
from api.bands.band_model import Band
from api.bands.band_repository import BandRepository
from api.bands.band_signup import sign_up_band  # Function for signing up a band
from api.common.db import get_flask_database_connection

# Blueprint setup
band_bp = Blueprint('band_bp', __name__)

# Route to get all bands
@band_bp.route('/bands', methods=['GET'])
def get_all_bands():
    connection = get_flask_database_connection(current_app)
    band_repo = BandRepository(connection)
    all_bands = band_repo.find_all()

    # Convert list of Band objects to list of dictionaries
    bands_dict = [band.to_dict() for band in all_bands]

    return jsonify(bands_dict), 200

# Route to create a new band
@band_bp.route('/bands', methods=['POST'])
def create_band():
    data = request.json

    # Validate the input data
    if not data or not all(key in data for key in ['band_name', 'band_email', 'password']):
        return jsonify(error="Missing required fields"), 400
    
    # Validate OAuth2 fields if they are provided
    oauth_provider = data.get('oauth_provider')
    oauth_provider_id = data.get('oauth_provider_id')

    if oauth_provider and not isinstance(oauth_provider, str):
        return jsonify(error="Invalid OAuth provider format"), 400

    if oauth_provider_id and not isinstance(oauth_provider_id, str):
        return jsonify(error="Invalid OAuth provider ID format"), 400

    band = Band(
        band_name=data.get('band_name'),
        band_email=data.get('band_email'),
        password=data.get('password'),
        oauth_provider=oauth_provider,
        oauth_provider_id=oauth_provider_id
    )

    try:
        result = sign_up_band(band)
        return jsonify(message=result), 201
    except ValueError as e:
        return jsonify(error=str(e)), 400

@band_bp.route('/signupband', methods=['GET'])
def sign_up_band_route():
    return render_template('signup_band.html')