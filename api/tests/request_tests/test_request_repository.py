import pytest
from api.requests.request_model import Request
from api.requests.request_repository import RequestRepository

def test_find_request_by_id(db_connection):
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    db_connection.seed("../seeds/requests_table_test_data.sql")
    request_repo = RequestRepository(db_connection)
    
    # Find the request with id 1
    result = request_repo.find(1)
    
    assert result is not None
    assert result.track_id == '12345'  # Let It Be
    assert result.guest_id == 1
    assert result.event_id == 1

def test_find_all_requests(db_connection):
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    db_connection.seed("../seeds/requests_table_test_data.sql")
    request_repo = RequestRepository(db_connection)
    
    results = request_repo.find_all()
    
    assert len(results) == 5  # We inserted 5 requests
    assert results[0].track_id == '12345'
    assert results[1].track_id == '67890'
    assert results[2].track_id == '13579'
    assert results[3].track_id == '24680'
    assert results[4].track_id == '11121'

def test_create_request(db_connection):
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    db_connection.seed("../seeds/requests_table_test_data.sql")
    request_repo = RequestRepository(db_connection)
    
    # Create a new Request object
    new_request = Request(
        track_id='12345',  # This track_id must exist in tracks table
        guest_id=1,
        event_id=2
    )
    
    # Insert the new request into the database
    request_id = request_repo.create(new_request)
    found_request = request_repo.find(request_id)
    
    assert found_request.request_id == request_id
    assert found_request.track_id == '12345'
    assert found_request.guest_id == 1
    assert found_request.event_id == 2

def test_delete_request(db_connection):
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    db_connection.seed("../seeds/requests_table_test_data.sql")
    request_repo = RequestRepository(db_connection)
    
    # Ensure request with id 1 exists before deletion
    request_before_deletion = request_repo.find(1)
    assert request_before_deletion is not None
    
    # Delete the request with id 1
    request_repo.delete(1)
    
    # Try to find the deleted request
    deleted_request = request_repo.find(1)
    assert deleted_request is None

def test_find_requests_by_event_id(db_connection):
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    db_connection.seed("../seeds/requests_table_test_data.sql")
    request_repo = RequestRepository(db_connection)

    # Test finding requests for event_id 2
    results_event_2 = request_repo.find_requests_by_event_id(2)
    assert len(results_event_2) == 2  # We expect two requests for event_id 2
    assert results_event_2[0].track_id == '13579'  # Shape of You
    assert results_event_2[1].track_id == '24680'  # Bohemian Rhapsody

    # Test finding requests for a non-existent event
    results_event_non_existent = request_repo.find_requests_by_event_id(9999)
    assert results_event_non_existent is None

def test_requests_by_guest(db_connection):
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    db_connection.seed("../seeds/requests_table_test_data.sql")
    request_repo = RequestRepository(db_connection)

    # Test guest 1 for event 1 (should return 1 request)
    guest_1_event_1_count = request_repo.requests_by_guest(1, 1)
    assert guest_1_event_1_count == 1  # In the seed data, guest 1 has made 1 request for event 1
    
    # Test guest 2 for event 1 (should return 1 request)
    guest_2_event_1_count = request_repo.requests_by_guest(2, 1)
    assert guest_2_event_1_count == 1  # Guest 2 made 1 request for event 1
    
    # Test guest 3 for event 2 (should return 1 request)
    guest_3_event_2_count = request_repo.requests_by_guest(3, 2)
    assert guest_3_event_2_count == 1  # Guest 3 made 1 request for event 2

    # Test guest 1 for event 2 (should return 0 requests)
    guest_1_event_2_count = request_repo.requests_by_guest(1, 2)
    assert guest_1_event_2_count == 0  # Guest 1 made no requests for event 2

    # Test guest 11 for event 1 (should return 0 requests)
    guest_11_no_requests = request_repo.requests_by_guest(11, 1)
    assert guest_11_no_requests == 0  # Guest 11 made no requests

    # Test a guest for an event that doesn't exist (should return 0 requests)
    guest_1_event_non_existent = request_repo.requests_by_guest(1, 9999)
    assert guest_1_event_non_existent == 0  # Event 9999 doesn't exist, so no requests
