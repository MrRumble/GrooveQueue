from api.guests.guest_model import Guest
from api.guests.guest_repository import GuestRepository
import datetime


"""
When I use .find_by_id I return the user id
"""

def test_find_user_by_id(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/guests_table_test_data.sql")
    
    # Create an instance of GuestRepository
    guest_repo = GuestRepository(db_connection)
    
    # Find the guest with id 1
    result = guest_repo.find(1)
    
    # Create the expected Guest object
    expected_guest = Guest(
        id=1,
        name='John Doe',
        email='john.doe@example.com',
        password='password123',
        oauth_provider='google',
        oauth_provider_id='google123',
        created_at=None,  # We will handle timestamp comparison separately
        updated_at=None   # We will handle timestamp comparison separately
    )
    
    # Check if the result is not None
    assert result is not None

    # Compare individual attributes, excluding created_at and updated_at
    assert result.id == expected_guest.id
    assert result.name == expected_guest.name
    assert result.email == expected_guest.email
    assert result.password == expected_guest.password
    assert result.oauth_provider == expected_guest.oauth_provider
    assert result.oauth_provider_id == expected_guest.oauth_provider_id

    # Optionally, compare timestamps with some tolerance if needed
    # This will depend on how precise you want the comparison to be
    assert abs((result.created_at - expected_guest.created_at).total_seconds()) < 1
    assert abs((result.updated_at - expected_guest.updated_at).total_seconds()) < 1
