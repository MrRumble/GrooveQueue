import os
import pytest
from flask import Flask
from api.guests.guest_signup import sign_up_guest
from api.guests.guest_model import Guest
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
        connection.seed("../seeds/guests_table_test_data.sql")
        yield app 
    
def test_sign_up_guest_valid_details(app):
    with app.app_context():
        new_guest = Guest(
            name="James Rumble",
            email="jim@example.com",
            password="SecureP@ssw0rd",
            oauth_provider=None,
            oauth_provider_id=None
        )
        
        result = sign_up_guest(new_guest)
        assert result == "New Guest created and stored in db."
        
        # Verify that the guest is in the database
        connection = get_flask_database_connection(app)
        guests = connection.execute("SELECT * FROM guests WHERE email = %s", [new_guest.email])
        assert len(guests) == 1
        assert guests[0]['name'] == "James Rumble"

def test_sign_up_guest_invalid_email(app):
    with app.app_context():
        invalid_guest = Guest(
            name="James Rumble",
            email="invalid-email",
            password="SecureP@ssw0rd",
            oauth_provider=None,
            oauth_provider_id=None
        )
        with pytest.raises(ValueError, match="Invalid email format"):
            sign_up_guest(invalid_guest)

def test_sign_up_guest_invalid_password(app):
    with app.app_context():
        invalid_guest = Guest(
            name="James Rumble",
            email="jim@example.com",
            password="short",
            oauth_provider=None,
            oauth_provider_id=None
        )
        with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
            sign_up_guest(invalid_guest)

def test_sign_up_guest_email_exists(app):
    with app.app_context():
        invalid_guest = Guest(
            name="James Rumble",
            email="john.doe@example.com",
            password="SecureP@ssw0rd",
            oauth_provider=None,
            oauth_provider_id=None
        )
        with pytest.raises(ValueError, match='Email already in use'):
            sign_up_guest(invalid_guest)

def test_sign_up_guest_name_empty_string(app):
    with app.app_context():
        invalid_guest = Guest(
            name="   ",
            email="john.doe@example.com",
            password="SecureP@ssw0rd",
            oauth_provider=None,
            oauth_provider_id=None
        )
        with pytest.raises(ValueError, match='Name cannot be empty'):
            sign_up_guest(invalid_guest)
