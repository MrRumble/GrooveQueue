from api.guests.guest_repository import GuestRepository
from api.guests.guest_model import Guest
from api.common.db import get_flask_database_connection
from api.utils.validators import validate_email, validate_password
from flask import current_app
from werkzeug.security import generate_password_hash


def sign_up_guest(guest: Guest) -> str:
    connection = get_flask_database_connection(current_app)
    guest_repo = GuestRepository(connection)
    
    if not validate_email(guest.email):
        raise ValueError("Invalid email format")
    
    if not validate_password(guest.password):
        raise ValueError("Password must be at least 8 characters long, include uppercase, lowercase, number, and special character")
    
    if not guest.name or guest.name.strip() == "":
        raise ValueError("Name cannot be empty")

    if guest_repo.email_exists(guest.email):
        raise ValueError("Email already in use")

    # Hash the password
    guest.password = generate_password_hash(guest.password)
    
    guest_repo.create(guest)
    return "New Guest created and stored in db."

