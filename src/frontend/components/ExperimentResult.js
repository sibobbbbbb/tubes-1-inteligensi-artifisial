// components/ExperimentResult.js
export default function ExperimentResult({ result }) {
    if (!result) return null;
  
    return (
      <div className="p-4 mt-6 border rounded">
        <h2 className="text-xl font-semibold mb-4">Experiment Results</h2>
        <p><strong>Initial State:</strong></p>
        <pre>{JSON.stringify(result.initial_state, null, 2)}</pre>
  
        <p><strong>Final State:</strong></p>
        <pre>{JSON.stringify(result.final_state, null, 2)}</pre>
  
        <p><strong>Objective Value:</strong> {result.objective_value}</p>
        <p><strong>Duration:</strong> {result.duration.toFixed(2)} seconds</p>
        {result.stuck && (<p><strong>Stuck:</strong> {result.stuck}</p>)}

        <div className="mt-4">
          <img src={`data:image/png;base64,${result.plot}`} alt="Performance Plot" />
        </div>
        {result.plot2 && (
            <div className="mt-4">
              <img src={`data:image/png;base64,${result.plot2}`} alt="Energy Values Plot" />
            </div>
          )}

      </div>
    );
  }
  