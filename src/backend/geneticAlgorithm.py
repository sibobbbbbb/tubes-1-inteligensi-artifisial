import numpy as np
import random
from collections import Counter
from cube import *

class GeneticAlgorithm:
    def __init__(self, initial_state: Cube, n_population=100, n_generations=100, elitism_rate=0.1):
        self.initial_state = initial_state
        self.n_population = n_population
        self.n_generations = n_generations
        self.elitism_rate = elitism_rate
        self.min_cost_per_generation = []
        self.avg_cost_per_generation = []
        self.population = self.__initialize_population()
        
    def __initialize_population(self):
        population = [Cube() for _ in range(self.n_population - 1)]
        population.append(self.initial_state)
        return population

    def __calculate_fitness(self, cubes):
        fitness = [1 / (1 + cube.value) for cube in cubes]
        return fitness

    def __selection(self, cumulative_probabilities, cubes):
        selected_cube = []
        for _ in range(2):
            r = random.random()
            for i, cp in enumerate(cumulative_probabilities):
                if r <= cp:
                    selected_cube.append(cubes[i].copy())
                    break
        return selected_cube

    def __crossover(self, selected_cubes):
        crossover_point = random.randint(0, 124)
  
        # Flatten to perform crossover
        cube1 = np.array(selected_cubes[0].cube).flatten()
        cube2 = np.array(selected_cubes[1].cube).flatten()
        
        # Create children by swapping segments between the two crossover points
        child1 = np.concatenate((cube1[:crossover_point], cube2[crossover_point:])).reshape((5, 5, 5))
        child2 = np.concatenate((cube2[:crossover_point], cube1[crossover_point:])).reshape((5, 5, 5))
        
        return [Cube(child1), Cube(child2)]

    def __mutation(self, children, mutation_rate=0.1):
        mutated_children = []
        for child in children:
            if not self.is_cube_unique(child.cube):
                element_counts = Counter(child.cube.flatten())
                duplicates = [item for item, count in element_counts.items() if count > 1]
                missing = [num for num in range(1, 126) if num not in element_counts]
                
                for duplicate, miss in zip(duplicates, missing):
                    duplicate_index = np.where(child.cube == duplicate)
                    if len(duplicate_index[0]) > 0:
                        child.cube[duplicate_index[0][0], duplicate_index[1][0], duplicate_index[2][0]] = miss
            
            if random.random() < mutation_rate:
                # Randomly swap two positions
                idx1, idx2 = random.sample(range(125), 2)
                pos1 = np.unravel_index(idx1, (5, 5, 5))
                pos2 = np.unravel_index(idx2, (5, 5, 5))
                child.cube[pos1], child.cube[pos2] = child.cube[pos2], child.cube[pos1]
            
            mutated_children.append(child)
        return mutated_children

    def is_cube_unique(self, cube):
        # Check if all elements in the cube are unique
        flattened_cube = cube.flatten()
        return len(flattened_cube) == len(set(flattened_cube))

    def run(self):
        for generation in range(self.n_generations):
            mutation_rate = max(0.05, 0.2 * (1 - generation / self.n_generations))
            fitness = self.__calculate_fitness(self.population)

            costs = [cube.value for cube in self.population]
            sorted_indices = np.argsort(costs)
            
            # Track min and average cost
            self.min_cost_per_generation.append(np.min(costs))
            self.avg_cost_per_generation.append(np.mean(costs))
            
            # Retain elites
            elite_size = max(1, int(self.n_population * self.elitism_rate * (1 - generation / self.n_generations)))
            elites = [self.population[i] for i in sorted_indices[-elite_size:]]
            
            # Calculate cumulative probabilities
            probabilities = [f / sum(fitness) for f in fitness]
            cumulative_probabilities = np.cumsum(probabilities).tolist()
            
            # Select parents and generate children
            selected_cubes = self.__selection(cumulative_probabilities, self.population)
            children = self.__crossover(selected_cubes)
            mutated_children = self.__mutation(children, mutation_rate)
            
            # Generate new population
            self.population = [Cube() for _ in range(self.n_population - elite_size - 1)] + mutated_children + elites
            
            # Update fitness for new population
            fitness = self.__calculate_fitness(self.population)
            self.population = [self.population[i] for i in np.argsort(fitness)[-self.n_population:]]

        # Select best cube
        best_cube = min(self.population, key=lambda cube: cube.value)
        
        return {
            "iterations": self.n_generations,
            "initial_state": self.initial_state.cube.tolist(),
            "final_state": best_cube.cube.tolist(),
            "objective_value": int(best_cube.value),
            "min_cost_per_generation": self.min_cost_per_generation,
            "avg_cost_per_generation": self.avg_cost_per_generation,
        }