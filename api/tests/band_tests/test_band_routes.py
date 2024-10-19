def strip_timestamps(data):
    """Helper function to remove or normalize timestamp fields from data."""
    for entry in data:
        entry.pop('created_at', None)
        entry.pop('updated_at', None)
    return data

def test_get_all_bands(db_connection, web_client):
    db_connection.seed("../seeds/bands_table_test_data.sql")  # Seed the test database
    response = web_client.get('/bands')
    assert response.status_code == 200

    response_json = response.get_json()

    # Define expected data with placeholders for timestamps
    expected_data = [
                {
            "band_id": 1,
            "band_name": "White Noise",
            "band_email": "white.noise@example.com",
            "password": "bandpass123",
            "oauth_provider": "spotify",
            "oauth_provider_id": "spotify123",
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "band_id": 2,
            "band_name": "The Rockers",
            "band_email": "rockers@example.com",
            "password": "rockpass456",
            "oauth_provider": "apple",
            "oauth_provider_id": "apple456",
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "band_id": 3,
            "band_name": "The Jazzmen",
            "band_email": "jazzmen@example.com",
            "password": "jazzpass789",
            "oauth_provider": None,
            "oauth_provider_id": None,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "band_id": 4,
            "band_name": "No Events Band",
            "band_email": "noevents@example.com",
            "password": "bandpass123",
            "oauth_provider": None,
            "oauth_provider_id": None,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        }

    ]

    # Strip timestamps from actual data for comparison
    stripped_actual = strip_timestamps(response_json.copy())
    stripped_expected = strip_timestamps(expected_data.copy())

    # Perform assertion
    assert stripped_actual == stripped_expected

def test_create_band_missing_field_returns_error(web_client):
    data = {
        'band_email': "band-test@example.com",
        'password': 'BandPass123!',
        'oauth_provider': None,
        'oauth_provider_id': None
    }
    
    response = web_client.post('/bands', json=data)
    assert response.status_code == 400

    response_json = response.get_json()
    assert response_json['error'] == "Missing required fields"

def test_create_band_correct_fields_returns_result(web_client):
    data = {
        'band_name': 'The Blues Brothers',
        'band_email': "bluesbrothers@example.com",
        'password': 'BluesPass123!',
        'oauth_provider': None,
        'oauth_provider_id': None
    }
    
    response = web_client.post('/bands', json=data)
    assert response.status_code == 201

    response_json = response.get_json()
    assert response_json['message'] == "New Band created and stored in db."

def test_create_band_oauth_field_wrong_data_type(web_client):
    data = {
        'band_name': 'The Metalheads',
        'band_email': "metalheads@example.com",
        'password': 'MetalPass123!',
        'oauth_provider': 1,  # Invalid type
        'oauth_provider_id': None
    }
    
    response = web_client.post('/bands', json=data)
    assert response.status_code == 400

    response_json = response.get_json()
    assert response_json['error'] == "Invalid OAuth provider format"

def test_login_band_correct_credentials_returns_token(web_client):
    data = {
        'band_email': "bluesbrothers@example.com",
        'password': 'BluesPass123!',
    }
    
    response = web_client.post('/bands/login', json=data)
    assert response.status_code == 200

    response_json = response.get_json()
    print(response_json)
    assert 'access_token' in response_json


def test_login_band_incorrect_credentials_returns_error(web_client):
    data = {
        'band_email': "bluesbrothers@example.com",
        'password': 'IncorrectPassword!',
    }
    
    response = web_client.post('/bands/login', json=data)
    assert response.status_code == 401


    

