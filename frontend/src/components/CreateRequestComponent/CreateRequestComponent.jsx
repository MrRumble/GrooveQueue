import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; // Import useParams
import axios from 'axios';
import Navbar from '../Navbar/Navbar';
import { jwtDecode } from 'jwt-decode';  // Import jwtDecode as a named import

const CreateRequestForm = () => {
  const { eventId } = useParams(); // Get eventId from URL params
  const [songName, setSongName] = useState('');
  const [userId, setUserId] = useState(null);  
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // Pull user_id from the token stored in localStorage or sessionStorage
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    console.log('Token:', token); 
    if (token) {
      const decodedToken = jwtDecode(token);
      console.log('Decoded Token:', decodedToken);
      setUserId(decodedToken.sub);  // Use `sub` for guest_id based on your token
      console.log('Guest ID:', decodedToken.sub);
    }
  }, []);  

  const handleSubmit = async (e) => {
    e.preventDefault();

    setErrorMessage(null);
    setSuccessMessage(null);

    if (!songName.trim()) {
      setErrorMessage('Song name cannot be empty');
      return;
    }

    if (!userId) {
      setErrorMessage('User not logged in');
      return;
    }

    try {
      // Make a POST request to create the new request
      const response = await axios.post(`http://localhost:5001/events/${eventId}/requests`, {
        song_name: songName,
        guest_id: userId,  
      });

      setSuccessMessage(`Request created successfully! Request ID: ${response.data.request_id}`);
      setSongName('');  
    } catch (error) {
      if (error.response && error.response.data.error) {
        setErrorMessage(error.response.data.error);
      } else {
        setErrorMessage('An error occurred. Please try again.');
      }
    }
  };

  return (
    <div>
      <Navbar/>
      <h2>Create a Song Request for Event {eventId}</h2>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Song Name:</label>
          <input
            type="text"
            value={songName}
            onChange={(e) => setSongName(e.target.value)}
            required
          />
        </div>
        <button type="submit">Submit Request</button>
      </form>
    </div>
  );
};

export default CreateRequestForm;
