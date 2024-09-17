from api.guests.guest_repository import GuestRepository

def test_create_guest_correct_fields_stored_in_db(db_connection, web_client):
    guest_repo = GuestRepository(db_connection)
    data =  {
            'name' : 'Big Jim',
            'email' : "jimmy-test@example.com",
            'password' : 'Password123!'
            }
    
    response = web_client.post('/signupguest', json=data)
    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json['message'] == "New Guest created and stored in db."

    guests = guest_repo.find_all()
    created_guest_emails = [guest.email for guest in guests]
    assert data['email'] in created_guest_emails

def test_create_guest_invalid_fields_not_in_db(db_connection, web_client):
    guest_repo = GuestRepository(db_connection)
    data =  {
            'name' : 'Big Jim',
            'email' : "jimmy-test2@example.com",
            'password' : 'Password123'
            }
    
    web_client.post('/signupguest', json=data)
    
    guests = guest_repo.find_all()
    created_guest_emails = [guest.email for guest in guests]
    assert data['email'] not in created_guest_emails