import datetime

class Notification:
    def __init__(self, notification_id=None, recipient_id=None, recipient_type=None,
                 event_id=None, notification_type=None, message=None,
                 is_read=False, created_at=None, updated_at=None):
        self.notification_id = notification_id
        self.recipient_id = recipient_id  # Guest or Band ID
        self.recipient_type = recipient_type  # 'guest' or 'band'
        self.event_id = event_id  # Reference to the event
        self.notification_type = notification_type  # Type of notification
        self.message = message  # Content of the notification
        self.is_read = is_read  # Whether the notification has been read
        self.created_at = created_at or datetime.datetime.now()
        self.updated_at = updated_at or datetime.datetime.now()

    def __eq__(self, other):
        if not isinstance(other, Notification):
            return False
        return (self.notification_id == other.notification_id and
                self.recipient_id == other.recipient_id and
                self.recipient_type == other.recipient_type and
                self.event_id == other.event_id and
                self.notification_type == other.notification_type and
                self.message == other.message and
                self.is_read == other.is_read)

    def __repr__(self):
        return (f"Notification(id={self.notification_id}, recipient_id={self.recipient_id}, "
                f"recipient_type={self.recipient_type}, event_id={self.event_id}, "
                f"type={self.notification_type}, is_read={self.is_read}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})")

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "recipient_id": self.recipient_id,
            "recipient_type": self.recipient_type,
            "event_id": self.event_id,
            "notification_type": self.notification_type,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat(),  # Convert to ISO format
            "updated_at": self.updated_at.isoformat()   # Convert to ISO format
        }
