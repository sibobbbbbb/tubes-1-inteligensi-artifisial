import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import ExperimentForm from '../components/ExperimentForm';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';

// Dynamically import MagicCube without SSR
const MagicCube = dynamic(() => import('../components/MagicCube'), { 
  ssr: false,
  loading: () => <LoadingSpinner /> // Show LoadingSpinner while MagicCube is loading
});

// Loading spinner component
function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 "></div>
    </div>
  );
}

export default function Home() {
  const [cubeState, setCubeState] = useState([]);
  const [experimentResult, setExperimentResult] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [gap, setGap] = useState(1.2); // New state for dynamic gap

  // Typing animation state
  const [displayedText, setDisplayedText] = useState('');
  const fullText = 'Diagonal Magic Cube';

  useEffect(() => {
    let index = 0;
    const typeText = () => {
      setDisplayedText(fullText.substring(0, index + 1));
      index += 1;
      if (index === fullText.length) {
        setTimeout(() => {
          index = 0;
          setDisplayedText('');
          typeText();
        }, 2000);
      } else {
        setTimeout(typeText, 150);
      }
    };
    typeText();
    return () => setDisplayedText('');
  }, []);

  useEffect(() => {
    // Fetch initial cube state from Flask backend
    fetch('http://localhost:5000/api/cube-state')
      .then((res) => res.json())
      .then((data) => setCubeState(data))
      .catch((error) => console.error("Failed to fetch initial cube state:", error));
  }, []);

  const handleExperimentSubmit = async (config) => {
    try {
      const response = await fetch('http://localhost:5000/api/run-experiment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });
      const result = await response.json();
      setCubeState(result.final_state);
      setExperimentResult({
        objectiveValue: result.objective_value,
        duration: result.duration.toFixed(2),
        plot: result.plot,
      });
    } catch (error) {
      console.error("Failed to run experiment:", error);
    }
  };

  return (
    <div className="relative w-full h-screen">
      {/* Navbar with Hamburger Icon */}
      <header className="fixed top-0 left-0 w-full bg-overlayBlack text-white flex justify-between items-center p-4 z-10">
        <h1 
          className="text-2xl font-semibold cursor-pointer" 
          onClick={() => window.location.reload()}
        >
          {displayedText}
        </h1>
        
        {/* Hamburger Icon to toggle sidebar */}
        <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="text-white">
          <AiOutlineMenu size={24} />
        </button>
      </header>

      {/* Fullscreen 3D Cube Canvas or Loading Spinner */}
      <MagicCube cubeState={cubeState} gap={gap} /> {/* Pass gap as a prop */}

      {/* Sidebar */}
      <div className={`fixed top-0 right-0 h-full w-64 bg-overlayBlack shadow-lg p-4 transform ${isSidebarOpen ? 'translate-x-0' : 'translate-x-full'} transition-transform duration-300 z-20`}>
        
        {/* Close Button at the top of the sidebar */}
        <button onClick={() => setIsSidebarOpen(false)} className="absolute top-4 right-4">
          <AiOutlineClose size={24} />
        </button>

        <h2 className="text-xl font-semibold mb-4">Run Experiment</h2>
        
        {/* Experiment Form */}
        <ExperimentForm onSubmit={handleExperimentSubmit} />

        {/* Gap Control Slider */}
        <div className="mt-4 p-4 bg-abu">
          <label htmlFor="gap" className="text-white">Adjust Gap:</label>
          <input
            type="range"
            id="gap"
            min="1.0"
            max="2.0"
            step="0.1"
            value={gap}
            onChange={(e) => setGap(parseFloat(e.target.value))}
            className="w-full mt-2"
          />
          <p className="text-white mt-1">Gap: {gap}</p>
        </div>

        {/* Display Experiment Results */}
        {experimentResult && (
          <div className="mt-4 p-4 bg-abu">
            <p><strong>Objective Value:</strong> {experimentResult.objectiveValue}</p>
            <p><strong>Duration:</strong> {experimentResult.duration} seconds</p>

            {/* Display the plot if available */}
            {experimentResult.plot && (
              <div className="mt-4">
                <img src={`data:image/png;base64,${experimentResult.plot}`} alt="Performance Plot" className="w-full h-auto" />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
