import pytest

def strip_timestamps(data):
    """Helper function to remove or normalize timestamp fields from data."""
    for entry in data:
        entry.pop('created_at', None)
        entry.pop('updated_at', None)
    return data

def test_get_all_events(db_connection, web_client):
    db_connection.seed("../seeds/events_table_test_data.sql")
    response = web_client.get('/events')
    assert response.status_code == 200

    response_json = response.get_json()

    # Define expected data with placeholders for timestamps
    expected_data = [
        {
            "event_id": 1,
            "event_name": "Rocking the City",
            "location": "Madison Square Garden, New York",
            "event_start": "2024-09-15T19:00:00",
            "event_end": "2024-09-15T23:00:00",
            "qr_code_content": "rocking_the_city_qr_code_001",
            "band_id": 1,
            "max_requests_per_user": 10,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "event_id": 2,
            "event_name": "Jazz Night",
            "location": "Blue Note, New York",
            "event_start": "2024-10-05T20:00:00",
            "event_end": "2024-10-05T23:59:00",
            "qr_code_content": "jazz_night_qr_code_002",
            "band_id": 3,
            "max_requests_per_user": 5,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "event_id": 3,
            "event_name": "The Big Apple Concert",
            "location": "Central Park, New York",
            "event_start": "2024-10-20T18:00:00",
            "event_end": "2024-10-20T22:00:00",
            "qr_code_content": "big_apple_concert_qr_code_003",
            "band_id": 2,
            "max_requests_per_user": 7,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "event_id": 4,
            "event_name": "Summer Festival",
            "location": "Hyde Park, London",
            "event_start": "2024-08-25T12:00:00",
            "event_end": "2024-08-25T22:00:00",
            "qr_code_content": "summer_festival_qr_code_004",
            "band_id": 1,
            "max_requests_per_user": 15,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "event_id": 5,
            "event_name": "Autumn Jazz Festival",
            "location": "Royal Albert Hall, London",
            "event_start": "2024-11-10T17:00:00",
            "event_end": "2024-11-10T22:00:00",
            "qr_code_content": "autumn_jazz_festival_qr_code_005",
            "band_id": 3,
            "max_requests_per_user": 3,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        }
    ]

    # Strip timestamps from actual data for comparison
    stripped_actual = strip_timestamps(response_json.copy())
    stripped_expected = strip_timestamps(expected_data.copy())

    # Perform assertion
    assert stripped_actual == stripped_expected

def test_get_event_by_id(db_connection, web_client):
    db_connection.seed("../seeds/events_table_test_data.sql")
    response = web_client.get('/events/1')
    assert response.status_code == 200

    response_json = response.get_json()
    expected_data = {
        "event_id": 1,
        "band_name": "White Noise",
        "event_name": "Rocking the City",
        "location": "Madison Square Garden, New York",
        "event_start": "2024-09-15T19:00:00",
        "event_end": "2024-09-15T23:00:00",
        "qr_code_content": "rocking_the_city_qr_code_001",
        "band_id": 1,
        "max_requests_per_user": 10,
        "created_at": "PLACEHOLDER",
        "updated_at": "PLACEHOLDER"
    }


    stripped_actual = strip_timestamps([response_json])[0]
    stripped_expected = strip_timestamps([expected_data])[0]
    assert stripped_actual == stripped_expected

def test_get_event_not_found(db_connection, web_client):
    db_connection.seed("../seeds/events_table_test_data.sql")
    response = web_client.get('/events/999')  # Assuming 999 is not in the test data
    assert response.status_code == 404

    response_json = response.get_json()
    assert response_json == {"error": "Event not found"}

def test_create_event(db_connection, web_client):
    db_connection.seed("../seeds/events_table_test_data.sql")
    new_event = {
        "event_name": "New Event",
        "location": "New Location",
        "event_start": "2024-12-01T10:00:00",
        "event_end": "2024-12-01T12:00:00",
        "qr_code_content": "new_event_qr_code",
        "band_id": 1
    }
    response = web_client.post('/events', json=new_event)
    assert response.status_code == 201

    response_json = response.get_json()
    assert "event_id" in response_json

    # Verify that the event was actually created
    response = web_client.get(f"/events/{response_json['event_id']}")
    assert response.status_code == 200
    created_event = response.get_json()
    assert created_event['event_name'] == new_event['event_name']

