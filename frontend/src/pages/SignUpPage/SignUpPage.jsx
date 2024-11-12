import React from 'react';
import { Link } from 'react-router-dom';
import './SignUpPage.css';
import Navbar from '../../components/Navbar/Navbar';
import grooveQueueLogo from '../../assets/GrooveQueueLogo.png'; // Adjust the path as needed
import guestImage from '../../assets/guest.jpg'; // Your Guest photo
import bandImage from '../../assets/band.jpg'; // Your Band photo

const SignupPage = () => {
  return (
    <div className="signup-selection-container">
      <Navbar />
      <h1 className="signup-header">Choose Your Account Type</h1>

      <div className="info-boxes">
        {/* Guest Signup Tile */}
        <Link to="/signupguest" className="info-box" style={{ backgroundImage: `url(${guestImage})` }}>
          <div className="overlay">
            <h2 className="info-box-header">GUEST</h2>
            <ul className="info-box-paragraph">
              <li>Scan a QR code to access the app.</li>
              <li>Request your favorite songs before AND during the event.</li>
              <li>Add a personal dedication to your song request.</li>
              <li>Receive real-time updates on your song status.</li>
            </ul>
          </div>
        </Link>

        {/* Band Signup Tile */}
        <Link to="/signupband" className="info-box" style={{ backgroundImage: `url(${bandImage})` }}>
          <div className="overlay">
            <h2 className="info-box-header">BAND</h2>
            <ul className="info-box-paragraph">
              <li>Create and manage multiple events effortlessly.</li>
              <li>Generate unique QR codes for each event.</li>
              <li>View and manage incoming song requests in real-time.</li>
              <li>Access analytics on song requests and guest interactions.</li>
            </ul>
          </div>
        </Link>
      </div>
    </div>
  );
};

export default SignupPage;
