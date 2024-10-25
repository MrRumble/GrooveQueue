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
import CreateEvent from './components/CreateEventComponent/CreateEventComponent';
import EventDetails from './components/EventDetailsComponent/EventsDetails';
import CurrentBandEvents from './components/CurrentBandEventsComponent/CurrentBandEventsComponent';
import BandEvents from './components/BandEventsComponent/BandEventsComponent';
import AllEvents from './components/AllEventsComponent/AllEvents';
import UpdateEvent from './components/UpdateEventComponent/UpdateEventComponent';
import EventAttendees from './components/EventAttendeesComponent/EventAtendeesComponent';
import NotificationsPage from './pages/NotificationsPage/NotificationsPage';
import SignupPage from './pages/SignUpPage/SignUpPage';
import CreateRequest from './components/CreateRequestComponent/CreateRequestComponent';



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
                <Route path="/create-event" element={<ProtectedRoute><CreateEvent/></ProtectedRoute>} />
                <Route path="/update-event/:eventId" element={<ProtectedRoute><UpdateEvent /></ProtectedRoute>} />
                <Route path="/events/:eventId" element={<EventDetails/>} />
                <Route path="/current-band-events" element={<CurrentBandEvents/>} />
                <Route path="/bands/:bandId/events" element={<BandEvents />} />
                <Route path="/events" element={<AllEvents />} />
                <Route path="/event-attendees/:eventId" element={<EventAttendees />} />
                <Route path="/notifications" element={<NotificationsPage />} />
                <Route path="/signup" element={<SignupPage />} />
                <Route path="/events/:eventId/requests" element={<CreateRequest />} />
                
            </Routes>
        </Router>
    );
};

export default App;
