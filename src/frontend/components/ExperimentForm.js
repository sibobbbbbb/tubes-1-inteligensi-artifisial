// components/ExperimentForm.js
import { useState } from 'react';

export default function ExperimentForm({ onSubmit }) {
  const [algorithm, setAlgorithm] = useState("hill_climbing");
  const [variant, setVariant] = useState("steepest_ascent");
  const [populationSize, setPopulationSize] = useState(50);
  const [iterations, setIterations] = useState(1000); // Iterations for Genetic Algorithm only
  const [threshold, setThreshold] = useState(0.01);
  const [temperature, setTemperature] = useState(100);
  const [coolingRate, setCoolingRate] = useState(0.95);
  const [maxSidewaysMoves, setMaxSidewaysMoves] = useState(10); // For Sideways Move
  const [maxRestarts, setMaxRestarts] = useState(5); // For Random Restart

  const handleSubmit = (e) => {
    e.preventDefault();

    const config = {
      algorithm,
      variant: algorithm === "hill_climbing" ? variant : null,
      population_size: algorithm === "genetic_algorithm" ? populationSize : null,
      ...(algorithm === "genetic_algorithm" && { iterations }),
      ...(algorithm === "simulated_annealing" && {
        threshold,
        temperature,
        cooling_rate: coolingRate,
      }),
      ...(algorithm === "hill_climbing" && variant === "sideways" && { max_sideways_moves: maxSidewaysMoves }),
      ...(algorithm === "hill_climbing" && variant === "random_restart" && { max_restarts: maxRestarts }),
    };

    onSubmit(config);
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 mt-7 bg-abu shadow-md w-full max-w-md mx-auto flex flex-col items-center">
      <label className="block mb-2 font-medium w-40">
        <strong>Algorithm:</strong>
        <select
          value={algorithm}
          onChange={(e) => setAlgorithm(e.target.value)}
          className="mt-1 p-1 border border-gray-300 rounded text-gray-800 w-full"
        >
          <option value="hill_climbing">Hill Climbing</option>
          <option value="simulated_annealing">Simulated Annealing</option>
          <option value="genetic_algorithm">Genetic Algorithm</option>
        </select>
      </label>

      {algorithm === "hill_climbing" && (
        <label className="block mb-2 font-medium w-40">
          <strong>Variant:</strong>
          <select
            value={variant}
            onChange={(e) => setVariant(e.target.value)}
            className="mt-1 p-1 border rounded border-gray-300 text-gray-800 w-full"
          >
            <option value="steepest_ascent">Steepest Ascent</option>
            <option value="stochastic">Stochastic</option>
            <option value="sideways">Sideways Move</option>
            <option value="random_restart">Random Restart</option>
          </select>
        </label>
      )}

      {algorithm === "hill_climbing" && variant === "sideways" && (
        <label className="block mb-2 font-medium w-40">
          <strong>Maximum Sideways Moves:</strong>
          <input
            type="number"
            value={maxSidewaysMoves}
            onChange={(e) => setMaxSidewaysMoves(parseInt(e.target.value))}
            className="mt-1 p-1 border border-gray-300 rounded text-gray-800 w-full"
            min="1"
          />
        </label>
      )}

      {algorithm === "hill_climbing" && variant === "random_restart" && (
        <label className="block mb-2 font-medium w-40">
          <strong>Maximum Restarts:</strong>
          <input
            type="number"
            value={maxRestarts}
            onChange={(e) => setMaxRestarts(parseInt(e.target.value))}
            className="mt-1 p-1 border border-gray-300 rounded text-gray-800 w-full"
            min="1"
          />
        </label>
      )}

      {algorithm === "genetic_algorithm" && (
        <>
          <label className="block mb-2 font-medium w-40">
            <strong>Population Size:</strong>
            <input
              type="number"
              value={populationSize}
              onChange={(e) => setPopulationSize(parseInt(e.target.value))}
              className="mt-1 p-1 border border-gray-300 rounded text-gray-800 w-full"
              min="1"
            />
          </label>

          <label className="block mb-2 font-medium w-40">
            <strong>Iterations:</strong>
            <input
              type="number"
              value={iterations}
              onChange={(e) => setIterations(parseInt(e.target.value))}
              className="mt-1 p-1 border border-gray-300 rounded text-gray-800 w-full"
              min="1"
            />
          </label>
        </>
      )}

      {algorithm === "simulated_annealing" && (
        <>
          <label className="block mb-2 font-medium w-40">
            <strong>Threshold:</strong>
            <input
              type="number"
              value={threshold}
              onChange={(e) => setThreshold(parseFloat(e.target.value))}
              className="mt-1 p-1 border border-gray-300 rounded text-gray-800 w-full"
              step="0.01"
              min="0"
            />
          </label>

          <label className="block mb-2 font-medium w-40">
            <strong>Temperature:</strong>
            <input
              type="number"
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
              className="mt-1 p-1 border border-gray-300 rounded text-gray-800 w-full"
              step="0.1"
              min="0"
            />
          </label>

          <label className="block mb-2 font-medium w-40">
            <strong>Cooling Rate:</strong>
            <input
              type="number"
              value={coolingRate}
              onChange={(e) => setCoolingRate(parseFloat(e.target.value))}
              className="mt-1 p-1 border border-gray-300 rounded text-gray-800 w-full"
              step="0.01"
              min="0"
              max="1"
            />
          </label>
        </>
      )}

      <button
        type="submit"
        className="mt-4 mb-4 px-4 py-2 bg-ijo text-white font-semibold rounded w-40"
      >
        Execute
      </button>
    </form>
  );
}
