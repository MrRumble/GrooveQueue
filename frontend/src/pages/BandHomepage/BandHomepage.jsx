import React, { useEffect, useState } from 'react';
import {jwtDecode} from 'jwt-decode'; // Import jwt-decode
import { Link } from 'react-router-dom'; // Import Link for navigation
import Navbar from '../../components/Navbar/Navbar';

const BandHomepage = () => {
    const [bandDetails, setBandDetails] = useState(null);
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
            // Decode the token to get band details
            const decodedToken = jwtDecode(token);
            setBandDetails({
                band_name: decodedToken.band_name,
                band_email: decodedToken.band_email,
                band_id: decodedToken.band_id,
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
