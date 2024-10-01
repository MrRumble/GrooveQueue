import React, { useEffect, useState } from 'react';
import Navbar from '../../components/Navbar/Navbar'; // Assuming you have a Navbar component

const CurrentBandEvents = () => {
    const [events, setEvents] = useState([]);     // State to hold events
    const [loading, setLoading] = useState(true); // State to show loading status
    const [error, setError] = useState(null);     // State to handle errors

    // Fetch events when the component mounts
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
                setEvents(data); // Set the fetched events to state
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchEvents(); // Call the function to fetch events
    }, []); // Empty dependency array ensures this effect runs only once (on mount)

    if (loading) return <div>Loading events...</div>;
    if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

    return (
        <div>
            <Navbar /> {/* Include the Navbar component */}
            <div className="current-band-events">
                <h1>Your Band's Events</h1>
                {events.length > 0 ? (
                    <ul>
                        {events.map(event => (
                            <li key={event.id} className="event-item">
                                <h2>{event.event_name}</h2>
                                <p><strong>Location:</strong> {event.location}</p>
                                <p><strong>Start:</strong> {new Date(event.event_start).toLocaleString()}</p>
                                <p><strong>End:</strong> {new Date(event.event_end).toLocaleString()}</p>
                                <p><strong>QR Code:</strong> {event.qr_code_content}</p>
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
