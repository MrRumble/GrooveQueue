import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link for navigation
import axios from 'axios';
import Navbar from '../Navbar/Navbar'; // Assuming you have a Navbar component for navigation

const AllEvents = () => {
  const [events, setEvents] = useState([]); // State to hold events
  const [loading, setLoading] = useState(true); // State to track loading status
  const [error, setError] = useState(null); // State to hold any errors

  useEffect(() => {
    // Function to fetch all events
    const fetchEvents = async () => {
      try {
        const response = await axios.get('http://localhost:5001/events'); // Update with your API URL
        setEvents(response.data); // Update state with events data
      } catch (err) {
        setError('Failed to fetch events'); // Set error message
      } finally {
        setLoading(false); // Set loading to false
      }
    };

    fetchEvents(); // Call fetch function
  }, []); // Empty dependency array to run effect once on mount

  // Render loading state
  if (loading) return <p>Loading events...</p>;

  // Render error state
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  // Render events list
  return (
    <div>
      <Navbar />
      <h2>All Events</h2>
      {events.length > 0 ? (
        <ul>
          {events.map((event) => (
            <li key={event.event_id}>
              <Link to={`/events/${event.event_id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                <h3>{event.event_name}</h3>
                <p>Location: {event.location}</p>
                <p>Start: {new Date(event.event_start).toLocaleString()}</p>
                <p>End: {new Date(event.event_end).toLocaleString()}</p>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No events found.</p>
      )}
    </div>
  );
};

export default AllEvents;
