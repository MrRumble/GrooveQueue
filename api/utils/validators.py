import re

def validate_password(password: str) -> bool:

    # Check length
    if len(password) < 8:
        return False

    # Check for uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for lowercase letter
    if not re.search(r'[a-z]', password):
        return False

    # Check for digit
    if not re.search(r'[0-9]', password):
        return False

    # Check for special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True

import re

def validate_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(email_regex, email):
        try:
            local_part, domain_part = email.split('@')
            if '..' in domain_part:
                return False
            return True
        except ValueError:
            return False
    return False
