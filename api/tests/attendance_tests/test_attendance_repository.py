from api.attendances.attendance_model import Attendance
from api.attendances.attendance_repository import AttendanceRepository

def seed_database(db_connection):
    """Helper function to seed the database with necessary test data."""
    # Seed guests  
    db_connection.seed("../seeds/guests_table_test_data.sql")
    
    # Seed events
    db_connection.seed("../seeds/events_table_test_data.sql")
    
    # Seed attendance
    db_connection.seed("../seeds/attendances_table_test_data.sql")

def test_create_attendance(db_connection):
    # Seed the database
    seed_database(db_connection)

    # Create an instance of AttendanceRepository
    attendance_repo = AttendanceRepository(db_connection)

    # Create a new attendance record
    new_attendance = attendance_repo.create_attendance(1, 1, 'accepted')

    # Fetch the newly created attendance from the database
    found_attendance = attendance_repo.get_attendance_by_guest(1)[-1]  # Assuming guest_id 1 has this attendance
    assert found_attendance.attendance_id == new_attendance.attendance_id
    assert found_attendance.guest_id == 1
    assert found_attendance.event_id == 1
    assert found_attendance.status == 'accepted'

def test_get_attendance_by_guest(db_connection):
    # Seed the database
    seed_database(db_connection)

    # Create an instance of AttendanceRepository
    attendance_repo = AttendanceRepository(db_connection)

    # Get attendance records for guest_id 1
    attendances = attendance_repo.get_attendance_by_guest(1)

    expected_attendances = [
        Attendance(attendance_id=1, guest_id=1, event_id=1, status='accepted', created_at=None, updated_at=None),
        Attendance(attendance_id=10, guest_id=1, event_id=2, status='declined', created_at=None, updated_at=None),
    ]

    # Check if the number of results is as expected
    assert len(attendances) == len(expected_attendances)

    # Compare individual attributes
    for result, expected in zip(attendances, expected_attendances):
        assert result.attendance_id == expected.attendance_id
        assert result.guest_id == expected.guest_id
        assert result.event_id == expected.event_id
        assert result.status == expected.status

def test_get_attendance_by_event(db_connection):
    # Seed the database
    seed_database(db_connection)

    # Create an instance of AttendanceRepository
    attendance_repo = AttendanceRepository(db_connection)

    # Get attendance records for event_id 1
    attendances = attendance_repo.get_attendance_by_event(1)

    expected_attendances = [
        Attendance(attendance_id=1, guest_id=1, event_id=1, status='accepted', created_at=None, updated_at=None),
        Attendance(attendance_id=2, guest_id=2, event_id=1, status='declined', created_at=None, updated_at=None),
        Attendance(attendance_id=7, guest_id=7, event_id=1, status='accepted', created_at=None, updated_at=None)
    ]

    # Check if the number of results is as expected
    assert len(attendances) == len(expected_attendances)

    # Compare individual attributes
    for result, expected in zip(attendances, expected_attendances):
        assert result.attendance_id == expected.attendance_id
        assert result.guest_id == expected.guest_id
        assert result.event_id == expected.event_id
        assert result.status == expected.status

def test_update_attendance(db_connection):
    # Seed the database
    seed_database(db_connection)

    # Create an instance of AttendanceRepository
    attendance_repo = AttendanceRepository(db_connection)

    # Fetch an existing attendance to update
    attendances = attendance_repo.get_attendance_by_guest(1)
    
    # Assuming guest_id 1 has at least one attendance
    attendance_to_update = attendances[0]
    
    print("Before update:", attendance_to_update)

    # Modify the attendance's status
    attendance_repo.update_attendance(attendance_to_update.attendance_id, 'declined')

    # Fetch the updated attendance from the database
    updated_attendances = attendance_repo.get_attendance_by_guest(1)
    
    # Print the updated attendance for debugging
    print("Updated attendances:", updated_attendances)
    
    # Find the updated attendance entry (if multiple)
    updated_attendance = next((att for att in updated_attendances if att.attendance_id == attendance_to_update.attendance_id), None)

    # Assert that we found the updated record and check the status
    assert updated_attendance is not None, "Updated attendance not found!"
    assert updated_attendance.attendance_id == attendance_to_update.attendance_id
    assert updated_attendance.status == 'declined'


def test_delete_attendance(db_connection):
    # Seed the database
    seed_database(db_connection)

    # Create an instance of AttendanceRepository
    attendance_repo = AttendanceRepository(db_connection)

    # Ensure attendance with id 1 exists before deletion
    attendance_before_deletion = attendance_repo.get_attendance_by_guest(1)[0]
    assert attendance_before_deletion is not None

    # Delete the attendance with id 1
    attendance_repo.delete_attendance(attendance_before_deletion.attendance_id)

    # Try to find the deleted attendance
    attendances_after_deletion = attendance_repo.get_attendance_by_guest(1)
    assert len(attendances_after_deletion) == 1  # Should be only one attendance left for guest_id 1

def test_attendance_exists(db_connection):
    # Seed the database
    seed_database(db_connection)

    # Create an instance of AttendanceRepository
    attendance_repo = AttendanceRepository(db_connection)
 
    result = attendance_repo.get_attendance_by_guest(1)  # Get attendance for guest_id 1
    assert len(result) == 2  # Assume we know guest_id 1 has 2 attendances in the seeded data

    false_result = attendance_repo.get_attendance_by_guest(999)  # Non-existent guest_id
    assert len(false_result) == 0  # Should return an empty list
