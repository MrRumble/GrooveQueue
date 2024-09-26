import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        const token = localStorage.getItem('access_token');

        // Call the logout API to revoke the token on the server
        if (token) {
            try {
                await fetch('http://localhost:5001/guest/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token }), // Send the token in the request body
                });

                // Clear any user data from local storage
                localStorage.removeItem('access_token');
                localStorage.removeItem('email');
                localStorage.removeItem('user_id');

                // Redirect to login page
                navigate('/loginguest');
            } catch (error) {
                console.error('Logout failed:', error);
            }
        } else {
            // If there's no token, just navigate to the login page
            navigate('/');
        }
    };

    return (
        <nav>
            <ul>
                <li><Link to="/signupguest">Sign Up Guest</Link></li>
                <li><Link to="/signupband">Sign Up Band</Link></li>
                <li><Link to="/loginguest">Login Guest</Link></li>
                <li><Link to="/loginband">Login Band</Link></li>
                <li><button onClick={handleLogout}>Logout</button></li>
            </ul>
        </nav>
    );
};

export default Navbar;
