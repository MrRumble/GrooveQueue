from datetime import datetime

class Event:
    def __init__(self, event_id=None, event_name=None, location=None,
                event_start=None, event_end=None, qr_code_content=None,
                band_id=None, created_at=None, updated_at=None):
        self.event_id = event_id
        self.event_name = event_name
        self.location = location
        self.event_start = event_start or datetime.now()
        self.event_end = event_end or datetime.now()
        self.qr_code_content = qr_code_content
        self.band_id = band_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return (self.event_id == other.event_id and
                self.event_name == other.event_name and
                self.location == other.location)

    def __repr__(self):
        return (f"Event(event_id={self.event_id}, event_name={self.event_name}, "
                f"location={self.location}, event_start={self.event_start}, "
                f"event_end={self.event_end}, qr_code_content={self.qr_code_content}, "
                f"band_id={self.band_id}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})")

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "location": self.location,
            "event_start": self.event_start.isoformat(),
            "event_end": self.event_end.isoformat(),
            "qr_code_content": self.qr_code_content,
            "band_id": self.band_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
