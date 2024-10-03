import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';

const CreateEvent = () => {
    const [eventName, setEventName] = useState('');
    const [location, setLocation] = useState('');
    const [eventStart, setEventStart] = useState('');
    const [eventEnd, setEventEnd] = useState('');
    const [qrCodeContent, setQrCodeContent] = useState('');
    const [maxRequests, setMaxRequests] = useState(''); // New state for max requests
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        const token = localStorage.getItem('access_token'); // Use the token for authorization
        const bandId = localStorage.getItem('band_id'); // Get band ID from localStorage

        if (!token) {
            setError("You must be logged in to create an event.");
            return;
        }

        if (new Date(eventStart) >= new Date(eventEnd)) {
            setError("Event end time must be after event start time.");
            return;
        }

        // Validate that max requests is a number and positive
        if (maxRequests < 0 || isNaN(maxRequests)) {
            setError("Max requests must be a positive number.");
            return;
        }

        setLoading(true); // Start loading

        try {
            const response = await fetch('http://localhost:5001/events', {
                method: 'POST',
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
                    max_requests_per_user: maxRequests, // Include max requests in the request body
                    band_id: bandId, // Include the band ID in the request
                }),
            });

            if (!response.ok) {
                const { error } = await response.json();
                throw new Error(error || 'Failed to create event');
            }

            const data = await response.json();
            setSuccess('Event created successfully!');
            navigate('/band-homepage'); // Redirect to the band's homepage after success
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false); // End loading
        }
    };

    return (
        <div>
            <Navbar />
            <h1>Create a New Event</h1>
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
                    <label>Max Requests:</label>
                    <input
                        type="number"
                        value={maxRequests}
                        onChange={(e) => setMaxRequests(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Creating Event...' : 'Create Event'}
                </button>
            </form>
        </div>
    );
};

export default CreateEvent;
