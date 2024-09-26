import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignUpGuest from './pages/SignupGuest/SignupGuest';
import Home from './pages/Home/Home';
import LoginGuest from './pages/LoginGuest/LoginGuest';
import GuestHomepage from './pages/GuestHomepage/GuestHomepage';
import SignUpBand from './pages/SignupBand/SignupBand';
import LoginBand from './pages/LoginBand/LoginBand';
import BandHomepage from './pages/BandHomepage/BandHomepage';
import ProtectedRoute from './components/ProtectedRouteComponent/ProtectedRoute';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/signupguest" element={<SignUpGuest />} />
                <Route path="/loginguest" element={<LoginGuest />} />
                <Route path="/" element={<Home />} />
                <Route path="/guest-homepage" element={<ProtectedRoute><GuestHomepage /></ProtectedRoute>} />
                <Route path="/signupband" element={<SignUpBand />} />
                <Route path="/loginband" element={<LoginBand />} />
                <Route path="/band-homepage" element={<ProtectedRoute><BandHomepage /></ProtectedRoute>} />
            </Routes>
        </Router>
    );
};

export default App;
