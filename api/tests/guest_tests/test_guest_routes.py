import pytest
from flask import url_for
from werkzeug.security import check_password_hash
from api.guests.guest_model import Guest
from api.guests.guest_repository import GuestRepository
from api.common.db import get_flask_database_connection


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

def test_create_guest_correct_fields_stored_in_db(db_connection, web_client):
    db_connection.seed("../seeds/guests_table_test_data.sql")
    data = {
        'name': 'Big Jim',
        'email': 'jimmy-jimbob@example.com',
        'password': 'Password123!',
        'oauth_provider': '',
        'oauth_provider_id': ''
    }

    response = web_client.post('/guests', data=data)
    assert response.status_code == 302
    
    guest_repo = GuestRepository(db_connection)
    guests = guest_repo.find_all()
    created_guest_emails = [guest.email for guest in guests]
    assert data['email'] in created_guest_emails

def test_create_guest_invalid_fields_not_in_db(db_connection, web_client):
    db_connection.seed("../seeds/guests_table_test_data.sql")
    guest_repo = GuestRepository(db_connection)
    data_name_empty = {
        'name': '',
        'email': 'jimmy-jimbob@example.com',
        'password': 'Password123!',
        'oauth_provider': '',
        'oauth_provider_id': ''
    }
    data_email_empty = {
        'name': 'Big Jim',
        'email': '',
        'password': 'Password123!',
        'oauth_provider': '',
        'oauth_provider_id': ''
    }
    data_email_invalid = {
        'name': 'Big Jim',
        'email': 'jimmy-jimbob.example.com',
        'password': 'Password123!',
        'oauth_provider': '',
        'oauth_provider_id': ''
    }
    data_password_invalid = {
        'name': 'Big Jim',
        'email': 'jimmy-jimbob@example.com',
        'password': 'Password123',
        'oauth_provider': '',
        'oauth_provider_id': ''
    }

    web_client.post('/guests', data=data_name_empty)
    guests = guest_repo.find_all()
    created_guest_emails = [guest.email for guest in guests]
    print(created_guest_emails)
    assert data_name_empty['email'] not in created_guest_emails
    web_client.post('/guests', data=data_email_empty)
    guests = guest_repo.find_all()
    created_guest_emails = [guest.email for guest in guests]
    assert data_email_empty['email'] not in created_guest_emails
    web_client.post('/guests', data=data_email_invalid)
    guests = guest_repo.find_all()
    created_guest_emails = [guest.email for guest in guests]
    assert data_email_invalid['email'] not in created_guest_emails
    web_client.post('/guests', data=data_password_invalid)
    guests = guest_repo.find_all()
    created_guest_emails = [guest.email for guest in guests]
    assert data_password_invalid['email'] not in created_guest_emails
    

def test_hashed_password_stored_in_db(db_connection, web_client):
    guest_repo = GuestRepository(db_connection)
    data =  {
            'name' : 'Big Jim',
            'email' : "jimmy-test3@example.com",
            'password' : 'Password1234!'
            }
    
    web_client.post('/signupguest', json=data)

    guests = guest_repo.find_all()
    created_guest = guests[-1]
    assert created_guest.password != data['password']
    

