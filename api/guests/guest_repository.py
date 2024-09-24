from api.guests.guest_model import Guest
import datetime

class GuestRepository():
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        query = "SELECT * FROM guests"
        rows = self._connection.execute(query)
        guests = [Guest(**row) for row in rows]
        return guests

    def find(self, guest_id):
        rows = self._connection.execute('SELECT * FROM guests WHERE id = %s', [guest_id])
        row = rows[0]
        guest = Guest(
                    id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    password=row['password'],
                    oauth_provider=row.get('oauth_provider'),
                    oauth_provider_id=row.get('oauth_provider_id'),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
        return guest

    def create(self, guest):
        query =  """
            INSERT INTO guests (name, email, password, oauth_provider, oauth_provider_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at, updated_at
            """
        params = (
                guest.name,
                guest.email,
                guest.password,
                guest.oauth_provider,
                guest.oauth_provider_id,
                guest.created_at or datetime.now(),
                guest.updated_at or datetime.now()
            )
        self._connection.execute(query, params)
        return None
    
    def update(self, guest_id, guest):
        query = """
            UPDATE guests
            SET name = %s,
                email = %s,
                password = %s,
                oauth_provider = %s,
                oauth_provider_id = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING id, created_at, updated_at
        """
        params = (
                guest.name,
                guest.email,
                guest.password,
                guest.oauth_provider,
                guest.oauth_provider_id,
                guest.updated_at or datetime.datetime.now(),
                guest_id
            )
        self._connection.execute(query, params)
        return None
    
    def delete(self, guest_id):
        query = "DELETE FROM guests WHERE id = %s"
        self._connection.execute(query, [guest_id])
        return None
    
    def email_exists(self, email: str) -> bool:
        query = "SELECT 1 FROM guests WHERE email = %s LIMIT 1"
        rows = self._connection.execute(query, [email])
        return len(rows) > 0

    def find_by_email(self, email: str) -> Guest:
        query = "SELECT * FROM guests WHERE email = %s LIMIT 1"
        rows = self._connection.execute(query, [email])
        if len(rows) == 0:
            return None
        return Guest(**rows[0])
    