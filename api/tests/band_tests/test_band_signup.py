import os
import pytest
from flask import Flask
from api.bands.band_signup import sign_up_band  # Import the sign_up_band function
from api.bands.band_model import Band
from api.common.db import get_flask_database_connection

@pytest.fixture(scope='module')
def app():
    # Set up the Flask app and set it in testing mode
    app = Flask(__name__)
    app.config['TESTING'] = True
    os.environ['APP_ENV'] = 'test'
    
    with app.app_context():
        # Initialize the database connection
        connection = get_flask_database_connection(app)
        
        # Optionally, seed the test database if needed
        connection.seed("../seeds/bands_table_test_data.sql")
        yield app 

def test_sign_up_band_valid_details(app):
    with app.app_context():
        new_band = Band(
            band_name="The Who",
            band_email="thewho@example.com",
            password="SecureP@ssw0rd",
            oauth_provider=None,
            oauth_provider_id=None
        )
        
        result = sign_up_band(new_band)
        assert result == "New Band created and stored in db."
        
        # Verify that the band is in the database
        connection = get_flask_database_connection(app)
        bands = connection.execute("SELECT * FROM bands WHERE band_email = %s", [new_band.band_email])
        assert len(bands) == 1
        assert bands[0]['band_name'] == "The Who"

def test_sign_up_band_invalid_email(app):
    with app.app_context():
        invalid_band = Band(
            band_name="The Rockers",
            band_email="invalid-email",
            password="SecureP@ssw0rd",
            oauth_provider=None,
            oauth_provider_id=None
        )
        with pytest.raises(ValueError, match="Invalid email format"):
            sign_up_band(invalid_band)

def test_sign_up_band_invalid_password(app):
    with app.app_context():
        invalid_band = Band(
            band_name="The Rockers",
            band_email="rockers@example.com",
            password="short",
            oauth_provider=None,
            oauth_provider_id=None
        )
        with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
            sign_up_band(invalid_band)

def test_sign_up_band_email_exists(app):
    with app.app_context():
        existing_band = Band(
            band_name="Existing Band",
            band_email="rockers@example.com",  # This email should already exist in the test database
            password="SecureP@ssw0rd",
            oauth_provider=None,
            oauth_provider_id=None
        )
        with pytest.raises(ValueError, match='Email already in use'):
            sign_up_band(existing_band)

def test_sign_up_band_name_empty_string(app):
    with app.app_context():
        invalid_band = Band(
            band_name="   ",  # Empty name
            band_email="new.band@example.com",
            password="SecureP@ssw0rd",
            oauth_provider=None,
            oauth_provider_id=None
        )
        with pytest.raises(ValueError, match='Band name cannot be empty'):
            sign_up_band(invalid_band)
