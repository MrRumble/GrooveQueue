import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <Navbar />
      <header className="header">
        <h1>
          {Array.from('GROOVEQUEUE').map((letter, index) => (
            <span key={index}>{letter}</span>
          ))}
        </h1>
        <p>Your ultimate event management and guest interaction platform.</p>
      </header>

      <div className="content">
        <p>
          Manage events, connect with your guests, and create an unforgettable experience with GrooveQueue.
        </p>
        <Link to="/signup" className="signup-now-button">Sign Up Now</Link>
      </div>
    </div>
  );
};

export default Home;
