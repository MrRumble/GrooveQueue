import React, { useEffect, useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import { Link, useNavigate } from 'react-router-dom';
import './LoggedInAs.css'; // Add your custom styles here

const LoggedInAs = () => {
    const [userType, setUserType] = useState(null);
    const [userName, setUserName] = useState(null);
    const [showDropdown, setShowDropdown] = useState(false);
    const [loading, setLoading] = useState(false); // Loading state
    const [errorMessage, setErrorMessage] = useState(null); // Error message
    const [notificationCount, setNotificationCount] = useState(0); // State for notification count
    const navigate = useNavigate(); // useNavigate hook to redirect users

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        
        if (token) {
            try {
                const decodedToken = jwtDecode(token);
                const { role } = decodedToken;

                if (role === 'guest') {
                    setUserName(decodedToken.name);
                    setUserType('Guest');
                } else if (role === 'band') {
                    setUserName(decodedToken.band_name);
                    setUserType('Band');
                }
            } catch (error) {
                console.error('Invalid token:', error);
            }
        }
    }, []);

    // Fetch the notification count
    useEffect(() => {
        const fetchNotificationCount = async () => {
            const token = localStorage.getItem('access_token');

            if (!token) return;

            try {
                const response = await fetch('http://localhost:5001/notifications/count', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setNotificationCount(data.count); // Update the notification count state
                } else {
                    console.error('Failed to fetch notification count');
                }
            } catch (error) {
                console.error('Error fetching notification count:', error);
            }
        };

        fetchNotificationCount();
    }, [userName]); // Fetch the count again if the userName changes

    const handleDropdownToggle = () => {
        setShowDropdown(!showDropdown);
    };

    const handleLogout = async () => {
        setLoading(true); // Set loading state to true
        setErrorMessage(null); // Clear any previous error message

        try {
            // Use localhost URL for the API
            const apiUrl = userType === 'Guest' ? 'http://localhost:5001/guest/logout' : 'http://localhost:5001/band/logout';
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                },
            });

            if (response.ok) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('userType');
                navigate('/'); // Redirect to home after logout
            } else {
                setErrorMessage('Logout failed. Please try again.'); // Set error message
                console.error('Logout failed:', response.statusText);
            }
        } catch (error) {
            setErrorMessage('Error during logout.'); // Set error message
            console.error('Error during logout:', error);
        } finally {
            setLoading(false); // Reset loading state
        }
    };

    return (
        <div className="logged-in-container">
            {userName && userType ? (
                <div className="logged-in-as">
                    <div className="avatar-circle" onClick={handleDropdownToggle}>
                        {userName.charAt(0).toUpperCase()}
                        {/* Display notification count as a badge */}
                        {notificationCount > 0 && (
                            <span className="notification-badge">{notificationCount}</span>
                        )}
                    </div>
                    {showDropdown && (
                        <div className="dropdown-menu">
                            <p>
                                Logged in as: <strong>{userName}</strong> ({userType})
                            </p>
                            <ul>
                                <li><Link to="/notifications">Notifications</Link></li>
                                <li><Link to="/band-homepage">Profile</Link></li>
                                <li><Link to="/settings">Settings</Link></li>
                                <li onClick={handleLogout}>
                                    {loading ? 'Logging out...' : 'Logout'}
                                </li>
                            </ul>
                            {errorMessage && <p className="error-message">{errorMessage}</p>} {/* Display error message */}
                        </div>
                    )}
                </div>
            ) : (
                <p>Not logged in</p>
            )}
        </div>
    );
};

export default LoggedInAs;
