from api.bands.band_model import Band
from api.bands.band_repository import BandRepository
import datetime

def test_find_band_by_id(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/bands_table_test_data.sql")
    
    # Create an instance of BandRepository
    band_repo = BandRepository(db_connection)
    
    # Find the band with id 1
    result = band_repo.find(1)
    
    # Create the expected Band object, including the new field
    expected_band = Band(
        band_id=1,
        band_name='White Noise',
        band_email='white.noise@example.com',
        password='bandpass123',
        oauth_provider='spotify',
        oauth_provider_id='spotify123',
        profile_picture_path='path/to/profile1.jpg',  # Adjusted to include new field
        created_at=None,  # Handle timestamp comparison separately
        updated_at=None   # Handle timestamp comparison separately
    )
    
    # Check if the result is not None
    assert result is not None

    # Compare individual attributes, excluding created_at and updated_at
    assert result.band_id == expected_band.band_id
    assert result.band_name == expected_band.band_name
    assert result.band_email == expected_band.band_email
    assert result.password == expected_band.password
    assert result.oauth_provider == expected_band.oauth_provider
    assert result.oauth_provider_id == expected_band.oauth_provider_id
    assert result.profile_picture_path == expected_band.profile_picture_path  # New field comparison

    # Optionally, compare timestamps with some tolerance if needed
    assert abs((result.created_at - expected_band.created_at).total_seconds()) < 1
    assert abs((result.updated_at - expected_band.updated_at).total_seconds()) < 1

def test_find_all_bands(db_connection):
    db_connection.seed("../seeds/bands_table_test_data.sql")
    band_repo = BandRepository(db_connection)
    results = band_repo.find_all()
    
    expected_bands = [
        Band(
            band_id=1,
            band_name='White Noise',
            band_email='white.noise@example.com',
            password='bandpass123',
            oauth_provider='spotify',
            oauth_provider_id='spotify123',
            profile_picture_path='path/to/profile1.jpg',  # Adjusted to include new field
            created_at=None,  # Timestamps to be checked separately
            updated_at=None   # Timestamps to be checked separately
        ),
        Band(
            band_id=2,
            band_name='The Rockers',
            band_email='rockers@example.com',
            password='rockpass456',
            oauth_provider='apple',
            oauth_provider_id='apple456',
            profile_picture_path='path/to/profile2.jpg',  # Adjusted to include new field
            created_at=None,
            updated_at=None
        ),
        Band(
            band_id=3,
            band_name='The Jazzmen',
            band_email='jazzmen@example.com',
            password='jazzpass789',
            oauth_provider=None,
            oauth_provider_id=None,
            profile_picture_path=None,  # Adjusted to include new field
            created_at=None,
            updated_at=None
        ),
        Band(
            band_id=4,
            band_name='No Events Band',
            band_email='noevents@example.com',
            password='bandpass123',
            oauth_provider=None,
            oauth_provider_id=None,
            profile_picture_path='path/to/profile4.jpg',  # Adjusted to include new field
            created_at=None,
            updated_at=None
        )
    ]
    
    # Check if the number of results is as expected
    assert len(results) == len(expected_bands)
    
    # Compare individual attributes of each band
    for result, expected_band in zip(results, expected_bands):
        assert result.band_id == expected_band.band_id
        assert result.band_name == expected_band.band_name
        assert result.band_email == expected_band.band_email
        assert result.password == expected_band.password
        assert result.oauth_provider == expected_band.oauth_provider
        assert result.oauth_provider_id == expected_band.oauth_provider_id
        assert result.profile_picture_path == expected_band.profile_picture_path  # New field comparison
        
        # Optionally, compare timestamps with some tolerance
        if expected_band.created_at:
            assert abs((result.created_at - expected_band.created_at).total_seconds()) < 1
        else:
            assert result.created_at is None
        
        if expected_band.updated_at:
            assert abs((result.updated_at - expected_band.updated_at).total_seconds()) < 1
        else:
            assert result.updated_at is None

def test_create_band(db_connection):
    # Create an instance of BandRepository
    band_repo = BandRepository(db_connection)
    
    # Create a new Band object, including the new field
    new_band = Band(
        band_name='New Band',
        band_email='new.band@example.com',
        password='newbandpass',
        oauth_provider='twitter',
        oauth_provider_id='tw202',
        profile_picture_path=None  # Include new field
    )
    
    # Insert the new band into the database
    band_repo.create(new_band)
    found_band = band_repo.find(5) 
    assert found_band.band_id == 5
    assert found_band.band_name == "New Band"
    assert found_band.band_email == "new.band@example.com"
    assert found_band.password == "newbandpass"
    assert found_band.oauth_provider == 'twitter'
    assert found_band.oauth_provider_id == "tw202"
    assert found_band.profile_picture_path is None  # Assert new field is None

def test_update_band(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/bands_table_test_data.sql")
    
    # Create an instance of BandRepository
    band_repo = BandRepository(db_connection)
    
    # Find an existing band to update
    band_to_update = band_repo.find(1)
    
    # Modify the band's details, including the new field
    band_to_update.band_name = "Updated Band Name"
    band_to_update.band_email = "updated.band@example.com"
    band_to_update.password = "updatedbandpass"
    band_to_update.oauth_provider = "github"
    band_to_update.oauth_provider_id = "gh12345"
    band_to_update.profile_picture_path = "path/to/profile/pic.jpg"  # Set new field
    
    # Perform the update operation
    band_repo.update(band_to_update.band_id, band_to_update)
    
    # Fetch the updated band from the database
    updated_band = band_repo.find(band_to_update.band_id)
    
    # Assert the updated fields, including the new field
    assert updated_band.band_name == "Updated Band Name"
    assert updated_band.band_email == "updated.band@example.com"
    assert updated_band.password == "updatedbandpass"
    assert updated_band.oauth_provider == "github"
    assert updated_band.oauth_provider_id == "gh12345"
    assert updated_band.profile_picture_path == "path/to/profile/pic.jpg"  # Assert new field

    # Check that the IDs match
    assert updated_band.band_id == band_to_update.band_id

def test_delete_band(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/bands_table_test_data.sql")
    
    # Create an instance of BandRepository
    band_repo = BandRepository(db_connection)
    
    # Ensure band with id 1 exists before deletion
    band_before_deletion = band_repo.find(1)
    assert band_before_deletion is not None
    
    # Delete the band with id 1
    band_repo.delete(1)
    
    # Try to find the deleted band
    try:
        band_repo.find(1)
        band_found = True
    except ValueError:
        band_found = False
    
    # Assert that the band was deleted
    assert band_found is False

    all_bands = band_repo.find_all()
    assert len(all_bands) == 3  

def test_band_email_exists(db_connection):
    band_repo = BandRepository(db_connection)
    result = band_repo.email_exists("rockers@example.com")   # In test DB
    assert result is True

    false_result = band_repo.email_exists("unique-band-email@example.com")   # Not test DB
    assert false_result is False
