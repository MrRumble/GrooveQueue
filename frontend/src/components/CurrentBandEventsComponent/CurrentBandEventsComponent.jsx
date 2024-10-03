import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate for navigation
import Navbar from '../../components/Navbar/Navbar'; // Assuming you have a Navbar component

const CurrentBandEvents = () => {
    const [events, setEvents] = useState([]);     // State to hold events
    const [bandName, setBandName] = useState(''); // State to hold the band's name
    const [loading, setLoading] = useState(true); // State to show loading status
    const [error, setError] = useState(null);     // State to handle errors

    const navigate = useNavigate(); // Initialize navigate

    // Fetch events and band name when the component mounts
    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const response = await fetch('http://localhost:5001/bands/current/events', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // Assuming token is stored in localStorage
                    },
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch events');
                }

                const data = await response.json();
                setBandName(data.band_name); // Set the band's name from the response
                setEvents(data.events);      // Set the fetched events to state
                console.log(data.events); // Log fetched events
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchEvents(); // Call the function to fetch events and band name
    }, []); // Empty dependency array ensures this effect runs only once (on mount)

    if (loading) return <div>Loading events...</div>;
    if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

    // Function to handle navigation to the update event component
    const handleUpdateEvent = (eventId) => {
        console.log('Navigating to update event:', eventId); // Debug log
        navigate(`/update-event/${eventId}`); // Navigate to update event route with event ID
    };

    return (
        <div>
            <Navbar /> {/* Include the Navbar component */}
            <div className="current-band-events">
                <h1>{bandName ? `${bandName}'s Events` : "Your Band's Events"}</h1> {/* Display the band's name */}
                {events.length > 0 ? (
                    <ul>
                        {events.map(event => (
                            <li key={event.id} className="event-item">
                                <h2>{event.event_name}</h2>
                                <p><strong>Location:</strong> {event.location}</p>
                                <p><strong>Start:</strong> {new Date(event.event_start).toLocaleString()}</p>
                                <p><strong>End:</strong> {new Date(event.event_end).toLocaleString()}</p>
                                <p><strong>QR Code:</strong> {event.qr_code_content}</p>
                                <button onClick={() => handleUpdateEvent(event.event_id)}>Update Event</button> {/* Update Event Button */}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No events found for your band.</p>
                )}
            </div>
        </div>
    );
};

export default CurrentBandEvents;
