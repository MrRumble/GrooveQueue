import datetime
from api.attendances.attendance_model import Attendance  # Adjust import based on actual path

class AttendanceRepository:
    def __init__(self, connection):
        self._connection = connection

    def create_attendance(self, guest_id, event_id, status):
        query = """
            INSERT INTO attendance (guest_id, event_id, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING attendance_id, created_at, updated_at
        """
        params = (
            guest_id,
            event_id,
            status,
            datetime.datetime.now(),
            datetime.datetime.now()
        )
        result = self._connection.execute(query, params)
        attendance = Attendance(
            attendance_id=result[0]['attendance_id'],
            guest_id=guest_id,
            event_id=event_id,
            status=status,
            created_at=result[0]['created_at'],
            updated_at=result[0]['updated_at']
        )
        return attendance

    def get_attendance_by_guest(self, guest_id):
        query = "SELECT * FROM attendance WHERE guest_id = %s"
        rows = self._connection.execute(query, [guest_id])
        return [Attendance(**row) for row in rows]

    def get_attendance_by_event(self, event_id):
        query = "SELECT * FROM attendance WHERE event_id = %s"
        rows = self._connection.execute(query, [event_id])
        return [Attendance(**row) for row in rows]

    def update_attendance(self, attendance_id, status):
        query = """
            UPDATE attendance
            SET status = %s,
                updated_at = %s
            WHERE attendance_id = %s
            RETURNING attendance_id, guest_id, event_id, status, created_at, updated_at
        """
        params = (
            status,
            datetime.datetime.now(),
            attendance_id
        )
        result = self._connection.execute(query, params)
        if not result:
            raise ValueError("Attendance record not found")
        return Attendance(**result[0])

    def delete_attendance(self, attendance_id):
        query = "DELETE FROM attendance WHERE attendance_id = %s"
        self._connection.execute(query, [attendance_id])
        return None
