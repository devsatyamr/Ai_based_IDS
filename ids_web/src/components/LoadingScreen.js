import React, { useEffect, useRef, useState } from 'react';
import lottie from 'lottie-web';
import animationData from '../animations/loading-animation2.json'; // Adjust this path to where your JSON file is located

function LoadingScreen() {
  const container = useRef(null);
  const [animationLoaded, setAnimationLoaded] = useState(false);

  useEffect(() => {
    let anim = null;
    if (container.current) {
      anim = lottie.loadAnimation({
        container: container.current,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData: animationData
      });

      anim.addEventListener('DOMLoaded', () => {
        setAnimationLoaded(true);
      });
    }

    return () => {
      if (anim) anim.destroy();
    };
  }, []);

  return (
    <div className="fixed inset-0 bg-opacity-50 backdrop-filter backdrop-blur-sm flex items-center justify-center z-50">
      <div className="text-white text-4xl font-bold flex flex-col items-center">
        <div ref={container} style={{ width: 100, height: 100 }}></div>
        {!animationLoaded && (
          <p className="mt-4">
            Wait a minute
            <span className="animate-pulse">.</span>
            <span className="animate-pulse delay-100">.</span>
            <span className="animate-pulse delay-200">.</span>
          </p>
        )}
      </div>
    </div>
  );
}

export default LoadingScreen;