import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginBand = () => {
    const [bandEmail, setBandEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null); // State to manage error messages

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null); 
        
        try {
            const response = await fetch('http://localhost:5001/bands/login', { // Ensure the endpoint matches your server
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
            localStorage.setItem('band_email', data.band_email);
            localStorage.setItem('band_id', data.band_id);
            navigate('/band-homepage'); // Navigate to the band's homepage after successful login

        } catch (error) {
            setError(error.message); // Update error state with the error message
            console.error('Login failed:', error);
        }
    };

    return (
        <div>
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
