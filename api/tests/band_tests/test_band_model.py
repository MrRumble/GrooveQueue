from datetime import datetime
from api.bands.band_model import Band  # Adjust import based on actual path

def test_initialisation():
    # Test initialization with no arguments
    band = Band()
    assert band.band_id is None
    assert band.band_name is None
    assert band.band_email is None
    assert band.password is None
    assert band.oauth_provider is None
    assert band.oauth_provider_id is None
    assert isinstance(band.created_at, datetime)
    assert isinstance(band.updated_at, datetime)
    print("test_initialisation passed")

def test_initialisation_with_values():
    # Test initialization with arguments
    band = Band(band_id=1, band_name="White Noise", band_email="whitenoise@example.com",
                password="hashedpassword", oauth_provider="facebook",
                oauth_provider_id="abcde12345", 
                created_at=datetime(2023, 1, 1),
                updated_at=datetime(2023, 1, 2))

    assert band.band_id == 1
    assert band.band_name == "White Noise"
    assert band.band_email == "whitenoise@example.com"
    assert band.password == "hashedpassword"
    assert band.oauth_provider == "facebook"
    assert band.oauth_provider_id == "abcde12345"
    assert band.created_at == datetime(2023, 1, 1)
    assert band.updated_at == datetime(2023, 1, 2)
    print("test_initialisation_with_values passed")

def test_equality():
    # Test equality comparison
    band1 = Band(band_id=1, band_name="White Noise", band_email="whitenoise@example.com")
    band2 = Band(band_id=1, band_name="White Noise", band_email="whitenoise@example.com")
    band3 = Band(band_id=2, band_name="The Jazzers", band_email="jazzers@example.com")

    assert band1 == band2
    assert band1 != band3
    print("test_equality passed")

def test_representation():
    # Test string representation
    band = Band(band_id=1, band_name="White Noise", band_email="whitenoise@example.com",
                oauth_provider="facebook", oauth_provider_id="abcde12345",
                created_at=datetime(2023, 1, 1), 
                updated_at=datetime(2023, 1, 2))
    
    expected_repr = ("Band(band_id=1, band_name=White Noise, band_email=whitenoise@example.com, "
                    "oauth_provider=facebook, oauth_provider_id=abcde12345, "
                    "created_at=2023-01-01 00:00:00, "
                    "updated_at=2023-01-02 00:00:00)")
    
    assert repr(band) == expected_repr
    print("test_representation passed")

def test_to_dict():
    # Test dictionary conversion
    band = Band(band_id=1, band_name="White Noise", band_email="whitenoise@example.com",
                oauth_provider="facebook", oauth_provider_id="abcde12345",
                created_at=datetime(2023, 1, 1), 
                updated_at=datetime(2023, 1, 2))

    expected_dict = {
        "band_id": 1,
        "band_name": "White Noise",
        "band_email": "whitenoise@example.com",
        "password": None,  # Assuming password is not included in the dict
        "oauth_provider": "facebook",
        "oauth_provider_id": "abcde12345",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-02T00:00:00"
    }
    
    assert band.to_dict() == expected_dict
    print("test_to_dict passed")
