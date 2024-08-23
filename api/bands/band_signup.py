from api.bands.band_repository import BandRepository
from api.bands.band_model import Band
from api.common.db import get_flask_database_connection
from api.utils.validators import validate_email, validate_password
from flask import current_app

def sign_up_band(band: Band) -> str:
    connection = get_flask_database_connection(current_app)
    band_repo = BandRepository(connection)
    
    # Validate email format
    if not validate_email(band.band_email):
        raise ValueError("Invalid email format")
    
    # Validate password strength
    if not validate_password(band.password):
        raise ValueError("Password must be at least 8 characters long, include uppercase, lowercase, number, and special character")
    
    # Validate band name
    if not band.band_name or band.band_name.strip() == "":
        raise ValueError("Band name cannot be empty")
    
    # Check if email already exists
    if band_repo.email_exists(band.band_email):
        raise ValueError("Email already in use")
    
    # If validations pass, create the band
    band_repo.create(band)
    return "New Band created and stored in db."
