import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Import Link for navigation and useNavigate for redirection
import Navbar from '../../components/Navbar/Navbar';

const BandHomepage = () => {
    const [bandDetails, setBandDetails] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate(); // For programmatic navigation

    useEffect(() => {
        const fetchBandDetails = async () => {
            const token = localStorage.getItem('access_token'); // Use the correct key for your token

            if (!token) {
                setError("No token found. Please log in.");
                setLoading(false);
                return;
            }

            try {
                // Fetch band details from the API
                const response = await fetch('http://localhost:5001/band/current', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}` // Attach the token for authentication
                    }
                });

                if (!response.ok) {
                    // If the token is invalid or blacklisted, handle the error
                    throw new Error("Invalid or blacklisted token. Please log in again.");
                }

                const data = await response.json();
                setBandDetails(data);
            } catch (err) {
                setError(err.message);
                // Optionally clear the token if unauthorized
                localStorage.removeItem('access_token'); // Clear the token
                navigate('/loginband'); // Redirect to login page
            } finally {
                setLoading(false);
            }
        };

        fetchBandDetails();
    }, [navigate]);

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

                    {/* Link to the Current Band Events page */}
                    <Link to="/current-band-events" style={{ marginLeft: '10px' }}>
                        <button>View {bandDetails.band_name}'s Events</button>
                    </Link>
                </div>
            ) : (
                <p>No band details available.</p>
            )}
        </div>
    );
};

export default BandHomepage;
