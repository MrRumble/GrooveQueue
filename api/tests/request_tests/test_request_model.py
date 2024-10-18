from datetime import datetime
from api.requests.request_model import Request  

def test_initialization():
    # Test initialization with no arguments
    request = Request()
    assert request.request_id is None
    assert request.track_id is None  # Updated from song_name to track_id
    assert request.guest_id is None
    assert request.event_id is None
    assert isinstance(request.created_at, datetime)
    assert isinstance(request.updated_at, datetime)
    print("test_initialization passed")

def test_initialization_with_values():
    # Test initialization with arguments
    request = Request(request_id=1, track_id="12345", guest_id=1,  # Updated to track_id
                      event_id=1, created_at=datetime(2023, 8, 1),
                      updated_at=datetime(2023, 8, 2))

    assert request.request_id == 1
    assert request.track_id == "12345"  # Updated to track_id
    assert request.guest_id == 1
    assert request.event_id == 1
    assert request.created_at == datetime(2023, 8, 1)
    assert request.updated_at == datetime(2023, 8, 2)

def test_equality():
    # Test equality comparison
    request1 = Request(request_id=1, track_id="12345", guest_id=1, event_id=1)  # Updated to track_id
    request2 = Request(request_id=1, track_id="12345", guest_id=1, event_id=1)  # Updated to track_id
    request3 = Request(request_id=2, track_id="67890", guest_id=2, event_id=2)  # Updated to track_id

    assert request1 == request2
    assert request1 != request3

def test_representation():
    # Test string representation
    request = Request(request_id=1, track_id="12345", guest_id=1, event_id=1,  # Updated to track_id
                      created_at=datetime(2023, 8, 1), updated_at=datetime(2023, 8, 2))

    expected_repr = ("Request(request_id=1, track_id=12345, guest_id=1, event_id=1, "  # Updated to track_id
                     "created_at=2023-08-01 00:00:00, updated_at=2023-08-02 00:00:00)")
    
    assert repr(request) == expected_repr

def test_to_dict():
    # Test conversion to dictionary
    request = Request(request_id=1, track_id="12345", guest_id=1, event_id=1,  # Updated to track_id
                      created_at=datetime(2023, 8, 1), updated_at=datetime(2023, 8, 2))

    request_dict = request.to_dict()
    expected_dict = {
        "request_id": 1,
        "track_id": "12345",  # Updated to track_id
        "guest_id": 1,
        "event_id": 1,
        "created_at": "2023-08-01T00:00:00",
        "updated_at": "2023-08-02T00:00:00"
    }

    assert request_dict == expected_dict

