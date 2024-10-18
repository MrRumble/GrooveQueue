from api.requests.request_model import Request
from datetime import datetime

class RequestRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        query = "SELECT * FROM requests"
        rows = self._connection.execute(query)
        requests = [Request(**row) for row in rows]
        return requests

    def find(self, request_id):
        query = 'SELECT * FROM requests WHERE request_id = %s'
        rows = self._connection.execute(query, [request_id])
        if not rows:
            return None
        row = rows[0]
        request = Request(
            request_id=row['request_id'],
            track_id=row['track_id'],  # Changed to track_id
            guest_id=row['guest_id'],
            event_id=row['event_id'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
        return request

    def create(self, request):
        query = """
            INSERT INTO requests (track_id, guest_id, event_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING request_id, created_at, updated_at
        """
        params = (
            request.track_id,  # Changed from song_name to track_id
            request.guest_id,
            request.event_id,
            request.created_at or datetime.now(),
            request.updated_at or datetime.now()
        )
        result = self._connection.execute(query, params)
        return result[0]['request_id']  # Return the newly created request's ID

    def delete(self, request_id):
        query = "DELETE FROM requests WHERE request_id = %s"
        self._connection.execute(query, [request_id])
        return None

    def find_requests_by_event_id(self, event_id):
        query = "SELECT * FROM requests WHERE event_id = %s"
        rows = self._connection.execute(query, [event_id])
        if not rows:
            return None
        requests = []
        for row in rows:
            request = Request(
                request_id=row['request_id'],
                track_id=row['track_id'],  # Changed to track_id
                guest_id=row['guest_id'],
                event_id=row['event_id'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            requests.append(request)
        return requests
    
    def requests_by_guest(self, guest_id, event_id):
        query = """
            SELECT COUNT(*) as request_count
            FROM requests
            WHERE guest_id = %s AND event_id = %s
        """
        result = self._connection.execute(query, [guest_id, event_id])
        return result[0]['request_count'] if result else 0
