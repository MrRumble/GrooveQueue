from flask import Blueprint, request, jsonify, current_app
from api.requests.request_model import Request
from api.requests.request_repository import RequestRepository
from api.common.db import get_flask_database_connection

request_bp = Blueprint('request_bp', __name__)

@request_bp.route('/requests/<int:request_id', methods=['GET'])
def get_request_by_id(event_id: int)-> Request:
    connection = get_flask_database_connection(current_app)
    request_repo = RequestRepository(connection)
    request = request_repo.find()
    
    if request is None:
        return jsonify(error="Event not found"), 404

    return jsonify(request.to_dict()), 200