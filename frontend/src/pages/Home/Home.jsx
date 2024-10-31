import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../../components/Navbar/Navbar';
import './Home.css';
import GrooveQueueLogo from "../../assets/GrooveQueueLogo.png"; // Ensure the import name is correct

const Home = () => {
  return (
    <div className="home-container">
      <Navbar className="home-navbar" />
      <header className="home-header">
      <h1>
        {Array.from("GROOVEQUEUE").map((letter, index) => (
          <span key={index} className={`letter letter-${index}`}>
            {letter}
          </span>
        ))}
      </h1>
      <p>Your ultimate event management and guest interaction platform.</p>
    </header>


      <div className="home-content">
        <img src={GrooveQueueLogo} alt="GrooveQueue Icon" className="home-logo-icon" />
        <p>
          Manage events, connect with your guests, and create an unforgettable experience with GrooveQueue.
        </p>
        <Link to="/signup" className="home-signup-now-button">Sign Up Now</Link>
      </div>
    </div>
  );
};

export default Home;
