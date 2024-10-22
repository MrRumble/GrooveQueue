from datetime import datetime, timedelta
from api.events.event_model import Event

def validate_event(event: Event) -> (bool, str):
    # Ensure event fields are properly populated
    if not event.event_name or event.event_name.strip() == "":
        return False, "Event name cannot be empty."
    
    if not event.location or event.location.strip() == "":
        return False, "Location cannot be empty."

    # Check that event start is before event end
    if event.event_start >= event.event_end:
        return False, "Event start must be before event end."
    
    # Ensure band ID is provided
    if not event.band_id:
        return False, "Band ID must be provided."
    
    # Ensure QR code content is provided
    if not event.qr_code_content:
        return False, "QR code content must be provided."

    # Check that the event start time is not in the past
    if event.event_start < datetime.now():
        return False, "Event start time cannot be in the past."

    # Check that event duration does not exceed 24 hours
    if event.event_end - event.event_start > timedelta(days=1):
        return False, "Event duration cannot exceed 24 hours."

    return True, ""  # All checks passed
