import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Import Link and useNavigate for navigation
import Navbar from '../../components/Navbar/Navbar'; // Adjust the import path as necessary
import './NotificationsPage.css'; // Import the CSS file

const NotificationsPage = () => {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate(); // Initialize useNavigate for programmatic navigation

    useEffect(() => {
        const fetchNotifications = async () => {
            const token = localStorage.getItem('access_token'); // Use the correct key for your token

            if (!token) {
                setError("No token found. Please log in.");
                setLoading(false);
                return;
            }

            try {
                const response = await fetch('http://localhost:5001/notifications', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    const errorMessage = await response.json();
                    throw new Error(errorMessage.error || 'Failed to fetch notifications');
                }

                const data = await response.json();
                setNotifications(data.notifications || []); // Handle case where notifications might be undefined
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchNotifications();
    }, []);

    const handleNotificationClick = async (notification) => {
        // Mark notification as read
        await markNotificationAsRead(notification.notification_id);

        if (notification.notification_type === 'attendance_accepted') {
            navigate(`/events/${notification.event_id}/requests`); // Navigate to the event page
        }
    };

    const markNotificationAsRead = async (notificationId) => {
        const token = localStorage.getItem('access_token'); // Use the correct key for your token

        try {
            const response = await fetch(`http://localhost:5001/notifications/${notificationId}/read`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                const errorMessage = await response.json();
                throw new Error(errorMessage.error || 'Failed to mark notification as read');
            }

            // Optionally, you can update the state to reflect that the notification is read
            setNotifications((prev) =>
                prev.map((notif) =>
                    notif.notification_id === notificationId ? { ...notif, is_read: true } : notif
                )
            );
        } catch (err) {
            console.error(err.message);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

    return (
        <div className="notifications-container">
            <Navbar />
            <h1>Notifications</h1>
            {notifications.length === 0 ? (
                <p>No notifications available.</p>
            ) : (
                <ul className="notifications-list">
                    {notifications.map((notification) => (
                        <li
                            key={notification.notification_id}
                            className="notification-item"
                            onClick={() => handleNotificationClick(notification)}
                        >
                            <p className="notification-message">{notification.message}</p>
                            <p className="notification-status">
                                Status: {notification.is_read ? 'Read' : 'Unread'}
                            </p>
                        </li>
                    ))}
                </ul>
            )}
            <Link to="/">
                <button>Go to Homepage</button>
            </Link>
        </div>
    );
};

export default NotificationsPage;
