import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SignUpBand = () => {
    const [bandName, setBandName] = useState('');
    const [bandEmail, setBandEmail] = useState('');
    const [password, setPassword] = useState('');
    const [profilePicture, setProfilePicture] = useState(null); // State for profile picture
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData(); // Create a FormData object
        formData.append('band_name', bandName);
        formData.append('band_email', bandEmail);
        formData.append('password', password);
        if (profilePicture) {
            formData.append('profile_picture', profilePicture); // Append the file
        }

        try {
            const response = await fetch('http://localhost:5001/bands', {
                method: 'POST',
                body: formData, // Send the FormData object
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Something went wrong!');
            }

            setMessage(data.message);
            setError('');

            setBandName('');
            setBandEmail('');
            setPassword('');
            setProfilePicture(null); // Clear the profile picture input

            navigate('/loginband');

        } catch (err) {
            setError(err.message);
            setMessage('');
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
                <div>
                    <label>Profile Picture:</label>
                    <input 
                        type="file" 
                        accept="image/*" 
                        onChange={(e) => setProfilePicture(e.target.files[0])} // Get the file
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
