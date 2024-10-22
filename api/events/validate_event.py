from api.events.event_model import Event

def validate_event(event: Event) -> bool:
    if not event.event_name or event.event_name.strip() == "":
        return False
    
    if not event.location or event.location.strip() == "":
        return False

    if event.event_start >= event.event_end:
        return False
    
    if not event.band_id:
        return False
    
    if not event.qr_code_content:
        return False
    
    return True  # Return True if all validation checks pass
