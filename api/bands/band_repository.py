from api.bands.band_model import Band
import datetime

class BandRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        query = "SELECT * FROM bands"
        rows = self._connection.execute(query)
        bands = [Band(**row) for row in rows]
        return bands

    def find(self, band_id):
        rows = self._connection.execute('SELECT * FROM bands WHERE band_id = %s', [band_id])
        if not rows:
            raise ValueError("Band not found")
        row = rows[0]
        band = Band(
            band_id=row['band_id'],
            band_name=row['band_name'],
            band_email=row['band_email'],
            password=row['password'],
            oauth_provider=row.get('oauth_provider'),
            oauth_provider_id=row.get('oauth_provider_id'),
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
        return band

    def create(self, band):
        query = """
            INSERT INTO bands (band_name, band_email, password, oauth_provider, oauth_provider_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING band_id, created_at, updated_at
        """
        params = (
            band.band_name,
            band.band_email,
            band.password,
            band.oauth_provider,
            band.oauth_provider_id,
            band.created_at or datetime.datetime.now(),
            band.updated_at or datetime.datetime.now()
        )
        result = self._connection.execute(query, params)
        band.band_id = result[0]['band_id']
        return band

    def update(self, band_id, band):
        query = """
            UPDATE bands
            SET band_name = %s,
                band_email = %s,
                password = %s,
                oauth_provider = %s,
                oauth_provider_id = %s,
                updated_at = %s
            WHERE band_id = %s
            RETURNING band_id, created_at, updated_at
        """
        params = (
            band.band_name,
            band.band_email,
            band.password,
            band.oauth_provider,
            band.oauth_provider_id,
            band.updated_at or datetime.datetime.now(),
            band_id
        )
        result = self._connection.execute(query, params)
        return result[0] if result else None

    def delete(self, band_id):
        query = "DELETE FROM bands WHERE band_id = %s"
        self._connection.execute(query, [band_id])
        return None

    def email_exists(self, email: str) -> bool:
        query = "SELECT 1 FROM bands WHERE band_email = %s LIMIT 1"
        rows = self._connection.execute(query, [email])
        return len(rows) > 0

    def find_by_email(self, email: str) -> Band:
        query = "SELECT * FROM bands WHERE band_email = %s LIMIT 1"
        rows = self._connection.execute(query, [email])
        
        # Check if any rows are returned
        if not rows:
            raise ValueError("Band not found")
        
        row = rows[0]
        return Band(
            band_id=row['band_id'],
            band_name=row['band_name'],
            band_email=row['band_email'],
            password=row['password'],
            oauth_provider=row.get('oauth_provider'),
            oauth_provider_id=row.get('oauth_provider_id'),
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