def test_update_event(db_connection, web_client):
    db_connection.seed("../seeds/events_table_test_data.sql")
    updated_event = {
        "event_name": "Updated Event",
        "location": "Updated Location",
        "event_start": "2024-12-01T14:00:00",
        "event_end": "2024-12-01T16:00:00",
        "qr_code_content": "updated_event_qr_code",
        "band_id": 2
    }
    response = web_client.put('/events/1', json=updated_event)
    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json == {"message": "Event updated successfully"}

    # Verify that the event was actually updated
    response = web_client.get('/events/1')
    assert response.status_code == 200
    updated_event_response = response.get_json()
    assert updated_event_response['event_name'] == updated_event['event_name']

def test_delete_event(db_connection, web_client):
    db_connection.seed("../seeds/events_table_test_data.sql")
    response = web_client.delete('/events/1')
    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json == {"message": "Event deleted successfully"}

    # Verify that the event was actually deleted
    response = web_client.get('/events/1')
    assert response.status_code == 404
    response_json = response.get_json()
    assert response_json == {"error": "Event not found"}

def test_get_events_by_band_id(db_connection, web_client):
    # Seed the database with test data
    db_connection.seed("../seeds/events_table_test_data.sql")
    
    # Make a GET request to the endpoint
    response = web_client.get('/bands/1/events')
    
    # Assert the status code is 200 (OK)
    assert response.status_code == 200

    # Get the JSON response
    response_json = response.get_json()
    
    # Define the expected output structure
    expected_data = {
        "band_name": "White Noise",  # Replace with the actual band name from your test data
        "events": [
            {
                "event_id": 1,
                "event_name": "Rocking the City",
                "location": "Madison Square Garden, New York",
                "event_start": "2024-09-15T19:00:00",
                "event_end": "2024-09-15T23:00:00",
                "qr_code_content": "rocking_the_city_qr_code_001",
                "band_id": 1,
                "max_requests_per_user": 10,
                "created_at": "PLACEHOLDER",  # Adjust this as necessary
                "updated_at": "PLACEHOLDER"   # Adjust this as necessary
            },
            {
                "event_id": 4,
                "event_name": "Summer Festival",
                "location": "Hyde Park, London",
                "event_start": "2024-08-25T12:00:00",
                "event_end": "2024-08-25T22:00:00",
                "qr_code_content": "summer_festival_qr_code_004",
                "band_id": 1,
                "max_requests_per_user": 15,
                "created_at": "PLACEHOLDER",  # Adjust this as necessary
                "updated_at": "PLACEHOLDER"   # Adjust this as necessary
            }
        ]
    }

    # Strip timestamps from the actual response
    stripped_actual = {
        "band_name": response_json["band_name"],
        "events": strip_timestamps(response_json["events"])
    }
    
    # Prepare the expected data by stripping timestamps
    stripped_expected = {
        "band_name": expected_data["band_name"],
        "events": strip_timestamps(expected_data["events"])
    }

    # Assert that the stripped actual response matches the stripped expected response
    assert stripped_actual == stripped_expected

def test_get_events_by_non_existent_band_id(db_connection, web_client):
    db_connection.seed("../seeds/events_table_test_data.sql")
    
    # Test for a band ID that does not exist
    response = web_client.get('/bands/999/events')  # Assuming 999 does not exist
    assert response.status_code == 404
    response_json = response.get_json()
    assert response_json == {"error": "Band not found"}

def test_get_events_by_existing_band_id_no_events(db_connection, web_client):
    db_connection.seed("../seeds/events_table_test_data.sql")
    
    # Test for a band ID that exists but has no events
    response = web_client.get('/bands/4/events')  # Assuming band 1 exists but has no events
    assert response.status_code == 404
    response_json = response.get_json()
    assert response_json == {"error": "No events found for this band"}

