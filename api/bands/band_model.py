import datetime

class Band:
    def __init__(self, band_id=None, band_name=None, band_email=None, password=None,
                 oauth_provider=None, oauth_provider_id=None,
                 profile_picture_path=None, created_at=None, updated_at=None):
        self.band_id = band_id
        self.band_name = band_name
        self.band_email = band_email
        self.password = password
        self.oauth_provider = oauth_provider
        self.oauth_provider_id = oauth_provider_id
        self.profile_picture_path = profile_picture_path
        self.created_at = created_at or datetime.datetime.now()
        self.updated_at = updated_at or datetime.datetime.now()

    def __eq__(self, other):
        if not isinstance(other, Band):
            return False
        return (self.band_id == other.band_id and
                self.band_name == other.band_name and
                self.band_email == other.band_email and
                self.password == other.password and
                self.oauth_provider == other.oauth_provider and
                self.oauth_provider_id == other.oauth_provider_id and
                self.profile_picture_path == other.profile_picture_path)

    def __repr__(self):
        return (f"Band(band_id={self.band_id}, band_name={self.band_name}, "
                f"band_email={self.band_email}, "
                f"oauth_provider={self.oauth_provider}, "
                f"oauth_provider_id={self.oauth_provider_id}, "
                f"profile_picture_path={self.profile_picture_path}, "
                f"created_at={self.created_at}, "
                f"updated_at={self.updated_at})")

    def to_dict(self):
        return {
            "band_id": self.band_id,
            "band_name": self.band_name,
            "band_email": self.band_email,
            "password": self.password,
            "oauth_provider": self.oauth_provider,
            "oauth_provider_id": self.oauth_provider_id,
            "profile_picture_path": self.profile_picture_path,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
