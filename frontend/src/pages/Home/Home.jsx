import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';

const Home = () => {
return (
    <div className="home-container">
        <Navbar />
        <header className="header">
            <h1>Welcome to GrooveQueue</h1>
            <p>Your ultimate event management and guest interaction platform.</p>
        </header>

    <div className="content">
        <p>
        Manage events, connect with your guests, and create an unforgettable experience with GrooveQueue.
        </p>
        <Link to="/signupguest" className="signup-link">
        Sign Up as Guest
        </Link>
    </div>
    </div>
    );
}

export default Home;
