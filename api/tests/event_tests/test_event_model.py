from api.events.event_model import Event  # Assuming the Event model is in this module
from datetime import datetime

def test_initialisation():
    # Test initialisation with no arguments
    event = Event()
    assert event.event_id is None
    assert event.event_name is None
    assert event.location is None
    assert isinstance(event.event_start, datetime)
    assert isinstance(event.event_end, datetime)
    assert event.qr_code_content is None
    assert event.band_id is None
    assert isinstance(event.created_at, datetime)
    assert isinstance(event.updated_at, datetime)
    print("test_initialization passed")

def test_initialisation_with_values():
    # Test initialisation with arguments
    event = Event(event_id=1, event_name="Jazz Festival", location="Central Park",
                  event_start=datetime(2023, 9, 10, 15, 0, 0), 
                  event_end=datetime(2023, 9, 10, 18, 0, 0),
                  qr_code_content="some_qr_code_data", band_id=2,
                  created_at=datetime(2023, 8, 1),
                  updated_at=datetime(2023, 8, 2))

    assert event.event_id == 1
    assert event.event_name == "Jazz Festival"
    assert event.location == "Central Park"
    assert event.event_start == datetime(2023, 9, 10, 15, 0, 0)
    assert event.event_end == datetime(2023, 9, 10, 18, 0, 0)
    assert event.qr_code_content == "some_qr_code_data"
    assert event.band_id == 2
    assert event.created_at == datetime(2023, 8, 1)
    assert event.updated_at == datetime(2023, 8, 2)

def test_equality():
    # Test equality comparison
    event1 = Event(event_id=1, event_name="Jazz Festival", location="Central Park")
    event2 = Event(event_id=1, event_name="Jazz Festival", location="Central Park")
    event3 = Event(event_id=2, event_name="Rock Concert", location="Madison Square Garden")

    assert event1 == event2
    assert event1 != event3

def test_representation():
    # Test string representation
    event = Event(event_id=1, event_name="Jazz Festival", location="Central Park",
                  event_start=datetime(2023, 9, 10, 15, 0, 0), 
                  event_end=datetime(2023, 9, 10, 18, 0, 0),
                  qr_code_content="some_qr_code_data", band_id=2,
                  created_at=datetime(2023, 8, 1),
                  updated_at=datetime(2023, 8, 2))
    
    expected_repr = ("Event(event_id=1, event_name=Jazz Festival, location=Central Park, "
                     "event_start=2023-09-10 15:00:00, event_end=2023-09-10 18:00:00, "
                     "qr_code_content=some_qr_code_data, band_id=2, "
                     "created_at=2023-08-01 00:00:00, "
                     "updated_at=2023-08-02 00:00:00)")
    
    assert repr(event) == expected_repr

def test_to_dict():
    # Test conversion to dictionary
    event = Event(event_id=1, event_name="Jazz Festival", location="Central Park",
                  event_start=datetime(2023, 9, 10, 15, 0, 0), 
                  event_end=datetime(2023, 9, 10, 18, 0, 0),
                  qr_code_content="some_qr_code_data", band_id=2,
                  created_at=datetime(2023, 8, 1),
                  updated_at=datetime(2023, 8, 2))

    event_dict = event.to_dict()
    expected_dict = {
        "event_id": 1,
        "event_name": "Jazz Festival",
        "location": "Central Park",
        "event_start": "2023-09-10T15:00:00",
        "event_end": "2023-09-10T18:00:00",
        "qr_code_content": "some_qr_code_data",
        "band_id": 2,
        "created_at": "2023-08-01T00:00:00",
        "updated_at": "2023-08-02T00:00:00"
    }

    assert event_dict == expected_dict
