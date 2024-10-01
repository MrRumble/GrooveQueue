from api.events.event_model import Event
from api.events.event_repository import EventRepository
from api.common.db import get_flask_database_connection
from flask import current_app

def create_event(event: Event) -> str:

    if not event.event_name or event.event_name.strip() == "":
        raise ValueError("Invalid event name format.")
    
    if not event.location or event.location.strip() == "":
        raise ValueError("Location cannot be empty.")

    if event.event_start >= event.event_end:
        raise ValueError("Event end time must be after start time")
    
    if not event.band_id:
        raise ValueError("Band ID is required")
    
    if not event.qr_code_content:
        raise ValueError("QR code content cannot be empty")
    
    connection = get_flask_database_connection(current_app)
    event_repo = EventRepository(connection)
    return event_repo.create(event)
