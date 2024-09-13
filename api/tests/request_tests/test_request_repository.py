from api.requests.request_model import Request
from api.requests.request_repository import RequestRepository


def test_find_request_by_id(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/requests_table_test_data.sql")
    # Create an instance of RequestRepository
    request_repo = RequestRepository(db_connection)
    
    # Find the request with id 1
    result = request_repo.find(1)
    
    # Create the expected Request object
    expected_request = Request(
        request_id=1,
        song_name='Let It Be',
        guest_id=1,
        event_id=1,
        created_at=None,  # Handle timestamp comparison separately
        updated_at=None   # Handle timestamp comparison separately
    )
    
    # Check if the result is not None
    assert result is not None

    # Compare individual attributes, excluding created_at and updated_at
    assert result.request_id == expected_request.request_id
    assert result.song_name == expected_request.song_name
    assert result.guest_id == expected_request.guest_id
    assert result.event_id == expected_request.event_id

    # Optionally, compare timestamps with some tolerance if needed
    if expected_request.created_at:
        assert abs((result.created_at - expected_request.created_at).total_seconds()) < 1
    else:
        assert result.created_at is None

    if expected_request.updated_at:
        assert abs((result.updated_at - expected_request.updated_at).total_seconds()) < 1
    else:
        assert result.updated_at is None

def test_find_all_requests(db_connection):
    # Seed the database with the new test data
    db_connection.seed("../seeds/requests_table_test_data.sql")
    
    # Create an instance of RequestRepository
    request_repo = RequestRepository(db_connection)
    
    # Fetch all requests from the repository
    results = request_repo.find_all()
    
    # Define the expected Request objects based on the seed data
    expected_requests = [
        Request(
            request_id=1,
            song_name='Let It Be',
            guest_id=1,
            event_id=1,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=2,
            song_name='Rolling in the Deep',
            guest_id=2,
            event_id=1,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=3,
            song_name='Shape of You',
            guest_id=3,
            event_id=2,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=4,
            song_name='Bohemian Rhapsody',
            guest_id=4,
            event_id=2,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=5,
            song_name='Blinding Lights',
            guest_id=5,
            event_id=3,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=6,
            song_name='Someone Like You',
            guest_id=6,
            event_id=3,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=7,
            song_name='Uptown Funk',
            guest_id=7,
            event_id=4,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=8,
            song_name='Havana',
            guest_id=8,
            event_id=4,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=9,
            song_name='Despacito',
            guest_id=9,
            event_id=5,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=10,
            song_name='Perfect',
            guest_id=10,
            event_id=5,
            created_at=None,
            updated_at=None
        ),
    ]
    
    # Check if the number of results is as expected
    assert len(results) == len(expected_requests)
    
    # Compare individual attributes of each request
    for result, expected_request in zip(results, expected_requests):
        assert result.request_id == expected_request.request_id
        assert result.song_name == expected_request.song_name
        assert result.guest_id == expected_request.guest_id
        assert result.event_id == expected_request.event_id
        
        # Optionally, compare timestamps with some tolerance
        if expected_request.created_at:
            assert abs((result.created_at - expected_request.created_at).total_seconds()) < 1
        else:
            assert result.created_at is None
        
        if expected_request.updated_at:
            assert abs((result.updated_at - expected_request.updated_at).total_seconds()) < 1
        else:
            assert result.updated_at is None

def test_create_request(db_connection):
    db_connection.seed("../seeds/requests_table_test_data.sql")
    
    # Create an instance of RequestRepository
    request_repo = RequestRepository(db_connection)
    
    # Create a new Request object
    new_request = Request(
        song_name='New Song',
        guest_id=1,
        event_id=2
    )
    
    # Insert the new request into the database
    request_id = request_repo.create(new_request)
    found_request = request_repo.find(request_id)
    
    assert found_request.request_id == request_id
    assert found_request.song_name == "New Song"
    assert found_request.guest_id == 1
    assert found_request.event_id == 2

def test_update_request(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/requests_table_test_data.sql")
    
    # Create an instance of RequestRepository
    request_repo = RequestRepository(db_connection)
    
    # Find an existing request to update
    request_to_update = request_repo.find(1)
    
    # Modify the request's details
    request_to_update.song_name = "Updated Song"
    request_to_update.guest_id = 2
    request_to_update.event_id = 3
    
    # Perform the update operation
    request_repo.update(request_to_update.request_id, request_to_update)
    
    # Fetch the updated request from the database
    updated_request = request_repo.find(request_to_update.request_id)
    
    # Assert the updated fields
    assert updated_request.song_name == "Updated Song"
    assert updated_request.guest_id == 2
    assert updated_request.event_id == 3
    
    # Check that the IDs match
    assert updated_request.request_id == request_to_update.request_id

def test_delete_request(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/requests_table_test_data.sql")
    
    # Create an instance of RequestRepository
    request_repo = RequestRepository(db_connection)
    
    # Ensure request with id 1 exists before deletion
    request_before_deletion = request_repo.find(1)
    assert request_before_deletion is not None
    
    # Delete the request with id 1
    request_repo.delete(1)
    
    # Try to find the deleted request
    deleted_request = request_repo.find(1)
    
    # Assert that the request was deleted (i.e., it should be None)
    assert deleted_request is None
    
    # Optionally, check that the number of requests has decreased by one
    all_requests = request_repo.find_all()
    expected_request_count = 9  # Adjust this if the number of requests was different before deletion
    assert len(all_requests) == expected_request_count

def test_find_requests_by_event_id(db_connection):
    db_connection.seed("../seeds/requests_table_test_data.sql")
    request_repo = RequestRepository(db_connection)

    expected_requests_event_2 = [
        Request(
            request_id=3,
            song_name='Shape of You',
            guest_id=3,
            event_id=2,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=4,
            song_name='Bohemian Rhapsody',
            guest_id=4,
            event_id=2,
            created_at=None,
            updated_at=None
        ),
    ]

    expected_requests_event_4 = [
        Request(
            request_id=7,
            song_name='Uptown Funk',
            guest_id=7,
            event_id=4,
            created_at=None,
            updated_at=None
        ),
        Request(
            request_id=8,
            song_name='Havana',
            guest_id=8,
            event_id=4,
            created_at=None,
            updated_at=None
        ),
    ]

    # Assert no results returns None
    assert request_repo.find_requests_by_event_id(10) == None

    # Test finding requests for event_id 2
    result_event_2 = request_repo.find_requests_by_event_id(2)
    assert result_event_2 == expected_requests_event_2

    # Test finding requests for event_id 4
    result_event_4 = request_repo.find_requests_by_event_id(4)
    assert result_event_4 == expected_requests_event_4
