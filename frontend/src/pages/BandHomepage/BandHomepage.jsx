import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link for navigation
import Navbar from '../../components/Navbar/Navbar';

const BandHomepage = () => {
    const [bandDetails, setBandDetails] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchBandDetails = async () => {
            const token = localStorage.getItem('access_token'); // Use the correct key for your token

            if (!token) {
                setError("No token found. Please log in.");
                setLoading(false);
                return;
            }

            try {
                const response = await fetch('http://localhost:5001/band/current', { // Ensure the endpoint matches your server
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch band details');
                }

                const data = await response.json();
                setBandDetails(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        
        fetchBandDetails();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

    return (
        <div>
            <Navbar />
            <h1>Welcome to the Band Homepage!</h1>
            {bandDetails ? (
                <div>
                    <h2>Band Details:</h2>
                    <p><strong>Band Name:</strong> {bandDetails.band_name}</p>
                    <p><strong>Band Email:</strong> {bandDetails.band_email}</p>
                    <p><strong>Band ID:</strong> {bandDetails.band_id}</p>

                    {/* Link to the Create New Event page */}
                    <Link to="/create-event">
                        <button>Create New Event</button>
                    </Link>
                </div>
            ) : (
                <p>No band details available.</p>
            )}
        </div>
    );
};

export default BandHomepage;
