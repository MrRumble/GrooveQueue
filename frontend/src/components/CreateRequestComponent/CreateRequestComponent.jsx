import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom'; // Importing useParams
import {jwtDecode} from 'jwt-decode'; // Correct import for jwt_decode

const CreateRequest = () => {
    const { eventId } = useParams(); // Destructure eventId from useParams
    const [songName, setSongName] = useState('');
    const [artist, setArtist] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    const [guestId, setGuestId] = useState(null); // State to hold guest ID

    useEffect(() => {
        const token = localStorage.getItem('access_token'); // Assuming you store your JWT in local storage

        if (!token) {
            setError("No token found. Please log in.");
            return;
        }

        try {
            // Decode the token to get guest_id
            const decodedToken = jwtDecode(token);
            setGuestId(decodedToken ? decodedToken.sub : null); // Assuming 'sub' contains the guest_id
        } catch (err) {
            setError("Invalid token. Please log in again.");
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(false);

        if (!guestId) {
            setError('Guest ID not found. Please log in again.');
            return;
        }

        try {
            const response = await axios.post(`http://localhost:5001/events/${eventId}/requests`, {
                song_name: songName,
                artist: artist,
                guest_id: guestId // Include the guest_id in the request body
            }, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.status === 201) {
                setSuccess(true);
                setSongName('');
                setArtist('');
            }
        } catch (err) {
            if (err.response) {
                setError(err.response.data.error || 'An error occurred while submitting your request.');
            } else {
                setError('An error occurred. Please try again later.');
            }
        }
    };

    return (
        <div className="create-request">
            <h2>Create Song Request</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="songName">Song Name:</label>
                    <input
                        type="text"
                        id="songName"
                        value={songName}
                        onChange={(e) => setSongName(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="artist">Artist:</label>
                    <input
                        type="text"
                        id="artist"
                        value={artist}
                        onChange={(e) => setArtist(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Submit Request</button>
            </form>
            {error && <div className="error">{error}</div>}
            {success && <div className="success">Request submitted successfully!</div>}
        </div>
    );
};

export default CreateRequest;
