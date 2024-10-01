import pytest
from api.common.db import get_flask_database_connection
from flask import Flask
import os
from datetime import datetime
from api.requests.request_model import Request
from api.requests.request_create import validate_create_request

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
        connection.seed("../seeds/requests_table_test_data.sql")
        connection.seed("../seeds/guests_table_test_data.sql")
        connection.seed("../seeds/events_table_test_data.sql")
        yield app 

def test_create_new_request_valid_details(app):
    with app.app_context():
        # Define the test data
        request_date = datetime(2024, 9, 10)
        
        test_request = Request(
            song_name="Wonderwall",
            guest_id=1,
            event_id=1,
            created_at=request_date,
            updated_at=request_date
        )

        result = validate_create_request(test_request)
        assert result == "Request successfully created."

        connection = get_flask_database_connection(app)
        request = connection.execute("SELECT * FROM requests WHERE song_name = %s", [test_request.song_name])
        assert len(request) == 1
        assert request[0]['song_name'] == "Wonderwall"

def test_create_request_empty_song_name(app):
    with app.app_context():
        request_date = datetime(2024, 9, 10)
        
        invalid_request = Request(
            song_name="",
            guest_id=1,
            event_id=1,
            created_at=request_date,
            updated_at=request_date
        )
        with pytest.raises(ValueError, match="Song name cannot be empty"):
            validate_create_request(invalid_request)

def test_create_request_missing_guest_id(app):
    with app.app_context():
        request_date = datetime(2024, 9, 10)
        
        invalid_request = Request(
            song_name="Wonderwall",
            guest_id=None,  # Missing guest ID
            event_id=1,
            created_at=request_date,
            updated_at=request_date
        )
        with pytest.raises(ValueError, match="Guest ID is required"):
            validate_create_request(invalid_request)

def test_create_request_missing_event_id(app):
    with app.app_context():
        request_date = datetime(2024, 9, 10)
        
        invalid_request = Request(
            song_name="Wonderwall",
            guest_id=1,
            event_id=None,  # Missing event ID
            created_at=request_date,
            updated_at=request_date
        )
        with pytest.raises(ValueError, match="Event ID is required"):
            validate_create_request(invalid_request)

# Add more tests as needed to cover other edge cases
