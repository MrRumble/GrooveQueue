import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link for navigation
import Navbar from '../../components/Navbar/Navbar'; // Adjust the import path as necessary

const NotificationsPage = () => {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

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

    if (loading) return <div>Loading...</div>;
    if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

    return (
        <div>
            <Navbar />
            <h1>Notifications</h1>
            {notifications.length === 0 ? (
                <p>No notifications available.</p>
            ) : (
                <ul>
                    {notifications.map((notification) => (
                        <li key={notification.notification_id}>
                            <p>{notification.message}</p>
                            <p>Status: {notification.is_read ? 'Read' : 'Unread'}</p>
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
