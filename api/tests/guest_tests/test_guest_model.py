from api.guests.guest_model import Guest
from datetime import datetime

def test_initialisation():
    # Test initialisation with no arguments
    guest = Guest()
    assert guest.id is None
    assert guest.name is None
    assert guest.email is None
    assert guest.password is None
    assert guest.oauth_provider is None
    assert guest.oauth_provider_id is None
    assert isinstance(guest.created_at, datetime)
    assert isinstance(guest.updated_at, datetime)
    print("test_initialization passed")

def test_initialisation_with_values():
    # Test initialisation with arguments
    guest = Guest(id=1, name="John Doe", email="john@example.com",
                password="secret", oauth_provider="google",
                oauth_provider_id="12345", 
                created_at=datetime(2023, 1, 1),
                updated_at=datetime(2023, 1, 2))

    assert guest.id == 1
    assert guest.name == "John Doe"
    assert guest.email == "john@example.com"
    assert guest.password == "secret"
    assert guest.oauth_provider == "google"
    assert guest.oauth_provider_id == "12345"
    assert guest.created_at == datetime(2023, 1, 1)
    assert guest.updated_at == datetime(2023, 1, 2)

def test_equality():
    # Test equality comparison
    guest1 = Guest(id=1, name="John Doe", email="john@example.com")
    guest2 = Guest(id=1, name="John Doe", email="john@example.com")
    guest3 = Guest(id=2, name="Jane Doe", email="jane@example.com")

    assert guest1 == guest2
    assert guest1 != guest3

def test_representation():
    # Test string representation
    guest = Guest(id=1, name="John Doe", email="john@example.com",
                oauth_provider="google", oauth_provider_id="12345",
                created_at=datetime(2023, 1, 1), 
                updated_at=datetime(2023, 1, 2))
    
    expected_repr = ("Guest(id=1, email=john@example.com, name=John Doe, "
                    "oauth_provider=google, oauth_provider_id=12345, "
                    "created_at=2023-01-01 00:00:00, "
                    "updated_at=2023-01-02 00:00:00)")
    
    assert repr(guest) == expected_repr


