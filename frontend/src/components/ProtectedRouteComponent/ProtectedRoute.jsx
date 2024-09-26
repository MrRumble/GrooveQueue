import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('access_token'); // Use the correct key for your token

    // If there's no token, redirect to the login page
    if (!token) {
        return <Navigate to="/loginguest" />;
    }

    // If there is a token, render the child component (the protected page)
    return children;
};

export default ProtectedRoute;
