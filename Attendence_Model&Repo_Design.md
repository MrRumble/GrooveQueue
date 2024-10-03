# Attendance Model and Repository Design

## Attendance Model

The `Attendance` model represents the relationship between guests and events, indicating whether a guest is attending a specific event. This model will help track attendance status and any associated details.

### Table: attendance
- **attendance_id**: SERIAL PRIMARY KEY
- **guest_id**: INTEGER NOT NULL REFERENCES guests(id) -- The ID of the guest
- **event_id**: INTEGER NOT NULL REFERENCES events(event_id) -- The ID of the event
- **status**: VARCHAR(50) NOT NULL -- The attendance status (e.g., 'accepted', 'declined', 'pending')
- **created_at**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- When the attendance was recorded
- **updated_at**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- When the attendance record was last updated

## Attendance Repository

The `AttendanceRepository` will handle all database operations related to attendance records. It will provide methods to create, read, update, and delete attendance records.

### Class: AttendanceRepository

#### Methods:
- **__init__(self, connection)**: Initializes the repository with a database connection.
- **create_attendance(self, guest_id, event_id, status)**: Creates a new attendance record.
- **get_attendance_by_guest(self, guest_id)**: Retrieves all attendance records for a specific guest.
- **get_attendance_by_event(self, event_id)**: Retrieves all attendance records for a specific event.
- **update_attendance(self, attendance_id, status)**: Updates the attendance status for a specific record.
- **delete_attendance(self, attendance_id)**: Deletes a specific attendance record.


