import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from 'react-router-dom';
import HomePage from './components/Homepage';
import MaliciousIPDetector from './components/MaliciousIPDetector';
import LoadingScreen from './components/LoadingScreen';

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

function AppContent() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleNavigation = () => {
      setLoading(true);
      setTimeout(() => setLoading(false), 1500); // Simulating a 1.5s loading time
    };

    handleNavigation();
  }, [location.pathname]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-900 to-violet-400">
      {loading && <LoadingScreen />}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/malicious-ip-detector" element={<MaliciousIPDetector />} />
        {/* Add routes for other features here */}
      </Routes>
    </div>
  );
}

export default App;