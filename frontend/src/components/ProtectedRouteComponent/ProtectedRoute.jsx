import React from 'react';
import { Navigate } from 'react-router-dom';

// Utility function to check if the token is expired
const isTokenExpired = (token) => {
    if (!token) return true; // No token means expired
    try {
        const payload = JSON.parse(atob(token.split('.')[1])); // Decode JWT payload
        const expiry = payload.exp * 1000; // Convert to milliseconds
        return Date.now() > expiry; // Check if the token is expired
    } catch (e) {
        return true; // In case the token is malformed, treat it as expired
    }
};

const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('access_token'); // Get token from localStorage

    // If there's no token or it's expired, redirect to the login page
    if (!token || isTokenExpired(token)) {
        localStorage.removeItem('access_token'); // Clean up the token if it's invalid or expired
        return <Navigate to="/loginguest" />; // Redirect to login page
    }

    // If the token is valid, render the protected page
    return children;
};

export default ProtectedRoute;
