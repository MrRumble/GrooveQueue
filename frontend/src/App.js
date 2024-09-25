import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GuestPage from './pages/GuestPage';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/guests" element={<GuestPage />} />
                <Route path="/" element={<h1>Home Page</h1>} />
            </Routes>
        </Router>
    );
};

export default App;
