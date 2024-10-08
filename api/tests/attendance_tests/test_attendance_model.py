from datetime import datetime
from api.attendances.attendance_model import Attendance  # Adjust the import based on the actual path

def test_initialisation():
    # Test initialization with no arguments
    attendance = Attendance()
    assert attendance.attendance_id is None
    assert attendance.guest_id is None
    assert attendance.event_id is None
    assert attendance.status is None
    assert isinstance(attendance.created_at, datetime)
    assert isinstance(attendance.updated_at, datetime)
    print("test_initialisation passed")

def test_initialisation_with_values():
    # Test initialization with arguments
    attendance = Attendance(
        attendance_id=1,
        guest_id=101,
        event_id=202,
        status='accepted',
        created_at=datetime(2023, 1, 1),
        updated_at=datetime(2023, 1, 2)
    )

    assert attendance.attendance_id == 1
    assert attendance.guest_id == 101
    assert attendance.event_id == 202
    assert attendance.status == 'accepted'
    assert attendance.created_at == datetime(2023, 1, 1)
    assert attendance.updated_at == datetime(2023, 1, 2)
    print("test_initialisation_with_values passed")

def test_equality():
    # Test equality comparison
    attendance1 = Attendance(
        attendance_id=1,
        guest_id=101,
        event_id=202,
        status='accepted',
        created_at=None,
        updated_at=None
    )
    attendance2 = Attendance(
        attendance_id=1,
        guest_id=101,
        event_id=202,
        status='accepted',
        created_at=None,
        updated_at=None
    )
    attendance3 = Attendance(
        attendance_id=2,
        guest_id=102,
        event_id=203,
        status='declined',
        created_at=None,
        updated_at=None
    )

    assert attendance1 == attendance2
    assert attendance1 != attendance3
    print("test_equality passed")

def test_representation():
    # Test string representation
    attendance = Attendance(
        attendance_id=1,
        guest_id=101,
        event_id=202,
        status='accepted',
        created_at=datetime(2023, 1, 1),
        updated_at=datetime(2023, 1, 2)
    )
    
    expected_repr = ("Attendance(attendance_id=1, guest_id=101, "
                    "event_id=202, status=accepted, "
                    "created_at=2023-01-01 00:00:00, "
                    "updated_at=2023-01-02 00:00:00)")
    
    assert repr(attendance) == expected_repr
    print("test_representation passed")

def test_to_dict():
    # Test dictionary conversion
    attendance = Attendance(
        attendance_id=1,
        guest_id=101,
        event_id=202,
        status='accepted',
        created_at=datetime(2023, 1, 1),
        updated_at=datetime(2023, 1, 2)
    )

    expected_dict = {
        "attendance_id": 1,
        "guest_id": 101,
        "event_id": 202,
        "status": 'accepted',
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-02T00:00:00"
    }
    
    assert attendance.to_dict() == expected_dict
    print("test_to_dict passed")

