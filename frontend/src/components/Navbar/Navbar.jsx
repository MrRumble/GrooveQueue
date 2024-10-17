import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css'; // Import the CSS file

const Navbar = () => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        const guestToken = localStorage.getItem('access_token'); // Adjust this based on your actual token naming
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
                <li className="nav-item"><Link className="nav-link" to="/signupguest">Sign Up Guest</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/signupband">Sign Up Band</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/loginguest">Login Guest</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/loginband">Login Band</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/band-homepage">My Band</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/events">View All Events</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/notifications">Notifications</Link></li> {/* New Link for Notifications */}
                <li className="nav-item"><button className="logout-button" onClick={handleLogout}>Logout</button></li>
            </ul>
        </nav>
    );
};

export default Navbar;
