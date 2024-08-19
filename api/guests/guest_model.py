import datetime

class Guest:
    def __init__(self, id=None, name=None, email=None, password=None,
                oauth_provider=None, oauth_provider_id=None,
                created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.oauth_provider = oauth_provider
        self.oauth_provider_id = oauth_provider_id
        self.created_at = created_at or datetime.datetime.now()
        self.updated_at = updated_at or datetime.datetime.now()

    def __eq__(self, other):
        if not isinstance(other, Guest):
            return False
        return (self.id == other.id and
                self.name == other.name and
                self.email == other.email and
                self.password == other.password and
                self.oauth_provider == other.oauth_provider and
                self.oauth_provider_id == other.oauth_provider_id)

    def __repr__(self):
        return (f"Guest(id={self.id}, email={self.email}, "
                f"name={self.name}, "
                f"oauth_provider={self.oauth_provider}, "
                f"oauth_provider_id={self.oauth_provider_id}, "
                f"created_at={self.created_at}, "
                f"updated_at={self.updated_at})")
