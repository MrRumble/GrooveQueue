import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';

const LoginBand = () => {
    const [bandEmail, setBandEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null); // State to manage error messages

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        // Check if there's a logged-in guest session
        const existingUserType = localStorage.getItem('userType');
        if (existingUserType === 'guest') {
            // Clear existing session data for guest
            localStorage.removeItem('access_token');
            localStorage.removeItem('email');
            localStorage.removeItem('user_id');
        }

        // Set the user type to band
        localStorage.setItem('userType', 'band');

        try {
            const response = await fetch('http://localhost:5001/bands/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ band_email: bandEmail, password }), // Note the field names
            });

            if (!response.ok) {
                const { error } = await response.json();
                throw new Error(error); // Throw an error if response is not ok
            }

            const data = await response.json();
            console.log('Login successful:', data);
            localStorage.setItem('access_token', data.access_token);
            navigate('/band-homepage'); // Navigate to the band's homepage after successful login

        } catch (error) {
            setError(error.message); // Update error state with the error message
            console.error('Login failed:', error);
        }
    };

    return (
        <div>
            <Navbar />
            <h2>Band Login</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error message */}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Band Email:</label>
                    <input 
                        type="email" 
                        value={bandEmail} 
                        onChange={(e) => setBandEmail(e.target.value)} 
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

export default LoginBand;
