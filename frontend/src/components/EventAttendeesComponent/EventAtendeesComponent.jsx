import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // To access route parameters
import Navbar from '../../components/Navbar/Navbar'; // Assuming you have a Navbar component

const EventAttendees = () => {
    const { eventId } = useParams(); // Get eventId from URL parameters
    const [attendees, setAttendees] = useState([]); // State to hold attendees
    const [loading, setLoading] = useState(true); // State to show loading status
    const [error, setError] = useState(null); // State to handle errors

    // Fetch attendees when the component mounts
    useEffect(() => {
        const fetchAttendees = async () => {
            try {
                const response = await fetch(`http://localhost:5001/events/${eventId}/attendees`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // Assuming token is stored in localStorage
                    },
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch attendees');
                }

                const data = await response.json();
                setAttendees(data.attendees); // Set the fetched attendees to state
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAttendees(); // Call the function to fetch attendees
    }, [eventId]); // Dependency on eventId ensures it fetches new data if the eventId changes

    // Render loading state
    if (loading) return <div>Loading attendees...</div>;
    
    // Render error state
    if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

    return (
        <div>
            <Navbar /> {/* Include the Navbar component */}
            <div className="event-attendees">
                <h1>Attendees for Event ID: {eventId}</h1> {/* Display event ID */}
                {attendees.length > 0 ? (
                    <ul>
                        {attendees.map(attendee => (
                            <li key={attendee.attendance_id} className="attendee-item">
                                <p><strong>Guest ID:</strong> {attendee.guest_id}</p>
                                <p><strong>Guest Name:</strong> {attendee.guest_name}</p> {/* Display guest name */}
                                <p><strong>Guest Email:</strong> {attendee.guest_email}</p> {/* Display guest email */}
                                <p><strong>Status:</strong> {attendee.status}</p>
                                <p><strong>Created At:</strong> {new Date(attendee.created_at).toLocaleString()}</p>
                                <p><strong>Updated At:</strong> {new Date(attendee.updated_at).toLocaleString()}</p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No attendees found for this event.</p>
                )}
            </div>
        </div>
    );
};

export default EventAttendees;
