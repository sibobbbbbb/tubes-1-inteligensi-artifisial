from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import random
import time
import matplotlib.pyplot as plt
import io
import base64
from genetic import *

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
def hill_climbing(cube, variant="steepest_ascent", max_sideways=10, max_restarts=10):
    current_state = cube
    current_value = objective_function(current_state)
    objective_values = [current_value]
    iterations = 0
    sideways_moves = 0
    restarts = 0

    while restarts <= max_restarts:
        # Generate neighbors
        neighbors = [generate_neighbor(current_state) for _ in range(20)]
        
        # Initialize next_state to None at the start of each loop iteration
        next_state = None

        # Determine next state based on the variant
        if variant == "steepest_ascent":
            # Choose the neighbor with the highest objective value
            if neighbors:
                next_state = max(neighbors, key=objective_function)
        elif variant == "stochastic":
            # Randomly pick one of the neighbors that improves the objective value
            improving_neighbors = [n for n in neighbors if objective_function(n) >= current_value]
            if improving_neighbors:
                next_state = random.choice(improving_neighbors)
        elif variant == "sideways":
            if neighbors:
                next_state = max(neighbors, key=objective_function)
                if next_state and objective_function(next_state) == current_value:
                    sideways_moves += 1
                    if sideways_moves > max_sideways:
                        break
                else:
                    sideways_moves = 0  # Reset sideways moves if there's an improvement

        # Ensure `next_state` is defined and not None before proceeding
        if next_state is None:
            # If no valid moves are found, and no valid `next_state` is set, break the loop
            break

        next_value = objective_function(next_state)

        # Stopping condition if no improvement
        if next_value <= current_value:
            if variant == "random_restart":
                current_state = create_initial_cube()
                current_value = objective_function(current_state)
                restarts += 1
            else:
                break
        else:
            current_state, current_value = next_state, next_value
            objective_values.append(current_value)
            iterations += 1

    return {
        "final_state": current_state.tolist(),
        "objective_value": current_value,
        "objective_values": objective_values,
        "iterations": iterations
    }



# Simulated Annealing
def simulated_annealing(cube, initial_temp=1000, cooling_rate=0.003):
    current_state = cube
    current_value = objective_function(current_state)
    temp = initial_temp
    objective_values = [current_value]
    iterations = 0

    while temp > 1:
        neighbor = generate_neighbor(current_state)
        next_value = objective_function(neighbor)

        # Calculate probability and decide to accept or reject the neighbor
        if next_value > current_value or random.uniform(0, 1) < np.exp((next_value - current_value) / temp):
            current_state, current_value = neighbor, next_value

        temp *= (1 - cooling_rate)
        objective_values.append(current_value)
        iterations += 1

    return {
        "final_state": current_state.tolist(),
        "objective_value": current_value,
        "objective_values": objective_values,
        "iterations": iterations
    }

# Genetic Algorithm
def genetic_algorithm(init,n_population, n_generations=100, elitism_rate=0.1):
    # Initial state and tracking
    cubes = random_population(n_population - 1)
    cubes.append(init)
    
    min_cost_per_generation = []
    avg_cost_per_generation = []
    
    elite_size = max(1, int(n_population * elitism_rate)) 

    for generation in range(n_generations):
        mutation_rate = max(0.05, 0.2 * (1 - generation / n_generations))
        
        # Calculate fitness
        fitness = count_fitness(cubes)

        costs = [calculate_cost(cube, 315) for cube in cubes]
        sorted_indices = np.argsort(costs)
        
        # Track max and average fitness for each generation
        min_cost_per_generation.append(np.min(costs))
        avg_cost_per_generation.append(np.mean(costs))
        
        # Retain elites
        elites = [cubes[i] for i in sorted_indices[-elite_size:]]
        
        cumulative_probabilities = count_probability_random(fitness)
        selected_cubes = selection(cumulative_probabilities, cubes)
        results = crossover(selected_cubes)
        final = mutation(results, mutation_rate)
        
        # Create next generation
        cubes = random_population(n_population - elite_size - 1) + list(final) + elites
        fitness = count_fitness(cubes)
        
        # Select best individuals
        cubes = [cubes[i] for i in np.argsort(fitness)[-n_population:]]

    # Final best cube and cost
    cost_and_cubes = [(calculate_cost(cube, 315), cube) for cube in cubes]
    cost, best_array = min(cost_and_cubes, key=lambda x: x[0])

    return {
        "initial_state": init.tolist(),
        "final_state": best_array.tolist(),
        "objective_value": int(cost),
        "min_cost_per_generation": min_cost_per_generation,
        "avg_cost_per_generation": avg_cost_per_generation,
    }

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
    
    cube = create_initial_cube(size)
    initial_state = cube.copy()
    
    start_time = time.time()

    if algorithm == "hill_climbing":
        result = hill_climbing(cube, variant=data.get("variant", "steepest_ascent"))
    elif algorithm == "simulated_annealing":
        result = simulated_annealing(cube)
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

    # Ensure that all numpy objects are converted to native Python types
    return jsonify({
        "initial_state": initial_state.tolist(),  # Convert numpy array to list
        "final_state": np.array(result['final_state']).tolist(),  # Ensure final_state is a list
        "objective_value": int(result['objective_value']),  # Convert numpy int to native int
        "duration": float(duration),  # Convert to native float
        "plot": plot_url
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
