import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';
import OfferRedeem from './OfferRedeem';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/offers/redeem/:offerId" element={<OfferRedeem />} />
            </Routes>
        </Router>
    );
}

export default App;

