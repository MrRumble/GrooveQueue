import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // To get the event_id from the URL

const EventDetails = () => {
  const { eventId } = useParams(); // Extract the eventId from the URL parameters
  const [event, setEvent] = useState(null); // State to hold the event details
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state

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

  if (loading) return <div>Loading event details...</div>;

  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      {event ? (
        <div>
          <h2>Event Details</h2>
          <h3>{event.event_name}</h3>
          <p><strong>Band Name:</strong> {event.band_name}</p> {/* Display the band name */}
          <p><strong>Location:</strong> {event.location}</p>
          <p><strong>Starts:</strong> {new Date(event.event_start).toLocaleString()}</p>
          <p><strong>Ends:</strong> {new Date(event.event_end).toLocaleString()}</p>
          <p><strong>QR Code Content:</strong> {event.qr_code_content}</p>
        </div>
      ) : (
        <p>No event details available.</p>
      )}
    </div>
  );
};

export default EventDetails;
