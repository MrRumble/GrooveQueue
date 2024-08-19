from api.guests.guest_model import Guest

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
    