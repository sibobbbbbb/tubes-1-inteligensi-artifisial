from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import random
import time
import matplotlib.pyplot as plt
import io
import base64
from geneticAlgorithm import *
from simulatedAnnealing import *
from hillClimbing import *

app = Flask(__name__)
CORS(app)

# Utility function to create the cube
def create_initial_cube(size=5):
    numbers = list(range(1, size**3 + 1))
    random.shuffle(numbers)
    cube = np.array(numbers).reshape((size, size, size))
    return cube

# Objective function placeholder (you'll need to implement the actual logic)
def objective_function(cube):
    # This should calculate the "magic" objective value based on your problem
    return np.sum(cube)  # Simplified for demonstration

# Helper to generate a neighbor (swap two random elements)
def generate_neighbor(cube):
    neighbor = cube.copy()
    x1, y1, z1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
    x2, y2, z2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
    neighbor[x1, y1, z1], neighbor[x2, y2, z2] = neighbor[x2, y2, z2], neighbor[x1, y1, z1]
    return neighbor

# Hill-Climbing Algorithm Variants
def hill_climbing(cube, variant="steepest_ascent", max_sideways=5, max_restarts=5):
    if variant == "steepest_ascent":
        hillClimber = SteepestAscent(Cube(cube.copy()))
    elif variant == "stochastic":
        hillClimber = StochasticHC(Cube(cube.copy()))
    elif variant == "sideways":
        hillClimber = SidewaysMovement(Cube(cube.copy()), max_sideways)
    elif variant == "random_restart":
        hillClimber = RandomRestart(Cube(cube.copy()), max_restarts)
    else:
        raise "There is no such variant!"
    
    startTime = time.time()
    
    hillClimber.search()

    duration = time.time() - startTime
    
    current_state = hillClimber.state.cube
    current_value = hillClimber.state.value
    objective_values = hillClimber.objectiveValues
    iterations = hillClimber.iteration

    result = {
        "initial_state": cube.tolist(),
        "final_state": current_state.tolist(),
        "objective_value": current_value,
        "objective_values": objective_values,
        "iterations": iterations,
        "duration" : duration
    }

    if variant == "random_restart":
        result["restart_number"] = hillClimber.maxRestart
        result["restart_iterations"] = hillClimber.iterationsPerRestart

    return result


def simulated_annealing(cube, max_iter=100000, initial_temp=10000, cooling_rate=0.77, threshold=0.5):
    
    Simulated_annealing = SimulatedAnnealing(Cube(cube.copy()), max_iter, initial_temp, cooling_rate,threshold)
    Simulated_annealing.search()
    final_cube = Simulated_annealing.state.cube
    best_value = Simulated_annealing.best_value
    array_value = Simulated_annealing.objective_values
    duration = Simulated_annealing.duration
    iterations = Simulated_annealing.iteration
    stuck = Simulated_annealing.stuck
    array_e = Simulated_annealing.eValue
    
    return {
        "initial_state" : cube.tolist(),
        "final_state": final_cube.tolist(),
        "objective_value": best_value,
        "objective_values": array_value,
        "duration": duration,
        "iterations": iterations,
        "stuck" : stuck,
        "e_values" : array_e  
    }


# Genetic Algorithm
def genetic_algorithm(cube,n_population, n_generations):
    genetic = GeneticAlgorithm(Cube(cube.copy()),n_population, n_generations)
    return genetic.run()

# API endpoint to get the initial cube state
@app.route('/api/cube-state', methods=['GET'])
def get_initial_cube():
    cube = create_initial_cube()
    return jsonify(cube.tolist())

# Endpoint to run experiments
@app.route('/api/run-experiment', methods=['POST'])
def run_experiment():
    data = request.json
    algorithm = data.get("algorithm")
    size = data.get("size", 5)
    iterations = data.get("iterations", 1000)
    population_size = data.get("population_size", 50)

    if algorithm == "simulated_annealing":
        temperature = data.get("temperature")
        threshold = data.get("threshold")
        cooling_rate = data.get("cooling_rate")
    
    cube = create_initial_cube(size)
    initial_state = cube.copy()
    
    start_time = time.time()

    if algorithm == "hill_climbing":
        result = hill_climbing(cube, variant=data.get("variant", "steepest_ascent"), max_sideways=data.get("max_sideways_moves", 5), max_restarts=data.get("max_restarts", 5))
    elif algorithm == "simulated_annealing":
        result = simulated_annealing(cube, 100000, temperature, cooling_rate, threshold)
    elif algorithm == "genetic_algorithm":
        result = genetic_algorithm(cube,population_size, iterations)
    
    duration = time.time() - start_time

    # Generate plot
    if (algorithm != "genetic_algorithm"):
        fig, ax = plt.subplots()
        ax.plot(result['objective_values'])
        ax.set_xlabel("Iterations")
        ax.set_ylabel("Objective Function Value")
        plt.title(f"{algorithm.capitalize()} Performance")
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
    
    else:
        fig, ax = plt.subplots()
        ax.plot(result["min_cost_per_generation"], label="Min Objective Function")
        ax.plot(result["avg_cost_per_generation"], label="Average Objective Function")
        ax.set_xlabel("Generasi")
        ax.set_ylabel("Objective Function")
        plt.legend()
        plt.title("Genetic Algorithm - Objective Function")
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

    if (algorithm == "simulated_annealing"):
        fig, ax = plt.subplots()
        ax.plot(result['e_values'])
        ax.set_xlabel("Iterations")
        ax.set_ylabel("e Value")
        plt.title(f"{algorithm.capitalize()} Performance")
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url2 = base64.b64encode(img.getvalue()).decode()
        return jsonify({
            "initial_state": initial_state.tolist(),  # Convert numpy array to list
            "final_state": np.array(result['final_state']).tolist(),  # Ensure final_state is a list
            "objective_value": int(result['objective_value']),  # Convert numpy int to native int
            "duration": float(duration),  # Convert to native float
            "plot": plot_url,
            "iterations": result["iterations"],  # Ensure iterations
            "plot2": plot_url2,
            "stuck": result['stuck']
        })

    # Ensure that all numpy objects are converted to native Python types

    return jsonify({
        "initial_state": initial_state.tolist(),  # Convert numpy array to list
        "final_state": np.array(result['final_state']).tolist(),  # Ensure final_state is a list
        "objective_value": int(result['objective_value']),  # Convert numpy int to native int
        "duration": float(duration),  # Convert to native float
        "plot": plot_url,
        "iterations": result["iterations"]  # Ensure iterations
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
