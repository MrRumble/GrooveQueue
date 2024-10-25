from flask import request
from api.auth.token_manager import TokenManager

def validate_token(jwt_token):
    token_manager = TokenManager()

    # Get the token from the Authorization header
    jwt_token = request.headers.get('Authorization', '')

    # Check if the token exists and remove "Bearer " prefix
    if jwt_token.startswith('Bearer '):
        jwt_token = jwt_token.split(' ')[1]  # Extract the actual token
    else:
        return False  # Invalid authorization format

    if token_manager.is_token_blacklisted(jwt_token):
        return False  # Token is blacklisted

    return True  # Return the valid token
