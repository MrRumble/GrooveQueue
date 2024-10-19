import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import LoggedInAs from '../LoggedInAsComponent/LoggedInAsComponent'; // Import the LoggedInAs component
import './Navbar.css'; // Import the CSS file

const Navbar = () => {
    const navigate = useNavigate();
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        // Check if there is a valid token for guest or band
        const guestToken = localStorage.getItem('access_token');
        const bandToken = localStorage.getItem('band_access_token');

        // If either token is present, set the user as logged in
        if (guestToken || bandToken) {
            setIsLoggedIn(true);
        } else {
            setIsLoggedIn(false);
        }
    }, []); // Runs once on component mount

    const handleLogout = async () => {
        const guestToken = localStorage.getItem('access_token'); 
        const bandToken = localStorage.getItem('band_access_token'); // Adjust this based on your actual token naming

        // Determine which token is present and call the appropriate logout API
        try {
            if (guestToken) {
                await fetch('http://localhost:5001/guest/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token: guestToken }), // Send the guest token
                });

                // Clear guest data from local storage
                localStorage.clear();
            } else if (bandToken) {
                await fetch('http://localhost:5001/band/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token: bandToken }), // Send the band token
                });

                // Clear band data from local storage
                localStorage.clear();
            }

            // Redirect to login page
            navigate('/');
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return (
        <nav className="navbar">
            <ul className="nav-list">
                {/* Links that are always visible */}
                <li className="nav-item"><Link className="nav-link" to="/signup">Sign Up</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/loginguest">Login Guest</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/loginband">Login Band</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/events">View All Events</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/notifications">Notifications</Link></li>

                {/* Show 'My Band' only if a band is logged in */}
                {isLoggedIn && localStorage.getItem('band_access_token') && (
                    <li className="nav-item"><Link className="nav-link" to="/band-homepage">My Band</Link></li>
                )}

                {/* Show LoggedInAs component only if a user is logged in */}
                {isLoggedIn && (
                    <li className="nav-item">
                        <LoggedInAs /> {/* Show the logged-in user */}
                    </li>
                )}
            </ul>
        </nav>
    );
};

export default Navbar;
