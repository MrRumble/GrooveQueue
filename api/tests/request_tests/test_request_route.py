def strip_timestamps(data):
    """Helper function to remove or normalize timestamp fields from data."""
    for entry in data:
        entry.pop('created_at', None)
        entry.pop('updated_at', None)
    return data

def seed_database(db_connection):
    """Function to seed the database before each test."""
    db_connection.seed("../seeds/events_table_test_data.sql")
    db_connection.seed("../seeds/guests_table_test_data.sql")
    db_connection.seed("../seeds/requests_table_test_data.sql")

def test_get_request_by_request_id(db_connection, web_client):
    seed_database(db_connection)
    response = web_client.get('/requests/1')
    assert response.status_code == 200

    response_json = response.get_json()
    expected_data = {
        "request_id": 1,
        "song_name": "Let It Be",
        "event_id": 1,
        "guest_id": 1,             
        "created_at": "PLACEHOLDER",
        "updated_at": "PLACEHOLDER"
    }   

    stripped_actual = strip_timestamps([response_json])[0]
    stripped_expected = strip_timestamps([expected_data])[0]
    assert stripped_actual == stripped_expected

def test_get_request_by_request_id_not_found(db_connection, web_client):
    seed_database(db_connection)
    response = web_client.get('/requests/99')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Request not found"}

def test_post_request_valid_entry(db_connection, web_client):
    seed_database(db_connection)
    new_request = {
        "song_name": "Imagine",
        "guest_id": 5,
        "event_id": 5,
    }

    response = web_client.post('/requests', json=new_request)
    assert response.status_code == 201
    assert "request_id" in response.get_json()

def test_post_request_missing_field(db_connection, web_client):
    seed_database(db_connection)

    new_request = {
        "guest_id": 5,
        "event_id": 5,
    }
    response = web_client.post('/requests', json=new_request)
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing required fields"}

def test_post_request_invalid_entry(db_connection, web_client):
    seed_database(db_connection)

    new_request = {
        "song_name": "  ",
        "guest_id": 5,
        "event_id": 5,
    }
    response = web_client.post('/requests', json=new_request)
    assert response.status_code == 400
    assert response.get_json() == {"error": "Song name cannot be empty"}

def test_put_request_successful_update(db_connection, web_client):
    seed_database(db_connection)
    
    updated_data = {
        "song_name": "Hey Jude",
        "guest_id": 2,
        "event_id": 2
    }

    response = web_client.put('/requests/1', json=updated_data)
    assert response.status_code == 200
    assert response.get_json() == {"message": "Request updated successfully"}

    # Verify the update was applied correctly
    response = web_client.get('/requests/1')
    response_json = response.get_json()
    expected_data = {
        "request_id": 1,
        "song_name": "Hey Jude",
        "event_id": 2,
        "guest_id": 2,
        "created_at": "PLACEHOLDER",
        "updated_at": "PLACEHOLDER"
    }

    stripped_actual = strip_timestamps([response_json])[0]
    stripped_expected = strip_timestamps([expected_data])[0]
    assert stripped_actual == stripped_expected


def test_put_request_invalid_data(db_connection, web_client):
    seed_database(db_connection)
    
    updated_data = {
        "song_name": "  ", 
        "guest_id": 2,
        "event_id": 2
    }

    response = web_client.put('/requests/1', json=updated_data)
    assert response.status_code == 400
    assert response.get_json() == {"error": "Song name cannot be empty"}

def test_put_request_not_found(db_connection, web_client):
    seed_database(db_connection)
    
    updated_data = {
        "song_name": "New Song",
        "guest_id": 2,
        "event_id": 2
    }

    response = web_client.put('/requests/99', json=updated_data)
    assert response.status_code == 404
    assert response.get_json() == {"error": "Request not found"}

def test_get_requests_by_event_id_success(db_connection, web_client):
    seed_database(db_connection)
    
    # Test for event_id that should have requests
    response = web_client.get('/requests/event/1')
    assert response.status_code == 200
    
    response_json = response.get_json()
    expected_data = [
        {
            "request_id": 1,
            "song_name": "Let It Be",
            "guest_id": 1,
            "event_id": 1,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "request_id": 2,
            "song_name": "Rolling in the Deep",
            "guest_id": 2,
            "event_id": 1,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        }
    ]
    
    stripped_actual = strip_timestamps(response_json)
    stripped_expected = strip_timestamps(expected_data)
    assert stripped_actual == stripped_expected

def test_get_requests_by_event_id_no_requests(db_connection, web_client):
    seed_database(db_connection)
    
    # Test for an event_id that has no requests
    response = web_client.get('/requests/event/99')
    assert response.status_code == 404
    assert response.get_json() == {"error": "No requests found for this event"}





