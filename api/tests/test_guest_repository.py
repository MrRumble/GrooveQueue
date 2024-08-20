from api.guests.guest_model import Guest
from api.guests.guest_repository import GuestRepository


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

def test_find_all(db_connection):
    db_connection.seed("../seeds/guests_table_test_data.sql")
    guest_repo = GuestRepository(db_connection)
    results = guest_repo.find_all()
    
    expected_guests = [
        Guest(
            id=1,
            name='John Doe',
            email='john.doe@example.com',
            password='password123',
            oauth_provider='google',
            oauth_provider_id='google123',
            created_at=None,  # Timestamps to be checked separately
            updated_at=None   # Timestamps to be checked separately
        ),
        Guest(
            id=2,
            name='Jane Smith',
            email='jane.smith@example.com',
            password='securepass456',
            oauth_provider='facebook',
            oauth_provider_id='fb456',
            created_at=None,
            updated_at=None
        ),
        Guest(
            id=3,
            name='Alice Johnson',
            email='alice.j@example.com',
            password='mypassword789',
            oauth_provider=None,
            oauth_provider_id=None,
            created_at=None,
            updated_at=None
        ),
        Guest(
            id=4,
            name='Bob Brown',
            email='bob.brown@example.com',
            password='bobspassword',
            oauth_provider='github',
            oauth_provider_id='gh789',
            created_at=None,
            updated_at=None
        ),
        Guest(
            id=5,
            name='Carol White',
            email='carol.white@example.com',
            password='passwordcarol',
            oauth_provider=None,
            oauth_provider_id=None,
            created_at=None,
            updated_at=None
        ),
        Guest(
            id=6,
            name='David Green',
            email='david.green@example.com',
            password='davidspass123',
            oauth_provider='twitter',
            oauth_provider_id='tw101',
            created_at=None,
            updated_at=None
        ),
        Guest(
            id=7,
            name='Eve Black',
            email='eve.black@example.com',
            password='evepassword321',
            oauth_provider=None,
            oauth_provider_id=None,
            created_at=None,
            updated_at=None
        ),
        Guest(
            id=8,
            name='Frank Blue',
            email='frank.blue@example.com',
            password='frankpass',
            oauth_provider='google',
            oauth_provider_id='google202',
            created_at=None,
            updated_at=None
        ),
        Guest(
            id=9,
            name='Grace Purple',
            email='grace.purple@example.com',
            password='gracepurplepass',
            oauth_provider='facebook',
            oauth_provider_id='fb987',
            created_at=None,
            updated_at=None
        ),
        Guest(
            id=10,
            name='Henry Yellow',
            email='henry.yellow@example.com',
            password='henryyellow123',
            oauth_provider=None,
            oauth_provider_id=None,
            created_at=None,
            updated_at=None
        ),
    ]
    # Check if the number of results is as expected
    assert len(results) == len(expected_guests)
    
    # Compare individual attributes of each guest
    for result, expected_guest in zip(results, expected_guests):
        assert result.id == expected_guest.id
        assert result.name == expected_guest.name
        assert result.email == expected_guest.email
        assert result.password == expected_guest.password
        assert result.oauth_provider == expected_guest.oauth_provider
        assert result.oauth_provider_id == expected_guest.oauth_provider_id
        
        # Optionally, compare timestamps with some tolerance
        if expected_guest.created_at:
            assert abs((result.created_at - expected_guest.created_at).total_seconds()) < 1
        else:
            assert result.created_at is None
        
        if expected_guest.updated_at:
            assert abs((result.updated_at - expected_guest.updated_at).total_seconds()) < 1
        else:
            assert result.updated_at is None

def test_create(db_connection):
    # Create an instance of GuestRepository
    guest_repo = GuestRepository(db_connection)
    
    # Create a new Guest object
    new_guest = Guest(
        name='New Guest',
        email='new.guest@example.com',
        password='newpassword',
        oauth_provider='twitter',
        oauth_provider_id='tw202'
    )
    
    # Insert the new guest into the database
    guest_repo.create(new_guest)
    found_guest = guest_repo.find(11)
    assert found_guest.id == 11
    assert found_guest.name == "New Guest"
    assert found_guest.email == "new.guest@example.com"
    assert found_guest.password == "newpassword"
    assert found_guest.oauth_provider == 'twitter'
    assert found_guest.oauth_provider_id == "tw202"
    
def test_update(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/guests_table_test_data.sql")
    
    # Create an instance of GuestRepository
    guest_repo = GuestRepository(db_connection)
    
    # Find an existing guest to update
    guest_to_update = guest_repo.find(1)
    
    # Modify the guest's details
    guest_to_update.name = "Updated Name"
    guest_to_update.email = "updated.email@example.com"
    guest_to_update.password = "updatedpassword"
    guest_to_update.oauth_provider = "github"
    guest_to_update.oauth_provider_id = "gh12345"
    
    # Perform the update operation
    guest_repo.update(guest_to_update.id, guest_to_update)
    
    # Fetch the updated guest from the database
    updated_guest = guest_repo.find(guest_to_update.id)
    
    # Assert the updated fields
    assert updated_guest.name == "Updated Name"
    assert updated_guest.email == "updated.email@example.com"
    assert updated_guest.password == "updatedpassword"
    assert updated_guest.oauth_provider == "github"
    assert updated_guest.oauth_provider_id == "gh12345"
    
    # Check that the IDs match
    assert updated_guest.id == guest_to_update.id
