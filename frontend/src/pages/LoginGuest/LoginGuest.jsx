import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';

const LoginGuest = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null); // State to manage error messages

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        // Check if there's a logged-in band session
        const existingUserType = localStorage.getItem('userType');
        if (existingUserType === 'band') {
            // Clear existing session data for band
            localStorage.removeItem('access_token');
        }

        // Set the user type to guest
        localStorage.setItem('userType', 'guest');

        try {
            const response = await fetch('http://localhost:5001/guests/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const { error } = await response.json();
                throw new Error(error); // Throw an error if response is not ok
            }

            const data = await response.json();
            console.log('Login successful:', data);
            localStorage.setItem('access_token', data.access_token);
            navigate('/guest-homepage');

        } catch (error) {
            setError(error.message); // Update error state with the error message
            console.error('Login failed:', error);
        }
    };

    return (
        <div>
            <Navbar />
            <h2>Login</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error message */}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email:</label>
                    <input 
                        type="email" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input 
                        type="password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                    />
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default LoginGuest;
