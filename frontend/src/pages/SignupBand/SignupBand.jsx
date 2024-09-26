import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SignUpBand = () => {
    const [bandName, setBandName] = useState('');
    const [bandEmail, setBandEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(''); // State to manage error messages
    const [message, setMessage] = useState(''); // State to manage success messages

    const navigate = useNavigate(); // Step 2: Use useNavigate to get navigate function

    const handleSubmit = async (e) => {
        e.preventDefault();

        const bandData = {
            band_name: bandName,
            band_email: bandEmail,
            password,
        };

        try {
            const response = await fetch('http://localhost:5001/bands', { // Ensure the endpoint matches your server
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bandData),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Something went wrong!');
            }

            setMessage(data.message);
            setError(''); // Clear any previous error

            // Optionally reset the form fields
            setBandName('');
            setBandEmail('');
            setPassword('');

            // Step 3: Navigate to the band homepage after successful sign up
            navigate('/loginband');

        } catch (err) {
            setError(err.message);
            setMessage(''); // Clear any previous message
        }
    };

    return (
        <div>
            <h2>Sign Up as a Band</h2>
            <form onSubmit={handleSubmit} noValidate>
                <div>
                    <label>Band Name:</label>
                    <input 
                        type="text" 
                        value={bandName} 
                        onChange={(e) => setBandName(e.target.value)} 
                        required 
                    />
                </div>
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
                <button type="submit">Sign Up</button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {message && <p style={{ color: 'green' }}>{message}</p>}
        </div>
    );
};

export default SignUpBand;
