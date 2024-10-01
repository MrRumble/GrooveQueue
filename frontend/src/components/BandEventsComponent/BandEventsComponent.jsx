import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // Import useParams from react-router-dom
import Navbar from '../Navbar/Navbar';

const BandEvents = () => {
  const { bandId } = useParams(); // Get bandId from URL parameters
  const [bandName, setBandName] = useState(''); // State to hold the band name
  const [events, setEvents] = useState([]); // State to hold events
  const [loading, setLoading] = useState(true); // State to handle loading
  const [error, setError] = useState(null); // State to handle errors

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
        console.log('Band ID:', bandId); // Log the bandId for debugging

        // Check if the response is not OK
        if (!response.ok) {
          if (response.status === 404) {
            setError('No events found for this band');
          } else {
            throw new Error(`Failed to fetch events: ${response.statusText}`);
          }
        } else {
          // Parse the JSON response
          const data = await response.json();
          setBandName(data.band_name); // Set the band name from the response
          setEvents(data.events); // Set the events from the response
        }
      } catch (err) {
        // Log the error for better debugging
        console.error('Error:', err);
        setError(err.message || 'Failed to fetch events');
      } finally {
        setLoading(false); // Turn off loading state after the fetch completes
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
      <Navbar />
      <h2>Events for Band: {bandName}</h2> {/* Display band name */}
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
