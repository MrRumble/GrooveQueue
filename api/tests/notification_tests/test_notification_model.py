import unittest
from datetime import datetime, timedelta
from api.notifications.notification_model import Notification

class TestNotificationModel(unittest.TestCase):

    def setUp(self):
        # This runs before each test method
        self.notification1 = Notification(
            notification_id=1,
            recipient_id=101,
            recipient_type='guest',
            event_id=201,
            notification_type='song_request',
            message='Your song request for Event 201 has been received.',
            is_read=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.notification2 = Notification(
            notification_id=2,
            recipient_id=102,
            recipient_type='band',
            event_id=202,
            notification_type='event_created',
            message='Your event has been successfully created.',
            is_read=False,
            created_at=datetime.now() - timedelta(days=1),  # Older created_at date
            updated_at=datetime.now() - timedelta(days=1)
        )

    def test_notification_creation(self):
        """Test that notifications are created with correct values."""
        self.assertEqual(self.notification1.notification_id, 1)
        self.assertEqual(self.notification1.recipient_id, 101)
        self.assertEqual(self.notification1.recipient_type, 'guest')
        self.assertEqual(self.notification1.event_id, 201)
        self.assertEqual(self.notification1.notification_type, 'song_request')
        self.assertEqual(self.notification1.message, 'Your song request for Event 201 has been received.')
        self.assertFalse(self.notification1.is_read)

    def test_notification_equality(self):
        """Test that two notifications with the same data are considered equal."""
        notification_copy = Notification(
            notification_id=1,
            recipient_id=101,
            recipient_type='guest',
            event_id=201,
            notification_type='song_request',
            message='Your song request for Event 201 has been received.',
            is_read=False,
            created_at=self.notification1.created_at,
            updated_at=self.notification1.updated_at
        )
        
        # Both notifications should be equal
        self.assertEqual(self.notification1, notification_copy)

    def test_notification_not_equal(self):
        """Test that two notifications with different data are not considered equal."""
        self.assertNotEqual(self.notification1, self.notification2)

    def test_to_dict(self):
        """Test that notification can be converted to a dictionary properly."""
        notification_dict = self.notification1.to_dict()
        
        self.assertEqual(notification_dict['notification_id'], 1)
        self.assertEqual(notification_dict['recipient_id'], 101)
        self.assertEqual(notification_dict['recipient_type'], 'guest')
        self.assertEqual(notification_dict['event_id'], 201)
        self.assertEqual(notification_dict['notification_type'], 'song_request')
        self.assertEqual(notification_dict['message'], 'Your song request for Event 201 has been received.')
        self.assertFalse(notification_dict['is_read'])
        self.assertIsInstance(notification_dict['created_at'], str)  # ISO string
        self.assertIsInstance(notification_dict['updated_at'], str)  # ISO string

    def test_is_read_default(self):
        """Test that is_read defaults to False when not provided."""
        notification = Notification(
            notification_id=3,
            recipient_id=103,
            recipient_type='guest',
            event_id=203,
            notification_type='attendance_accepted',
            message='Your attendance has been accepted.'
        )
        self.assertFalse(notification.is_read)

    def test_created_at_auto_set(self):
        """Test that created_at is auto-set to current time if not provided."""
        notification = Notification(
            notification_id=4,
            recipient_id=104,
            recipient_type='band',
            event_id=204,
            notification_type='event_updated',
            message='Your event has been updated.'
        )
        self.assertIsInstance(notification.created_at, datetime)
        self.assertAlmostEqual(notification.created_at, datetime.now(), delta=timedelta(seconds=1))

