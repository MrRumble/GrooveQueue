from datetime import datetime

class Request:
    def __init__(self, request_id=None, song_name=None, guest_id=None,
                 event_id=None, created_at=None, updated_at=None):
        self.request_id = request_id
        self.song_name = song_name
        self.guest_id = guest_id
        self.event_id = event_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False
        return (self.request_id == other.request_id and
                self.song_name == other.song_name and
                self.guest_id == other.guest_id and
                self.event_id == other.event_id)

    def __repr__(self):
        return (f"Request(request_id={self.request_id}, song_name={self.song_name}, "
                f"guest_id={self.guest_id}, event_id={self.event_id}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})")

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "song_name": self.song_name,
            "guest_id": self.guest_id,
            "event_id": self.event_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }