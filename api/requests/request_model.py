from datetime import datetime

class Request:
    def __init__(self, request_id=None, track_id=None, guest_id=None,
                 event_id=None, created_at=None, updated_at=None):
        self.request_id = request_id
        self.track_id = track_id  # Changed from song_name to track_id
        self.guest_id = guest_id
        self.event_id = event_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False
        return (self.request_id == other.request_id and
                self.track_id == other.track_id and  # Updated for track_id
                self.guest_id == other.guest_id and
                self.event_id == other.event_id)

    def __repr__(self):
        return (f"Request(request_id={self.request_id}, track_id={self.track_id}, "
                f"guest_id={self.guest_id}, event_id={self.event_id}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})")

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "track_id": self.track_id,  # Updated for track_id
            "guest_id": self.guest_id,
            "event_id": self.event_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
