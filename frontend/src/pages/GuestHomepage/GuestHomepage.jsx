import React, { useEffect, useState } from 'react';
import {jwtDecode} from 'jwt-decode'; // Import jwt-decode
import Navbar from '../../components/Navbar/Navbar';

const GuestHomepage = () => {
    const [userDetails, setUserDetails] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('access_token'); // Use the correct key for your token

        if (!token) {
            setError("No token found. Please log in.");
            setLoading(false);
            return;
        }

        try {
            // Decode the token to get user details
            const decodedToken = jwtDecode(token);
            setUserDetails({
                name: decodedToken.name,
                email: decodedToken.email,
                id: decodedToken.guest_id,
            });
        } catch (err) {
            setError("Invalid token. Please log in again.");
        } finally {
            setLoading(false);
        }
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

    return (
        <div>
            <Navbar />
            <h1>Welcome to the Guest Homepage!</h1>
            {userDetails ? (
                <div>
                    <h2>User Details:</h2>
                    <p><strong>Name:</strong> {userDetails.name}</p>
                    <p><strong>Email:</strong> {userDetails.email}</p>
                    <p><strong>User ID:</strong> {userDetails.id}</p>
                </div>
            ) : (
                <p>No user details available.</p>
            )}
        </div>
    );
};

export default GuestHomepage;
