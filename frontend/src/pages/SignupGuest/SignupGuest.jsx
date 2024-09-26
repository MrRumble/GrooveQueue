import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Step 1: Import useNavigate

const SignUpGuest = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [oauthProvider, setOauthProvider] = useState('');
    const [oauthProviderId, setOauthProviderId] = useState('');
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');

    const navigate = useNavigate(); // Step 2: Use useNavigate to get navigate function

    const handleSubmit = async (e) => {
        e.preventDefault();

        const guestData = {
            name,
            email,
            password,
            oauth_provider: oauthProvider,
            oauth_provider_id: oauthProviderId,
        };

        try {
            const response = await fetch('http://localhost:5001/guests', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(guestData),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Something went wrong!');
            }

            setMessage(data.message);
            setError(''); // Clear any previous error

            // Optionally reset the form fields
            setName('');
            setEmail('');
            setPassword('');
            setOauthProvider('');
            setOauthProviderId('');

            // Step 3: Navigate to the login page after successful sign up
            navigate('/loginguest');

        } catch (err) {
            setError(err.message);
            setMessage(''); // Clear any previous message
        }
    };

    return (
        <div>
            <h2>Sign Up as a Guest</h2>
            <form onSubmit={handleSubmit} noValidate>
                <div>
                    <label>Name:</label>
                    <input 
                        type="text" 
                        value={name} 
                        onChange={(e) => setName(e.target.value)} 
                        required 
                    />
                </div>
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
                <button type="submit">Sign Up</button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {message && <p style={{ color: 'green' }}>{message}</p>}
        </div>
    );
};

export default SignUpGuest;
