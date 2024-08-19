from api.guests.guest_model import Guest

class GuestRepository():
    def __init__(self, connection):
        self._connection = connection

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


    