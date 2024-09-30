import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // To retrieve the event ID from the URL
import Navbar from '../../components/Navbar/Navbar'; // Assuming you have a Navbar component

const EventDetails = () => {
    const { eventId } = useParams(); // Extract the event ID from the URL
    const [event, setEvent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchEvent = async () => {
            try {
                const response = await fetch(`http://localhost:5001/events/${eventId}`, { // Update with your backend URL
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch event');
                }

                const data = await response.json();
                setEvent(data); // Assuming your API returns an event object
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchEvent();
    }, [eventId]); // Re-run the effect if eventId changes

    if (loading) return <div>Loading event details...</div>;
    if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

    return (
        <div>
            <Navbar />
            {event ? (
                <div className="event-details">
                    <h1>{event.event_name}</h1>
                    <p><strong>Location:</strong> {event.location}</p>
                    <p><strong>Start:</strong> {new Date(event.event_start).toLocaleString()}</p>
                    <p><strong>End:</strong> {new Date(event.event_end).toLocaleString()}</p>
                    <p><strong>QR Code Content:</strong> {event.qr_code_content}</p>
                    <p><strong>Band Name:</strong> {event.band_name}</p> {/* Display band name here */}
                </div>
            ) : (
                <p>No event details available.</p>
            )}
        </div>
    );
};

export default EventDetails;
