# notifications_routes.py
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt
from api.common.db import get_flask_database_connection
from api.notifications.notification_repository import NotificationRepository

# Create a blueprint for notifications
notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """
    Get notifications for the logged-in user (guest or band).
    """
    claims = get_jwt()
    
    # Retrieve the role from the claims
    user_type = claims.get('role', None)
    user_id = claims['sub'] 

    try:
        # Establish a database connection
        connection = get_flask_database_connection(current_app)
        notification_repo = NotificationRepository(connection)

        # Fetch notifications based on user type
        notifications = notification_repo.find_unread_notifications(user_id, user_type)
        # Convert notifications to a dictionary format for JSON response
        notifications_list = [notification.to_dict() for notification in notifications]
        return jsonify(notifications=notifications_list), 200

    except Exception as e:
        return jsonify(error=str(e)), 500

@notifications_bp.route('/notifications/count', methods=['GET'])
@jwt_required()
def get_notification_count():
    claims = get_jwt()
    user_id = claims['sub']
    user_type = claims.get('role')

    connection = get_flask_database_connection(current_app)
    notification_repo = NotificationRepository(connection)

    count = notification_repo.count_unread_notifications(user_id, user_type)
    return jsonify(count=count), 200

@notifications_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_as_read(notification_id):
    """
    Mark a notification as read.
    """
    claims = get_jwt()
    user_id = claims['sub'] 
    user_type = claims.get('role')

    try:
        # Establish a database connection
        connection = get_flask_database_connection(current_app)
        notification_repo = NotificationRepository(connection)

        # Call the repository method to update the notification
        notification_repo.update_is_read(notification_id, is_read=True)

        return jsonify(message="Notification marked as read."), 200

    except Exception as e:
        return jsonify(error=str(e)), 500
