import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';
import './BandHomepage.css'; 

const BandHomepage = () => {
    const [bandDetails, setBandDetails] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchBandDetails = async () => {
            const token = localStorage.getItem('access_token');

            if (!token) {
                setError("No token found. Please log in.");
                setLoading(false);
                return;
            }

            try {
                const response = await fetch('http://localhost:5001/band/current', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error("Invalid or blacklisted token. Please log in again.");
                }

                const data = await response.json();
                setBandDetails(data);
            } catch (err) {
                setError(err.message);
                localStorage.removeItem('access_token');
                navigate('/loginband');
            } finally {
                setLoading(false);
            }
        };

        fetchBandDetails();
    }, [navigate]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

    return (
        <div className="band-homepage-container"> {/* Use the specific class */}
            <Navbar />
            <h1 className="band-homepage-title">Welcome to the Band Homepage!</h1>
            {bandDetails ? (
                <div>
                    <h2 className="band-homepage-details">Band Details:</h2>
                    {bandDetails.profile_picture_path && (
                        <img 
                            className="band-homepage-image"  // Use the specific class
                            src={bandDetails.profile_picture_path} 
                            alt={`${bandDetails.band_name} Profile`} 
                        />
                    )}
                    <p><strong>Band Name:</strong> {bandDetails.band_name}</p>
                    <p><strong>Band Email:</strong> {bandDetails.band_email}</p>
                    

                    <Link to="/create-event">
                        <button className="band-homepage-button">Create New Event</button> {/* Use the specific class */}
                    </Link>

                    <Link to="/current-band-events" style={{ marginLeft: '10px' }}>
                        <button className="band-homepage-button">View {bandDetails.band_name}'s Events</button> {/* Use the specific class */}
                    </Link>
                </div>
            ) : (
                <p>No band details available.</p>
            )}
        </div>
    );
};

export default BandHomepage;
