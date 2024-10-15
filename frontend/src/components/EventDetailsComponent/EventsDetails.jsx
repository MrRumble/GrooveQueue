import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom'; // Import Link to create navigation links
import Navbar from '../Navbar/Navbar';
import { jwtDecode } from 'jwt-decode'; // Import jwt-decode to decode JWT

const EventDetails = () => {
  const { eventId } = useParams(); // Extract the eventId from the URL parameters
  const [event, setEvent] = useState(null); // State to hold the event details
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state
  const [submitting, setSubmitting] = useState(false); // Loading state for attendance request

  useEffect(() => {
    const fetchEventDetails = async () => {
      try {
        const response = await fetch(`http://localhost:5001/events/${eventId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          if (response.status === 404) {
            setError('Event not found');
          } else {
            throw new Error(`Failed to fetch event: ${response.statusText}`);
          }
        } else {
          const data = await response.json();
          setEvent(data); // Set the event details including band_name
        }
      } catch (err) {
        console.error('Error fetching event details:', err);
        setError(err.message || 'Failed to fetch event details');
      } finally {
        setLoading(false); // Turn off the loading state once the data is fetched
      }
    };

    fetchEventDetails(); // Fetch the event details when the component mounts
  }, [eventId]);

  const handleAttendanceRequest = async () => {
    // Get guestId from the JWT token
    const token = localStorage.getItem('access_token'); // Ensure you use the correct key for your token
    let guestId;

    if (token) {
      try {
        const decodedToken = jwtDecode(token); // Decode the token to get the payload
        guestId = decodedToken.sub; // Use `sub` for guest_id based on your token
      } catch (error) {
        console.error('Error decoding token:', error);
        alert('Invalid token. Please log in again.'); // Handle invalid token case
        return; // Stop the function if the token is invalid
      }
    } else {
      alert('No access token found. Please log in.'); // Handle case where no token is available
      return; // Stop the function if there's no token
    }

    const attendanceData = {
      guest_id: guestId, // Use extracted guestId
      event_id: eventId,
      status: 'pending', // Set status to 'pending'
    };

    setSubmitting(true); // Start submitting state

    try {
      const response = await fetch('http://localhost:5001/attendance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`, // Use the token from localStorage
        },
        body: JSON.stringify(attendanceData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(`Error: ${errorData.error}`); // Handle error feedback
      } else {
        alert('Attendance request sent successfully!'); // Success feedback
      }
    } catch (error) {
      console.error('Error sending attendance request:', error);
      alert('Failed to send attendance request');
    } finally {
      setSubmitting(false); // Stop submitting state
    }
  };

  if (loading) return <div>Loading event details...</div>;

  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <Navbar />
      {event ? (
        <div>
          <h2>Event Details</h2>
          <h3>{event.event_name}</h3>
          <p><strong>Band Name:</strong> {event.band_name}</p>
          <p><strong>Location:</strong> {event.location}</p>
          <p><strong>Starts:</strong> {new Date(event.event_start).toLocaleString()}</p>
          <p><strong>Ends:</strong> {new Date(event.event_end).toLocaleString()}</p>
          <p><strong>QR Code Content:</strong> {event.qr_code_content}</p>

          {/* Button to send attendance request */}
          <button onClick={handleAttendanceRequest} style={{ display: 'inline-block', marginTop: '20px' }} disabled={submitting}>
            {submitting ? 'Sending...' : 'Send Attendance Request'}
          </button>

          {/* Link to create a song request */}
          <Link to={`/events/${eventId}/requests`} style={{ display: 'inline-block', marginTop: '20px' }}>
            <button>Create Song Request</button>
          </Link>
        </div>
      ) : (
        <p>No event details available.</p>
      )}
    </div>
  );
};

export default EventDetails;
