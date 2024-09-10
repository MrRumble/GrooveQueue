from api.events.event_model import Event
from api.events.event_repository import EventRepository
import datetime

def test_find_event_by_id(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/events_table_test_data.sql")
    
    # Create an instance of EventRepository
    event_repo = EventRepository(db_connection)
    
    # Find the event with id 1
    result = event_repo.find(1)
    
    # Create the expected Event object
    expected_event = Event(
        event_id=1,
        event_name='Rocking the City',
        location='Madison Square Garden, New York',
        event_start=datetime.datetime(2024, 9, 15, 19, 0),
        event_end=datetime.datetime(2024, 9, 15, 23, 0),
        qr_code_content='rocking_the_city_qr_code_001',
        band_id=1,
        created_at=None,  # Handle timestamp comparison separately
        updated_at=None   # Handle timestamp comparison separately
    )
    
    # Check if the result is not None
    assert result is not None

    # Compare individual attributes, excluding created_at and updated_at
    assert result.event_id == expected_event.event_id
    assert result.event_name == expected_event.event_name
    assert result.location == expected_event.location
    assert result.event_start == expected_event.event_start
    assert result.event_end == expected_event.event_end
    assert result.qr_code_content == expected_event.qr_code_content
    assert result.band_id == expected_event.band_id

    # Optionally, compare timestamps with some tolerance if needed
    assert abs((result.created_at - expected_event.created_at).total_seconds()) < 1
    assert abs((result.updated_at - expected_event.updated_at).total_seconds()) < 1

def test_find_all_events(db_connection):
    # Seed the database with the new test data
    db_connection.seed("../seeds/events_table_test_data.sql")
    
    # Create an instance of EventRepository
    event_repo = EventRepository(db_connection)
    
    # Fetch all events from the repository
    results = event_repo.find_all()
    
    # Define the expected Event objects based on the seed data
    expected_events = [
        Event(
            event_id=1,
            event_name='Rocking the City',
            location='Madison Square Garden, New York',
            event_start=datetime.datetime(2024, 9, 15, 19, 0),
            event_end=datetime.datetime(2024, 9, 15, 23, 0),
            qr_code_content='rocking_the_city_qr_code_001',
            band_id=1,
            created_at=None,  # Handle timestamps separately
            updated_at=None   # Handle timestamps separately
        ),
        Event(
            event_id=2,
            event_name='Jazz Night',
            location='Blue Note, New York',
            event_start=datetime.datetime(2024, 10, 5, 20, 0),
            event_end=datetime.datetime(2024, 10, 5, 23, 59),
            qr_code_content='jazz_night_qr_code_002',
            band_id=3,
            created_at=None,
            updated_at=None
        ),
        Event(
            event_id=3,
            event_name='The Big Apple Concert',
            location='Central Park, New York',
            event_start=datetime.datetime(2024, 10, 20, 18, 0),
            event_end=datetime.datetime(2024, 10, 20, 22, 0),
            qr_code_content='big_apple_concert_qr_code_003',
            band_id=2,
            created_at=None,
            updated_at=None
        ),
        Event(
            event_id=4,
            event_name='Summer Festival',
            location='Hyde Park, London',
            event_start=datetime.datetime(2024, 8, 25, 12, 0),
            event_end=datetime.datetime(2024, 8, 25, 22, 0),
            qr_code_content='summer_festival_qr_code_004',
            band_id=1,
            created_at=None,
            updated_at=None
        ),
        Event(
            event_id=5,
            event_name='Autumn Jazz Festival',
            location='Royal Albert Hall, London',
            event_start=datetime.datetime(2024, 11, 10, 17, 0),
            event_end=datetime.datetime(2024, 11, 10, 22, 0),
            qr_code_content='autumn_jazz_festival_qr_code_005',
            band_id=3,
            created_at=None,
            updated_at=None
        ),
    ]
    
    # Check if the number of results is as expected
    assert len(results) == len(expected_events)
    
    # Compare individual attributes of each event
    for result, expected_event in zip(results, expected_events):
        assert result.event_id == expected_event.event_id
        assert result.event_name == expected_event.event_name
        assert result.location == expected_event.location
        assert result.event_start == expected_event.event_start
        assert result.event_end == expected_event.event_end
        assert result.qr_code_content == expected_event.qr_code_content
        assert result.band_id == expected_event.band_id
        
        # Optionally, compare timestamps with some tolerance
        if expected_event.created_at:
            assert abs((result.created_at - expected_event.created_at).total_seconds()) < 1
        else:
            assert result.created_at is None
        
        if expected_event.updated_at:
            assert abs((result.updated_at - expected_event.updated_at).total_seconds()) < 1
        else:
            assert result.updated_at is None
        
def test_create_event(db_connection):
    db_connection.seed("../seeds/events_table_test_data.sql")
    
    # Create an instance of EventRepository
    event_repo = EventRepository(db_connection)
    
    # Create a new Event object
    new_event = Event(
        event_name='New Event',
        location='New Venue',
        event_start=datetime.datetime(2023, 12, 25, 18, 0),
        event_end=datetime.datetime(2023, 12, 25, 22, 0),
        qr_code_content='newqrcodecontent',
        band_id=1
    )
    
    # Insert the new event into the database
    event_repo.create(new_event)
    found_event = event_repo.find(6)  # Assuming ID 4 is the new event
    assert found_event.event_id == 6
    assert found_event.event_name == "New Event"
    assert found_event.location == "New Venue"
    assert found_event.event_start == datetime.datetime(2023, 12, 25, 18, 0)
    assert found_event.event_end == datetime.datetime(2023, 12, 25, 22, 0)
    assert found_event.qr_code_content == 'newqrcodecontent'
    assert found_event.band_id == 1
    
def test_update_event(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/events_table_test_data.sql")
    
    # Create an instance of EventRepository
    event_repo = EventRepository(db_connection)
    
    # Find an existing event to update
    event_to_update = event_repo.find(1)
    
    # Modify the event's details
    event_to_update.event_name = "Updated Event Name"
    event_to_update.location = "Updated Venue"
    event_to_update.event_start = datetime.datetime(2024, 1, 1, 19, 0)
    event_to_update.event_end = datetime.datetime(2024, 1, 1, 23, 59)
    event_to_update.qr_code_content = "updatedqrcodecontent"
    event_to_update.band_id = 2
    
    # Perform the update operation
    event_repo.update(event_to_update.event_id, event_to_update)
    
    # Fetch the updated event from the database
    updated_event = event_repo.find(event_to_update.event_id)
    
    # Assert the updated fields
    assert updated_event.event_name == "Updated Event Name"
    assert updated_event.location == "Updated Venue"
    assert updated_event.event_start == datetime.datetime(2024, 1, 1, 19, 0)
    assert updated_event.event_end == datetime.datetime(2024, 1, 1, 23, 59)
    assert updated_event.qr_code_content == "updatedqrcodecontent"
    assert updated_event.band_id == 2
    
    # Check that the IDs match
    assert updated_event.event_id == event_to_update.event_id

def test_delete_event(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/events_table_test_data.sql")
    
    # Create an instance of EventRepository
    event_repo = EventRepository(db_connection)
    
    # Ensure event with id 1 exists before deletion
    event_before_deletion = event_repo.find(1)
    assert event_before_deletion is not None
    
    # Delete the event with id 1
    event_repo.delete(1)
    
    # Try to find the deleted event
    deleted_event = event_repo.find(1)
    
    # Assert that the event was deleted (i.e., it should be None)
    assert deleted_event is None
    
    # Optionally, check that the number of events has decreased by one
    all_events = event_repo.find_all()
    expected_event_count = 4  # Adjust this if the number of events was different before deletion
    assert len(all_events) == expected_event_count

def test_find_events_by_band_id(db_connection):
    db_connection.seed("../seeds/events_table_test_data.sql")
    event_repo = EventRepository(db_connection)

    expected_events = [
        Event(
            event_id=2,
            event_name='Jazz Night',
            location='Blue Note, New York',
            event_start=datetime.datetime(2024, 10, 5, 20, 0),
            event_end=datetime.datetime(2024, 10, 5, 23, 59),
            qr_code_content='jazz_night_qr_code_002',
            band_id=3,
            created_at=None,
            updated_at=None
        ),
        Event(
            event_id=5,
            event_name='Autumn Jazz Festival',
            location='Royal Albert Hall, London',
            event_start=datetime.datetime(2024, 11, 10, 17, 0),
            event_end=datetime.datetime(2024, 11, 10, 22, 0),
            qr_code_content='autumn_jazz_festival_qr_code_005',
            band_id=3,
            created_at=None,
            updated_at=None
        ),
    ]

    # Assert no results returns None

    assert event_repo.find_events_by_band_id(7) == None

    expected_result = event_repo.find_events_by_band_id(3)
    assert expected_result == expected_events