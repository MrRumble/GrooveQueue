import React from 'react';
import { Link } from 'react-router-dom';
import './SignUpPage.css';
import Navbar from '../../components/Navbar/Navbar';

const SignupPage = () => {
  return (
    <div className="signup-selection-container">
      <Navbar />
      <h1 className="signup-header">Choose Your Account Type</h1>
      <p className="signup-paragraph">Are you signing up as a guest or a band?</p>

      <div className="info-boxes">
        <div className="info-box">
          <h2 className="info-box-header">Guest</h2>
          <ul className="info-box-paragraph">
            <li>Scan a QR code to access the app.</li>
            <li>Request your favorite songs before AND during the event.</li>
            <li>Add a personal dedication to your song request.</li>
            <li>Receive real-time updates on your song status.</li>
          </ul>
          <Link to="/signupguest" className="signup-button">Sign Up as Guest</Link>
        </div>

        <div className="info-box">
          <h2 className="info-box-header">Band</h2>
          <ul className="info-box-paragraph">
            <li>Create and manage multiple events effortlessly.</li>
            <li>Generate unique QR codes for each event.</li>
            <li>View and manage incoming song requests in real-time.</li>
            <li>Access analytics on song requests and guest interactions.</li>
          </ul>
          <Link to="/signupband" className="signup-button">Sign Up as Band</Link>
        </div>
      </div>
    </div>
  );
}

export default SignupPage;
