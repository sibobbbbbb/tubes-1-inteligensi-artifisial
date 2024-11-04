import numpy as np
import matplotlib.pyplot as plt
import time
from cube import Cube
import random


class SimulatedAnnealing:
    def __init__(self, initial_state: Cube, max_iter=100000, initial_temp=10000, cooling_rate=0.77, threshold=0.5):
        self.state = initial_state
        self.max_iter = max_iter
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.threshold = threshold
        self.best_state = initial_state.copy()
        self.best_value = self.state.value
        self.iteration = 0
        self.duration = 0
        self.objective_values = [self.state.value]
        self.stuck = 0
        self.eValue = []

    def find_random_neighbor(self):
        neighbor = self.state.cube.copy()
        x1, y1, z1 = np.random.randint(0, 5, 3)
        x2, y2, z2 = np.random.randint(0, 5, 3)
        
        while (x1, y1, z1) == (x2, y2, z2):
            x2, y2, z2 = np.random.randint(0, 5, 3)
        
        neighbor[x1, y1, z1], neighbor[x2, y2, z2] = neighbor[x2, y2, z2], neighbor[x1, y1, z1]
        return Cube(neighbor)
    
    def search(self):
        temperature = self.initial_temp
        start_time = time.time()

        for iteration in range(self.max_iter):
            self.iteration += 1
            neighbor = self.find_random_neighbor()
            neighbor_value = neighbor.value

            if neighbor_value < self.state.value:
                self.state = neighbor
                if neighbor_value < self.best_value:
                    self.best_state = neighbor
                    self.best_value = neighbor_value
            else:
                
                delta = neighbor_value - self.state.value
                acceptance_prob = np.exp(-delta / temperature)
                self.eValue.append(acceptance_prob)
                if acceptance_prob > self.threshold:
                    self.state = neighbor
                    if neighbor_value < self.best_value:
                        self.best_state = neighbor
                        self.best_value = neighbor_value
                else:
                    self.stuck += 1
                    self.state = self.state

            self.objective_values.append(self.state.value)

            temperature *= self.cooling_rate

            if self.best_value == 0 or temperature < 0.0000000000000000000000000000000000000001:
                break

        end_time = time.time()
        self.duration = end_time - start_time



# def run_simulated_annealing_experiments(initial_cube, S, n=5):
#     # Daftar nilai parameter yang ingin dicoba
#     initial_temps = [40000 ,10000, 7500]
#     cooling_rates = [0.9, 0.95]
#     max_iters = [20000,50000]
#     thresholds = [0.5 ,0.55, 0.65, 0.6, 0.7, 0.8]

#     # Simpan hasil terbaik
#     best_deviation = float('inf')
#     best_params = {}
#     results = []

#     for initial_temp in initial_temps:
#         for cooling_rate in cooling_rates:
#             for max_iter in max_iters:
#                 for threshold in thresholds:
#                     # Panggil fungsi simulated_annealing dengan kombinasi parameter
#                     final_cube, final_deviation, _, duration = simulated_annealing(
#                         cube=initial_cube, 
#                         S=S, 
#                         max_iter=max_iter, 
#                         initial_temp=initial_temp, 
#                         cooling_rate=cooling_rate, 
#                         threshold=threshold
#                     )
                    
#                     # Simpan hasilnya
#                     results.append({
#                         'initial_temp': initial_temp,
#                         'cooling_rate': cooling_rate,
#                         'max_iter': max_iter,
#                         'threshold': threshold,
#                         'final_deviation': final_deviation,
#                         'duration': duration
#                     })

#                     # Update hasil terbaik jika ditemukan deviasi lebih rendah
#                     if final_deviation < best_deviation:
#                         best_deviation = final_deviation
#                         best_params = {
#                             'initial_temp': initial_temp,
#                             'cooling_rate': cooling_rate,
#                             'max_iter': max_iter,
#                             'threshold': threshold
#                         }

#     # Tampilkan hasil eksperimen terbaik
#     print("Best Parameters Found:", best_params)
#     print("Best Final Deviation:", best_deviation)

#     # Tampilkan semua hasil eksperimen
#     for res in results:
#         print(f"Params: initial_temp={res['initial_temp']}, cooling_rate={res['cooling_rate']}, "
#               f"max_iter={res['max_iter']}, threshold={res['threshold']} - "
#               f"Final Deviation: {res['final_deviation']} - Duration: {res['duration']} seconds")
    
#     return best_params, best_deviation


# Run the Simulated Annealing algorithm
# initial_cube = initialize_cube(n)
# # final_cube, final_deviation, deviations, duration = simulated_annealing(initial_cube, S)
# best_params, best_deviation = run_simulated_annealing_experiments(initial_cube, S, n)

# # Output results
# print("Initial Cube State:\n", initial_cube)
# print("\nFinal Cube State:\n", final_cube)
# print("\nFinal Objective Function Value (Total Deviation):", final_deviation)
# print("Duration of Process:", duration, "seconds")

# # Plot the objective function value over iterations
# plt.plot(deviations)
# plt.xlabel("Iterations")
# plt.ylabel("Objective Function Value (Total Deviation)")
# plt.title("Objective Function Value over Iterations")
# plt.show()