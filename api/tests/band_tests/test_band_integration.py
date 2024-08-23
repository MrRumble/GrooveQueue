from api.bands.band_repository import BandRepository

def test_create_band_correct_fields_stored_in_db(db_connection, web_client):
    # Initialize the repository
    band_repo = BandRepository(db_connection)
    
    # Define valid data for creating a band
    data = {
        'band_name': 'Rock Legends',
        'band_email': "rocklegends@example.com",
        'password': 'RockPass123!'
    }
    
    # Send a POST request to create a new band
    response = web_client.post('/bands', json=data)
    assert response.status_code == 201
    
    # Check the response message
    response_json = response.get_json()
    assert response_json['message'] == "New Band created and stored in db."

    # Fetch all bands from the repository
    bands = band_repo.find_all()
    created_band_emails = [band.band_email for band in bands]
    
    # Assert that the newly created band's email is in the list of emails
    assert data['band_email'] in created_band_emails

def test_create_band_invalid_fields_not_in_db(db_connection, web_client):
    # Initialize the repository
    band_repo = BandRepository(db_connection)
    
    # Define invalid data for creating a band
    data = {
        'band_name': 'Rock Legends',
        'band_email': "rocklegends2@example.com",
        'password': 'shortpass'
    }
    
    # Send a POST request to create a new band
    response = web_client.post('/bands', json=data)
    
    # Check that the response status code indicates an error
    assert response.status_code == 400
    
    # Fetch all bands from the repository
    bands = band_repo.find_all()
    created_band_emails = [band.band_email for band in bands]
    
    # Assert that the invalid band's email is not in the list of emails
    assert data['band_email'] not in created_band_emails
