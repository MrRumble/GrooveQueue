from api.notifications.notification_model import Notification
import datetime

class NotificationRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        """Retrieve all notifications from the database."""
        query = "SELECT * FROM notifications"
        rows = self._connection.execute(query)
        notifications = [Notification(**row) for row in rows]
        return notifications

    def find(self, notification_id):
        """Retrieve a single notification by its ID."""
        rows = self._connection.execute('SELECT * FROM notifications WHERE notification_id = %s', [notification_id])
        
        if rows:  # Check if any rows were returned
            row = rows[0]
            return Notification(
                notification_id=row['notification_id'],
                recipient_id=row['recipient_id'],
                recipient_type=row['recipient_type'],
                event_id=row['event_id'],
                notification_type=row['notification_type'],
                message=row['message'],
                is_read=row['is_read'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        else:
            return None  # No notification found with the given ID

    def create(self, notification):
        """Insert a new notification into the database."""
        query = """
            INSERT INTO notifications (recipient_id, recipient_type, event_id, notification_type, message, is_read, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING notification_id, created_at, updated_at
        """
        params = (
            notification.recipient_id,
            notification.recipient_type,
            notification.event_id,
            notification.notification_type,
            notification.message,
            notification.is_read,
            notification.created_at or datetime.datetime.now(),
            notification.updated_at or datetime.datetime.now()
        )
        self._connection.execute(query, params)
        return None

    def delete(self, notification_id):
        """Delete a notification from the database."""
        query = "DELETE FROM notifications WHERE notification_id = %s"
        self._connection.execute(query, [notification_id])
        return None

    def find_unread_notifications(self, recipient_id, recipient_type):
        """Find all unread notifications for a specific recipient."""
        query = """
            SELECT * FROM notifications
            WHERE recipient_id = %s AND recipient_type = %s AND is_read = FALSE
        """
        rows = self._connection.execute(query, [recipient_id, recipient_type])
        return [Notification(**row) for row in rows]

    def update_is_read(self, notification_id, is_read):
        """Update the read status of a notification."""
        query = """
            UPDATE notifications
            SET is_read = %s, updated_at = %s
            WHERE notification_id = %s
        """
        params = (is_read, datetime.datetime.now(), notification_id)
        self._connection.execute(query, params)
        return None