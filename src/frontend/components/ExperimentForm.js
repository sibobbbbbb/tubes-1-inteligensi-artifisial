// components/ExperimentForm.js
import { useState } from 'react';

export default function ExperimentForm({ onSubmit }) {
  const [algorithm, setAlgorithm] = useState("hill_climbing");
  const [variant, setVariant] = useState("steepest_ascent");
  const [populationSize, setPopulationSize] = useState(50);
  const [iterations, setIterations] = useState(1000);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      algorithm,
      variant: algorithm === "hill_climbing" ? variant : null,
      population_size: algorithm === "genetic_algorithm" ? populationSize : null,
      iterations,
    });
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
            <option value="sideways">Sideways</option>
            <option value="random_restart">Random Restart</option>
        </select>
        </label>
    )}

    {algorithm === "genetic_algorithm" && (
        <label className="block mb-2 font-medium w-40">
        <strong>Population Size:</strong>
        <input
            type="number"
            value={populationSize}
            onChange={(e) => setPopulationSize(parseInt(e.target.value))}
            className="mt-1 p-1 border border-gray-300 rounded text-gray-800 w-full"
        />
        </label>
    )}

    <label className="block mb-2 font-medium w-40">
        <strong>Iterations:</strong>
        <input
        type="number"
        value={iterations}
        onChange={(e) => setIterations(parseInt(e.target.value))}
        className="mt-1 p-1 border border-gray-300 rounded text-gray-800 w-full"
        />
    </label>

    <button
        type="submit"
        className="mt-4 mb-4 px-4 py-2 bg-ijo text-white font-semibold rounded w-40"
    >
        Execute
    </button>
    </form>

  );
}
