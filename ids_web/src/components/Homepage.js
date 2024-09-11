import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  const [text, setText] = useState('');
  const fullText = "Our IDS provides advanced features to detect and analyze potential security threats in real-time, enhancing your network's overall security posture.";

  useEffect(() => {
    let i = 0;
    const typingEffect = setInterval(() => {
      if (i < fullText.length) {
        setText(prevText => prevText + fullText.charAt(i));
        i++;
      } else {
        clearInterval(typingEffect);
      }
    }, 90); // Adjust typing speed here

    return () => clearInterval(typingEffect);
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center mb-12 text-white">
        SentinelX
      </h1>
      <div className="flex flex-col md:flex-row gap-40 py-16">
        <div className="md:w-1/2 flex items-center">
          <p className="text-white text-4xl font-monospace px-16 typing-text">
            {text}
            <span className="cursor"></span>
          </p>
        </div>
        
        <div className="md:w-1/2">
          <h2 className="text-2xl font-semibold mb-4 text-white">Features</h2>
          <div className="space-y-4">
            <Link to="/malicious-ip-detector" className="block bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg shadow-md rounded-lg p-4 hover:bg-opacity-30 transition duration-300">
              <h3 className="text-xl font-semibold mb-2 text-white">Malicious IP Detector</h3>
              <p className="text-white">Detect and analyze potentially malicious IP addresses in your network.</p>
            </Link>
            <Link to="/feature2" className="block bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg shadow-md rounded-lg p-4 hover:bg-opacity-30 transition duration-300">
              <h3 className="text-xl font-semibold mb-2 text-white">Feature 2</h3>
              <p className="text-white">Description of Feature 2.</p>
            </Link>
            <Link to="/feature3" className="block bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg shadow-md rounded-lg p-4 hover:bg-opacity-30 transition duration-300">
              <h3 className="text-xl font-semibold mb-2 text-white">Feature 3</h3>
              <p className="text-white">Description of Feature 3.</p>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;