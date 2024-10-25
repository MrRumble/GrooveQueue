import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Import Link for navigation and useNavigate for redirection
import Navbar from '../../components/Navbar/Navbar';

const GuestHomepage = () => {
    const [userDetails, setUserDetails] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate(); // For programmatic navigation

    useEffect(() => {
        const fetchGuestDetails = async () => {
            const token = localStorage.getItem('access_token'); // Use the correct key for your token

            if (!token) {
                setError("No token found. Please log in.");
                setLoading(false);
                return;
            }

            try {
                // Fetch current guest details from the API
                const response = await fetch('http://localhost:5001/guest/current', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`, // Include the token in the Authorization header
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    // If the token is invalid or blacklisted, handle the error
                    throw new Error("Invalid or blacklisted token. Please log in again.");
                }

                const data = await response.json();
                setUserDetails(data); // Assuming the response is already in the required format
            } catch (err) {
                setError(err.message || "An error occurred while fetching guest details.");
                // Optionally clear the token if unauthorized
                localStorage.removeItem('access_token'); // Clear the token
                navigate('/loginguest'); // Redirect to login page
            } finally {
                setLoading(false);
            }
        };

        fetchGuestDetails();
    }, [navigate]);

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

                    {/* You can add more links here for navigation if needed */}
                    {/* Example of adding a link to view events */}
                    <Link to="/view-events">
                        <button>View Events</button>
                    </Link>
                </div>
            ) : (
                <p>No user details available.</p>
            )}
        </div>
    );
};

export default GuestHomepage;
