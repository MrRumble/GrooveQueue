import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignUpGuest from './pages/SignupGuest/SignupGuest';
import Home from './pages/Home/Home';
import LoginGuest from './pages/LoginGuest/LoginGuest';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/signupguest" element={<SignUpGuest />} />
                <Route path="/loginguest" element={<LoginGuest />} />
                <Route path="/" element={<Home />} />
            </Routes>
        </Router>
    );
};

export default App;