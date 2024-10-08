import datetime

class Attendance:
    def __init__(self, attendance_id=None, guest_id=None, event_id=None,
                status=None, created_at=None, updated_at=None):
        self.attendance_id = attendance_id
        self.guest_id = guest_id
        self.event_id = event_id
        self.status = status
        self.created_at = created_at or datetime.datetime.now()
        self.updated_at = updated_at or datetime.datetime.now()

    def __eq__(self, other):
        if not isinstance(other, Attendance):
            return False
        return (self.attendance_id == other.attendance_id and
                self.guest_id == other.guest_id and
                self.event_id == other.event_id and
                self.status == other.status)
    
    
    def __repr__(self):
        return (f"Attendance(attendance_id={self.attendance_id}, guest_id={self.guest_id}, "
                f"event_id={self.event_id}, status={self.status}, "
                f"created_at={self.created_at}, "
                f"updated_at={self.updated_at})")

    def to_dict(self):
        return {
            "attendance_id": self.attendance_id,
            "guest_id": self.guest_id,
            "event_id": self.event_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),  # Convert to ISO format
            "updated_at": self.updated_at.isoformat()   # Convert to ISO format
        }
