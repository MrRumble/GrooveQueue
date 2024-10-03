import pytest
from api.common.db import get_flask_database_connection
from flask import Flask
import os
from datetime import datetime, timedelta
from api.events.event_model import Event
from api.events.event_create import create_event

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
        connection.seed("../seeds/events_table_test_data.sql")
        connection.seed("../seeds/bands_table_test_data.sql")
        yield app 

def test_create_new_event_valid_details(app):
        with app.app_context():
            # Create a specific datetime for testing
            event_start = datetime(2024, 9, 1, 18, 0)
            event_end = event_start + timedelta(hours=4)  

            test_event = Event(
                event_name="Rock Concert",
                location="Madison Square Garden",
                event_start=event_start,
                event_end=event_end,
                qr_code_content="https://example.com/event/1",
                band_id=1,
                max_requests_per_user=3,
                created_at=datetime(2024, 8, 1, 12, 0),  # August 1, 2024, 12:00
                updated_at=datetime(2024, 8, 15, 12, 0)  # Updated on August 15, 2024, 12:00
            )

            create_event(test_event)

            connection = get_flask_database_connection(app)
            event = connection.execute("SELECT * FROM events WHERE event_name = %s", [test_event.event_name])
            assert len(event) == 1
            assert event[0]['event_name'] == "Rock Concert"

def test_create_event_invalid_name(app):
    with app.app_context():
            event_start = datetime(2024, 9, 1, 18, 0)
            event_end = event_start + timedelta(hours=4)  

            invalid_event = Event(
                event_name="  ",
                location="Madison Square Garden",
                event_start=event_start,
                event_end=event_end,
                qr_code_content="https://example.com/event/1",
                band_id=1,
                created_at=datetime(2024, 8, 1, 12, 0),  # August 1, 2024, 12:00
                updated_at=datetime(2024, 8, 15, 12, 0)  # Updated on August 15, 2024, 12:00
            )
            with pytest.raises(ValueError, match="Invalid event name format"):
                create_event(invalid_event)

def test_create_event_invalid_location(app):
    with app.app_context():
            event_start = datetime(2024, 9, 1, 18, 0)
            event_end = event_start + timedelta(hours=4)  

            invalid_event = Event(
                event_name="Rock Concert",
                location="   ",
                event_start=event_start,
                event_end=event_end,
                qr_code_content="https://example.com/event/1",
                band_id=1,
                created_at=datetime(2024, 8, 1, 12, 0),  # August 1, 2024, 12:00
                updated_at=datetime(2024, 8, 15, 12, 0)  # Updated on August 15, 2024, 12:00
            )
            with pytest.raises(ValueError, match="Location cannot be empty"):
                create_event(invalid_event)

def test_create_event_end_before_start(app):
    with app.app_context():
        event_start = datetime(2024, 9, 1, 18, 0)
        event_end = event_start - timedelta(hours=1)  # End time is before start time

        invalid_event = Event(
            event_name="Rock Concert",
            location="Madison Square Garden",
            event_start=event_start,
            event_end=event_end,
            qr_code_content="https://example.com/event/1",
            band_id=1,
            created_at=datetime(2024, 8, 1, 12, 0),
            updated_at=datetime(2024, 8, 15, 12, 0)
        )
        with pytest.raises(ValueError, match="Event end time must be after start time"):
            create_event(invalid_event)

def test_create_event_missing_band_id(app):
    with app.app_context():
        event_start = datetime(2024, 9, 1, 18, 0)
        event_end = event_start + timedelta(hours=4)  

        invalid_event = Event(
            event_name="Rock Concert",
            location="Madison Square Garden",
            event_start=event_start,
            event_end=event_end,
            qr_code_content="https://example.com/event/1",
            band_id=None,  # Missing band ID
            created_at=datetime(2024, 8, 1, 12, 0),
            updated_at=datetime(2024, 8, 15, 12, 0)
        )
        with pytest.raises(ValueError, match="Band ID is required"):
            create_event(invalid_event)

def test_create_event_empty_qr_code(app):
    with app.app_context():
        event_start = datetime(2024, 9, 1, 18, 0)
        event_end = event_start + timedelta(hours=4)  

        invalid_event = Event(
            event_name="Rock Concert",
            location="Madison Square Garden",
            event_start=event_start,
            event_end=event_end,
            qr_code_content="",  # Empty QR code content
            band_id=1,
            created_at=datetime(2024, 8, 1, 12, 0),
            updated_at=datetime(2024, 8, 15, 12, 0)
        )
        with pytest.raises(ValueError, match="QR code content cannot be empty"):
            create_event(invalid_event)