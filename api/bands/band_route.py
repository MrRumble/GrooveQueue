from flask import Blueprint, request, jsonify, current_app
from api.bands.band_model import Band
from api.bands.band_repository import BandRepository
from api.bands.band_signup import sign_up_band  # Function for signing up a band
from api.common.db import get_flask_database_connection
from api.auth.token_manager import TokenManager
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
from werkzeug.security import check_password_hash
from datetime import timedelta
from api.auth.token_manager import TokenManager
from api.auth.token_fixture import token_required
from werkzeug.utils import secure_filename
import os

# Blueprint setup
band_bp = Blueprint('band_bp', __name__)

MAX_FILE_SIZE = 10 * 1024 * 1024

# Route to get all bands
@band_bp.route('/bands', methods=['GET'])
def get_all_bands():
    connection = get_flask_database_connection(current_app)
    band_repo = BandRepository(connection)
    all_bands = band_repo.find_all()

    # Convert list of Band objects to list of dictionaries
    bands_dict = [band.to_dict() for band in all_bands]

    return jsonify(bands_dict), 200

@band_bp.route('/bands', methods=['POST'])
def create_band():
    # Handle form data and files
    data = request.form
    file = request.files.get('profile_picture')

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

    # Handle image upload
    profile_picture_path = None
    if file:
        # Check file size
        if len(file.read()) > MAX_FILE_SIZE:
            return jsonify(error="File size exceeds 2 MB limit."), 400
        file.seek(0)  # Reset file pointer after reading

        # Validate file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return jsonify(error="Invalid image format. Only PNG, JPG, and GIF are allowed."), 400
        
        # Save the file
        filename = secure_filename(file.filename)
        upload_folder = 'api/static/uploads/profile_pictures'  # Adjust your path accordingly
        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, filename))
        
        # Save the path to the profile picture
        profile_picture_path = os.path.join(upload_folder, filename)

    # Create a new Band object
    band = Band(
        band_name=data.get('band_name'),
        band_email=data.get('band_email'),
        password=data.get('password'),
        oauth_provider=oauth_provider,
        oauth_provider_id=oauth_provider_id,
        profile_picture_path=profile_picture_path  # Include profile picture path
    )

    try:
        result = sign_up_band(band)
        return jsonify(message=result), 201
    except ValueError as e:
        return jsonify(error=str(e)), 400
    
@band_bp.route('/bands/login', methods=['POST'])
def login_band():
    data = request.json
    email = data.get('band_email')
    password = data.get('password')

    if not email or not password:
        return jsonify(error="Missing email or password"), 400  

    connection = get_flask_database_connection(current_app)
    band_repo = BandRepository(connection)

    try:
        band = band_repo.find_by_email(email)
    except ValueError as e:
        return jsonify(error=str(e)), 404

    if not band or not check_password_hash(band.password, password):
        return jsonify(error="Invalid email or password"), 401

    # Include band information in the JWT token
    additional_claims = {
        "role": "band",
        "band_email": band.band_email,
        "band_id": band.band_id,
        "band_name": band.band_name,
        "profile_picture_path": f"http://localhost:5001/static/uploads/profile_pictures/{os.path.basename(band.profile_picture_path)}"
    }

    access_token = create_access_token(
        identity=band.band_id,
        expires_delta=timedelta(minutes=30),
        additional_claims=additional_claims
    )
    
    # Return only the access_token in the response, as the band info is now in the token
    return jsonify(access_token=access_token), 200


@band_bp.route('/band/current', methods=['GET'])
@jwt_required()
@token_required
def get_current_band():
    # Get current band information from the token
    current_band_id = get_jwt_identity()
    current_band_claims = get_jwt()

    # Prepare band details dictionary to return
    band_dict = {
        "band_id": current_band_id,
        "band_name": current_band_claims.get("band_name"),
        "band_email": current_band_claims.get("band_email"),
        "profile_picture_path": current_band_claims.get("profile_picture_path")
    }

    return jsonify(band_dict), 200

@band_bp.route('/band/logout', methods=['POST'])
def logout_band():

    token_manager = TokenManager()
    token = request.headers.get('Authorization', None)

    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]  # Extract the token part

        # Blacklist the token
        token_manager.blacklist_token(token)

        return jsonify(message="Band logged out successfully"), 200
    
    return jsonify(message="Token not provided or invalid"), 400

