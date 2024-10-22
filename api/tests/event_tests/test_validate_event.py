import pytest
from api.common.db import get_flask_database_connection
from flask import Flask
import os
from datetime import datetime, timedelta
from api.events.event_model import Event
from api.events.validate_event import validate_event

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
        event_start = datetime(2030, 9, 1, 18, 0)
        event_end = event_start + timedelta(hours=4)

        test_event = Event(
            event_name="Rock Concert",
            location="Madison Square Garden",
            event_start=event_start,
            event_end=event_end,
            qr_code_content="https://example.com/event/1",
            band_id=1,
            max_requests_per_user=3,
            created_at=datetime(2024, 8, 1, 12, 0),
            updated_at=datetime(2024, 8, 15, 12, 0)
        )

        is_valid, error_message = validate_event(test_event)
        assert is_valid is True  # Expecting True for valid event
        assert error_message == ""  # No error message should be present

def test_create_event_invalid_name(app):
    with app.app_context():
        event_start = datetime(2024, 9, 1, 18, 0)
        event_end = event_start + timedelta(hours=4)

        invalid_event = Event(
            event_name="  ",  # Invalid event name
            location="Madison Square Garden",
            event_start=event_start,
            event_end=event_end,
            qr_code_content="https://example.com/event/1",
            band_id=1,
            created_at=datetime(2024, 8, 1, 12, 0),
            updated_at=datetime(2024, 8, 15, 12, 0)
        )

        is_valid, error_message = validate_event(invalid_event)
        assert is_valid is False  # Expecting False for invalid event name
        assert error_message == "Event name cannot be empty."  # Check for specific error message

def test_create_event_invalid_location(app):
    with app.app_context():
        event_start = datetime(2024, 9, 1, 18, 0)
        event_end = event_start + timedelta(hours=4)

        invalid_event = Event(
            event_name="Rock Concert",
            location="   ",  # Invalid location
            event_start=event_start,
            event_end=event_end,
            qr_code_content="https://example.com/event/1",
            band_id=1,
            created_at=datetime(2024, 8, 1, 12, 0),
            updated_at=datetime(2024, 8, 15, 12, 0)
        )

        is_valid, error_message = validate_event(invalid_event)
        assert is_valid is False  # Expecting False for invalid location
        assert error_message == "Location cannot be empty."  # Check for specific error message

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

        is_valid, error_message = validate_event(invalid_event)
        assert is_valid is False  # Expecting False for event with end time before start time
        assert error_message == "Event start must be before event end."  # Check for specific error message

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

        is_valid, error_message = validate_event(invalid_event)
        assert is_valid is False  # Expecting False for missing band ID
        assert error_message == "Band ID must be provided."  # Check for specific error message

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

        is_valid, error_message = validate_event(invalid_event)
        assert is_valid is False  # Expecting False for empty QR code content
        assert error_message == "QR code content must be provided."  # Check for specific error message

def test_create_event_start_in_the_past(app):
    with app.app_context():
        # Set the start time to a time in the past
        event_start = datetime.now() - timedelta(days=1)  # One day in the past
        event_end = event_start + timedelta(hours=4)  # End time after start time

        invalid_event = Event(
            event_name="Rock Concert",
            location="Madison Square Garden",
            event_start=event_start,
            event_end=event_end,
            qr_code_content="https://example.com/event/1",
            band_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        is_valid, error_message = validate_event(invalid_event)
        assert is_valid is False  # Expecting False for event with start time in the past
        assert error_message == "Event start time cannot be in the past."  # Check for specific error message

def test_create_event_longer_than_one_day(app):
    with app.app_context():
        event_start = datetime(2030, 9, 1, 18, 0)
        event_end = event_start + timedelta(days=2)  # 2 days long, which is invalid

        invalid_event = Event(
            event_name="Rock Concert",
            location="Madison Square Garden",
            event_start=event_start,
            event_end=event_end,
            qr_code_content="https://example.com/event/1",
            band_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        is_valid, error_message = validate_event(invalid_event)
        assert is_valid is False  # Expecting False for event longer than one day
        assert error_message == "Event duration cannot exceed 24 hours."  # Check for specific error message
