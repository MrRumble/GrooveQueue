from api.notifications.notification_model import Notification
from api.notifications.notification_repository import NotificationRepository
import datetime

def test_find_notification_by_id(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/notifications_table_test_data.sql")
    
    # Create an instance of NotificationRepository
    notification_repo = NotificationRepository(db_connection)
    
    # Find the notification with id 1
    result = notification_repo.find(1)
    
    # Create the expected Notification object
    expected_notification = Notification(
        notification_id=1,
        recipient_id=1,
        recipient_type='guest',
        event_id=1,
        notification_type='attendance_accepted',
        message='John Doe, your attendance has been confirmed for Rocking the City.',
        is_read=False,
        created_at=None,  # Handle timestamp comparison separately
        updated_at=None   # Handle timestamp comparison separately
    )
    
    # Check if the result is not None
    assert result is not None

    # Compare individual attributes, excluding created_at and updated_at
    assert result.notification_id == expected_notification.notification_id
    assert result.recipient_id == expected_notification.recipient_id
    assert result.recipient_type == expected_notification.recipient_type
    assert result.event_id == expected_notification.event_id
    assert result.notification_type == expected_notification.notification_type
    assert result.message == expected_notification.message
    assert result.is_read == expected_notification.is_read

    # Optionally, compare timestamps with some tolerance if needed
    assert abs((result.created_at - expected_notification.created_at).total_seconds()) < 1
    assert abs((result.updated_at - expected_notification.updated_at).total_seconds()) < 1

def test_find_all_notifications(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/notifications_table_test_data.sql")
    
    # Create an instance of NotificationRepository
    notification_repo = NotificationRepository(db_connection)
    
    # Fetch all notifications from the repository
    results = notification_repo.find_all()
    
    # Define the expected Notification objects based on the seed data
    expected_notifications = [
        Notification(
            notification_id=1,
            recipient_id=1,
            recipient_type='guest',
            event_id=1,
            notification_type='attendance_accepted',
            message='John Doe, your attendance has been confirmed for Rocking the City.',
            is_read=False,
            created_at=None,
            updated_at=None
        ),
        Notification(
            notification_id=2,
            recipient_id=2,
            recipient_type='guest',
            event_id=3,
            notification_type='request_received',
            message='Jane Smith, your request for The Big Apple Concert has been received.',
            is_read=False,
            created_at=None,
            updated_at=None
        ),
        Notification(
            notification_id=3,
            recipient_id=3,
            recipient_type='guest',
            event_id=2,
            notification_type='attendance_accepted',
            message='Alice Johnson, you have been accepted for Jazz Night.',
            is_read=False,
            created_at=None,
            updated_at=None
        ),
        Notification(
            notification_id=4,
            recipient_id=4,
            recipient_type='guest',
            event_id=4,
            notification_type='attendance_rejected',
            message='Bob Brown, your request for Summer Festival was not accepted.',
            is_read=False,
            created_at=None,
            updated_at=None
        ),
        Notification(
            notification_id=5,
            recipient_id=5,
            recipient_type='guest',
            event_id=1,
            notification_type='request_received',
            message='Carol White, we have received your request for Rocking the City.',
            is_read=False,
            created_at=None,
            updated_at=None
        ),
        Notification(
            notification_id=6,
            recipient_id=1,
            recipient_type='band',
            event_id=1,
            notification_type='event_created',
            message='White Noise, your event Rocking the City has been successfully created.',
            is_read=False,
            created_at=None,
            updated_at=None
        ),
        Notification(
            notification_id=7,
            recipient_id=2,
            recipient_type='band',
            event_id=3,
            notification_type='song_request',
            message='The Rockers, a new song request has been made for The Big Apple Concert.',
            is_read=False,
            created_at=None,
            updated_at=None
        ),
        Notification(
            notification_id=8,
            recipient_id=3,
            recipient_type='band',
            event_id=5,
            notification_type='event_full',
            message='The Jazzmen, your event Autumn Jazz Festival is now fully booked.',
            is_read=False,
            created_at=None,
            updated_at=None
        ),
        Notification(
            notification_id=9,
            recipient_id=1,
            recipient_type='band',
            event_id=4,
            notification_type='song_request',
            message='White Noise, a new song request has been made for Summer Festival.',
            is_read=False,
            created_at=None,
            updated_at=None
        ),
        Notification(
            notification_id=10,
            recipient_id=2,
            recipient_type='band',
            event_id=3,
            notification_type='event_updated',
            message='The Rockers, the schedule for The Big Apple Concert has been updated.',
            is_read=False,
            created_at=None,
            updated_at=None
        ),
    ]
    
    # Check if the number of results is as expected
    assert len(results) == len(expected_notifications)
    
    # Compare individual attributes of each notification
    for result, expected_notification in zip(results, expected_notifications):
        assert result.notification_id == expected_notification.notification_id
        assert result.recipient_id == expected_notification.recipient_id
        assert result.recipient_type == expected_notification.recipient_type
        assert result.event_id == expected_notification.event_id
        assert result.notification_type == expected_notification.notification_type
        assert result.message == expected_notification.message
        assert result.is_read == expected_notification.is_read
        
        # Optionally, compare timestamps with some tolerance
        if expected_notification.created_at:
            assert abs((result.created_at - expected_notification.created_at).total_seconds()) < 1
        else:
            assert result.created_at is None
        
        if expected_notification.updated_at:
            assert abs((result.updated_at - expected_notification.updated_at).total_seconds()) < 1
        else:
            assert result.updated_at is None

def test_create_notification(db_connection):
    db_connection.seed("../seeds/notifications_table_test_data.sql")
    
    # Create an instance of NotificationRepository
    notification_repo = NotificationRepository(db_connection)
    
    # Create a new Notification object
    new_notification = Notification(
        recipient_id=1,
        recipient_type='guest',
        event_id=2,
        notification_type='song_request',
        message='Your song has been added to the playlist!',
        is_read=False
    )
    
    # Insert the new notification into the database
    notification_repo.create(new_notification)
    found_notification = notification_repo.find(11)  # Assuming ID 11 is the new notification
    assert found_notification.notification_id == 11
    assert found_notification.recipient_id == 1
    assert found_notification.recipient_type == 'guest'
    assert found_notification.event_id == 2
    assert found_notification.notification_type == 'song_request'
    assert found_notification.message == 'Your song has been added to the playlist!'
    assert found_notification.is_read is False

def test_delete_notification(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/notifications_table_test_data.sql")
    
    # Create an instance of NotificationRepository
    notification_repo = NotificationRepository(db_connection)
    
    # Verify the notification exists before deletion
    notification_to_delete = notification_repo.find(1)
    assert notification_to_delete is not None
    
    # Perform the delete operation
    notification_repo.delete(1)
    
    # Verify the notification no longer exists
    deleted_notification = notification_repo.find(1)
    assert deleted_notification is None
