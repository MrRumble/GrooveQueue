from api.requests.request_model import Request
from api.requests.request_repository import RequestRepository
from api.common.db import get_flask_database_connection
from flask import current_app

def validate_create_request(request: Request) -> str:
    """
    Create a new request in the database.

    Args:
        request (Request): The request object to be created.

    Returns:
        str: A success message if the request is created successfully.

    Raises:
        ValueError: If the request data is invalid.
    """
    if not request.song_name or request.song_name.strip() == "":
        raise ValueError("Song name cannot be empty.")
    
    if not request.guest_id:
        raise ValueError("Guest ID is required")
    
    if not request.event_id:
        raise ValueError("Event ID is required")
    
    # Optional: Validate that the guest_id and event_id exist in their respective tables
    # This might involve querying the database to ensure they exist.
    
    connection = get_flask_database_connection(current_app)
    request_repo = RequestRepository(connection)
    request_repo.create(request)

    return "Request successfully created."
