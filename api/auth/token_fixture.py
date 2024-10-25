from functools import wraps
from flask import request, jsonify
from api.auth.token_manager import TokenManager

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        jwt_token = request.headers.get('Authorization', '')

        # Check if the token exists and remove "Bearer " prefix
        if jwt_token.startswith('Bearer '):
            jwt_token = jwt_token.split(' ')[1]  # Extract the actual token
        else:
            return jsonify({"msg": "Invalid authorization format."}), 401  # Unauthorized response

        # Check if the token is blacklisted
        token_manager = TokenManager()
        if token_manager.is_token_blacklisted(jwt_token):
            return jsonify({"msg": "Token blacklisted!"}), 403  # Forbidden response

        return f(*args, **kwargs)  # Call the original function if validation is successful

    return decorated
