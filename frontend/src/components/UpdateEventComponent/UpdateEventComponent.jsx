import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';
import { jwtDecode } from 'jwt-decode'; // Import the jwt-decode library

const UpdateEvent = () => {
    const [eventName, setEventName] = useState('');
    const [location, setLocation] = useState('');
    const [eventStart, setEventStart] = useState('');
    const [eventEnd, setEventEnd] = useState('');
    const [qrCodeContent, setQrCodeContent] = useState('');
    const [maxRequests, setMaxRequests] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const navigate = useNavigate();
    const { eventId } = useParams(); // Get the event ID from the URL

    // Check if the user is logged in
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            navigate('/loginband'); // Redirect to login if not authenticated
        }
    }, [navigate]);

    useEffect(() => {
        // Fetch the current event details
        const fetchEventDetails = async () => {
            const token = localStorage.getItem('access_token');

            try {
                const response = await fetch(`http://localhost:5001/events/${eventId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });

                if (!response.ok) {
                    const { error } = await response.json();
                    throw new Error(error || 'Failed to fetch event details');
                }

                const eventData = await response.json();
                setEventName(eventData.event_name);
                setLocation(eventData.location);
                setEventStart(eventData.event_start);
                setEventEnd(eventData.event_end);
                setQrCodeContent(eventData.qr_code_content || '');
                setMaxRequests(eventData.max_requests_per_user || '');
            } catch (err) {
                setError(err.message);
            }
        };

        fetchEventDetails();
    }, [eventId]);

    const handleDelete = async () => {
        const token = localStorage.getItem('access_token');

        if (!token) {
            setError("You must be logged in to delete an event.");
            return;
        }

        try {
            const response = await fetch(`http://localhost:5001/events/${eventId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                const { error } = await response.json();
                throw new Error(error || 'Failed to delete event');
            }

            setSuccess('Event deleted successfully!');
            navigate('/band-homepage'); // Redirect after success
        } catch (err) {
            setError(err.message);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        const token = localStorage.getItem('access_token');

        if (!token) {
            setError("You must be logged in to update an event.");
            return;
        }

        try {
            // Decode the token to extract band_id
            const decodedToken = jwtDecode(token);
            const bandId = decodedToken.sub; // Ensure 'band_id' matches the key in your token

            const response = await fetch(`http://localhost:5001/events/${eventId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    event_name: eventName,
                    location: location,
                    event_start: eventStart,
                    event_end: eventEnd,
                    qr_code_content: qrCodeContent,
                    max_requests_per_user: parseInt(maxRequests, 10) || null, // Ensure it's an integer
                    band_id: bandId // Include band_id in the request body
                }),
            });

            if (!response.ok) {
                const { error } = await response.json();
                throw new Error(error || 'Failed to update event');
            }

            setSuccess('Event updated successfully!');
            navigate('/band-homepage'); // Redirect after success
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div>
            <Navbar />
            <h1>Update Event</h1>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {success && <p style={{ color: 'green' }}>{success}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Event Name:</label>
                    <input
                        type="text"
                        value={eventName}
                        onChange={(e) => setEventName(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Location:</label>
                    <input
                        type="text"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Event Start:</label>
                    <input
                        type="datetime-local"
                        value={eventStart}
                        onChange={(e) => setEventStart(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Event End:</label>
                    <input
                        type="datetime-local"
                        value={eventEnd}
                        onChange={(e) => setEventEnd(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>QR Code Content (Optional):</label>
                    <input
                        type="text"
                        value={qrCodeContent}
                        onChange={(e) => setQrCodeContent(e.target.value)}
                    />
                </div>
                <div>
                    <label>Max Requests Per User:</label>
                    <input
                        type="number"
                        value={maxRequests}
                        onChange={(e) => setMaxRequests(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Update Event</button>
            </form>
            <button onClick={handleDelete} style={{ marginTop: '20px', color: 'white', backgroundColor: 'red' }}>
                Delete Event
            </button>
        </div>
    );
};

export default UpdateEvent;
