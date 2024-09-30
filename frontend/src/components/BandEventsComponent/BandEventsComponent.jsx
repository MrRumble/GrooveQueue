import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // Import useParams from react-router-dom

const BandEvents = () => {
  const { bandId } = useParams(); // Get bandId from URL parameters
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch(`http://localhost:5001/bands/${bandId}/events`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        // Log the entire response to see what's being returned
        console.log('Response:', response);
        console.log('Band ID:', bandId); // Log the bandId for debugging

        // Check if the response is an HTML error page
        if (!response.ok) {
          if (response.status === 404) {
            setError('No events found for this band');
          } else {
            throw new Error(`Failed to fetch events: ${response.statusText}`);
          }
        } else {
          // Try parsing the response as JSON
          const data = await response.json();
          setEvents(data);
        }
      } catch (err) {
        // Log the error for better debugging
        console.error('Error:', err);
        setError(err.message || 'Failed to fetch events');
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, [bandId]);

  if (loading) {
    return <div>Loading events...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h2>Events for Band {bandId}</h2>
      {events.length > 0 ? (
        <ul>
          {events.map((event) => (
            <li key={event.event_id}>
              <h3>{event.event_name}</h3>
              <p>Location: {event.location}</p>
              <p>Starts: {new Date(event.event_start).toLocaleString()}</p>
              <p>Ends: {new Date(event.event_end).toLocaleString()}</p>
              <p>QR Code Content: {event.qr_code_content}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No events found for this band.</p>
      )}
    </div>
  );
};

export default BandEvents;
