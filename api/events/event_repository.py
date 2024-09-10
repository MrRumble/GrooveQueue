from api.events.event_model import Event
from datetime import datetime

class EventRepository():
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        query = "SELECT * FROM events"
        rows = self._connection.execute(query)
        events = [Event(**row) for row in rows]
        return events

    def find(self, event_id):
        rows = self._connection.execute('SELECT * FROM events WHERE event_id = %s', [event_id])
        if not rows:
            return None
        row = rows[0]
        event = Event(
            event_id=row['event_id'],
            event_name=row['event_name'],
            location=row['location'],
            event_start=row['event_start'],
            event_end=row['event_end'],
            qr_code_content=row['qr_code_content'],
            band_id=row['band_id'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
        return event

    def create(self, event):
        query =  """
            INSERT INTO events (event_name, location, event_start, event_end, qr_code_content, band_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING event_id, created_at, updated_at
            """
        params = (
            event.event_name,
            event.location,
            event.event_start,
            event.event_end,
            event.qr_code_content,
            event.band_id,
            event.created_at or datetime.now(),
            event.updated_at or datetime.now()
        )
        result = self._connection.execute(query, params)
        return result[0]['event_id']  # Return the newly created event's ID
    
    def update(self, event_id, event):
        query = """
            UPDATE events
            SET event_name = %s,
                location = %s,
                event_start = %s,
                event_end = %s,
                qr_code_content = %s,
                band_id = %s,
                updated_at = %s
            WHERE event_id = %s
            RETURNING event_id, created_at, updated_at
        """
        params = (
            event.event_name,
            event.location,
            event.event_start,
            event.event_end,
            event.qr_code_content,
            event.band_id,
            event.updated_at or datetime.now(),
            event_id
        )
        self._connection.execute(query, params)
        return None
    
    def delete(self, event_id):
        query = "DELETE FROM events WHERE event_id = %s"
        self._connection.execute(query, [event_id])
        return None

    def find_events_by_band_id(self, band_id):
        query = "SELECT * FROM events WHERE band_id = %s"
        rows = self._connection.execute(query, [band_id])
        if not rows:
            return None
        events = []
        for row in rows:
            event = Event(
                event_id=row['event_id'],
                event_name=row['event_name'],
                location=row['location'],
                event_start=row['event_start'],
                event_end=row['event_end'],
                qr_code_content=row['qr_code_content'],
                band_id=row['band_id'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            events.append(event)
        return events
        
