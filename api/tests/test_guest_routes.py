from flask import json

def strip_timestamps(data):
    """Helper function to remove or normalize timestamp fields from data."""
    for entry in data:
        entry.pop('created_at', None)
        entry.pop('updated_at', None)
    return data

def test_get_all_guests(db_connection, web_client):
    db_connection.seed("../seeds/guests_table_test_data.sql")
    response = web_client.get('/guests')
    assert response.status_code == 200

    response_json = response.get_json()

    # Define expected data with placeholders for timestamps
    expected_data = [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "oauth_provider": "google",
            "oauth_provider_id": "google123",
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "password": "securepass456",
            "oauth_provider": "facebook",
            "oauth_provider_id": "fb456",
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "id": 3,
            "name": "Alice Johnson",
            "email": "alice.j@example.com",
            "password": "mypassword789",
            "oauth_provider": None,
            "oauth_provider_id": None,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "id": 4,
            "name": "Bob Brown",
            "email": "bob.brown@example.com",
            "password": "bobspassword",
            "oauth_provider": "github",
            "oauth_provider_id": "gh789",
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "id": 5,
            "name": "Carol White",
            "email": "carol.white@example.com",
            "password": "passwordcarol",
            "oauth_provider": None,
            "oauth_provider_id": None,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "id": 6,
            "name": "David Green",
            "email": "david.green@example.com",
            "password": "davidspass123",
            "oauth_provider": "twitter",
            "oauth_provider_id": "tw101",
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "id": 7,
            "name": "Eve Black",
            "email": "eve.black@example.com",
            "password": "evepassword321",
            "oauth_provider": None,
            "oauth_provider_id": None,
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "id": 8,
            "name": "Frank Blue",
            "email": "frank.blue@example.com",
            "password": "frankpass",
            "oauth_provider": "google",
            "oauth_provider_id": "google202",
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "id": 9,
            "name": "Grace Purple",
            "email": "grace.purple@example.com",
            "password": "gracepurplepass",
            "oauth_provider": "facebook",
            "oauth_provider_id": "fb987",
            "created_at": "PLACEHOLDER",
            "updated_at": "PLACEHOLDER"
        },
        {
            "id": 10,
            "name": "Henry Yellow",
            "email": "henry.yellow@example.com",
            "password": "henryyellow123",
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

def test_create_guest_missing_field_returns_error(web_client):

    data = {
            'email' : "jimmy-test@example.com",
            'password' : 'Password123!',
            'oauth_provider': None,
            'oauth_provider_id': None
            }
    
    response = web_client.post('/guests', json=data)
    assert response.status_code == 400

    response_json = response.get_json()
    assert response_json['error'] == "Missing required fields"

def test_create_guest_correct_fields_returns_result(web_client):

    data =  {
            'name' : 'Big Jim',
            'email' : "jimmy-test@example.com",
            'password' : 'Password123!',
            'oauth_provider': None,
            'oauth_provider_id': None
            }
    
    response = web_client.post('/guests', json=data)
    assert response.status_code == 201

    response_json = response.get_json()
    assert response_json['message'] == "New Guest created and stored in db."

def test_create_guest_oauth_field_wrong_data_type(web_client):

    data =  {
            'name' : 'Big Jim',
            'email' : "jimmy-test@example.com",
            'password' : 'Password123!',
            'oauth_provider': 1,
            'oauth_provider_id': None
            }
    
    response = web_client.post('/guests', json=data)
    assert response.status_code == 400

    response_json = response.get_json()
    assert response_json['error'] == "Invalid OAuth provider format"