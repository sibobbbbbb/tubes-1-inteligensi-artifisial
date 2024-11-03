import numpy as np
import random
import matplotlib.pyplot as plt
import time

# Define the side length of the cube
n = 5
# Calculate the magic constant (S) for a 5x5x5 magic cube
S = n * (n**3 + 1) // 2

# Initialize a 5x5x5 cube with values 1 to 125
def initialize_cube(n):
    numbers = np.arange(1, n**3 + 1)
    np.random.shuffle(numbers)
    cube = numbers.reshape((n, n, n))
    return cube

# Objective function to calculate the total deviation
# def calculate_total_deviation(cube, S):
#     deviation = 0
#     # Sum of each row, column, pillar (z-axis), and diagonals
#     for i in range(n):
#         deviation += abs(np.sum(cube[i, :, :]) - S)  # row sums
#         deviation += abs(np.sum(cube[:, i, :]) - S)  # column sums
#         deviation += abs(np.sum(cube[:, :, i]) - S)  # pillar sums

#     # Diagonals in each face (3 sets per axis)
#     for i in range(n):
#         deviation += abs(np.sum(cube[i, :, :].diagonal()) - S)  # diagonal in XY plane
#         deviation += abs(np.sum(np.fliplr(cube[i, :, :]).diagonal()) - S)
        
#         deviation += abs(np.sum(cube[:, i, :].diagonal()) - S)  # diagonal in XZ plane
#         deviation += abs(np.sum(np.fliplr(cube[:, i, :]).diagonal()) - S)
        
#         deviation += abs(np.sum(cube[:, :, i].diagonal()) - S)  # diagonal in YZ plane
#         deviation += abs(np.sum(np.fliplr(cube[:, :, i]).diagonal()) - S)

#     # Space diagonals (4 in total)
#     deviation += abs(np.sum([cube[i, i, i] for i in range(n)]) - S)
#     deviation += abs(np.sum([cube[i, i, n-1-i] for i in range(n)]) - S)
#     deviation += abs(np.sum([cube[i, n-1-i, i] for i in range(n)]) - S)
#     deviation += abs(np.sum([cube[n-1-i, i, i] for i in range(n)]) - S)

#     return deviation

def calculate_total_deviation(cube, magic_number):
    cost = 0
    
    n = len(cube)
    # 1. Hitung cost untuk setiap baris di setiap layer
    for layer in cube:
        for row in layer:
            cost += abs(sum(row) - magic_number)
    
    # 2. Hitung cost untuk setiap kolom di setiap layer
    for layer in cube:
        for col in range(n):
            column_sum = sum(layer[row][col] for row in range(n))
            cost += abs(column_sum - magic_number)
    
    # 3. Hitung cost untuk setiap tiang (melintasi layer z untuk setiap (x, y) pada layer)
    for x in range(n):
        for y in range(n):
            column_sum = sum(cube[z][x][y] for z in range(n))
            cost += abs(column_sum - magic_number)
    
    # 4. Hitung cost untuk diagonal pada setiap bidang (xy, xz, yz)
    # Diagonal pada bidang xy
    for z in range(n):
        diag1 = sum(cube[z][i][i] for i in range(n))
        diag2 = sum(cube[z][i][n - i - 1] for i in range(n))
        cost += abs(diag1 - magic_number)
        cost += abs(diag2 - magic_number)
    
    # Diagonal pada bidang xz
    for y in range(n):
        diag1 = sum(cube[i][y][i] for i in range(n))
        diag2 = sum(cube[i][y][n - i - 1] for i in range(n))
        cost += abs(diag1 - magic_number)
        cost += abs(diag2 - magic_number)
    
    # Diagonal pada bidang yz
    for x in range(n):
        diag1 = sum(cube[i][i][x] for i in range(n))
        diag2 = sum(cube[i][n - i - 1][x] for i in range(n))
        cost += abs(diag1 - magic_number)
        cost += abs(diag2 - magic_number)
    
    # 5. Hitung cost untuk diagonal ruang (melintasi sudut ke sudut kubus)
    diag1 = sum(cube[i][i][i] for i in range(n))
    diag2 = sum(cube[i][i][n - i - 1] for i in range(n))
    diag3 = sum(cube[i][n - i - 1][i] for i in range(n))
    diag4 = sum(cube[i][n - i - 1][n - i - 1] for i in range(n))
    cost += abs(diag1 - magic_number)
    cost += abs(diag2 - magic_number)
    cost += abs(diag3 - magic_number)
    cost += abs(diag4 - magic_number)
    
    return int(cost)

# Simulated Annealing algorithm
def simulated_annealing(cube, S, max_iter=100000, initial_temp=10000, cooling_rate=0.77, threshold=0.5):
    current_cube = cube.copy()
    current_deviation = calculate_total_deviation(current_cube, S)
    best_cube = current_cube.copy()
    best_deviation = current_deviation
    deviations = [current_deviation]
    
    temperature = initial_temp
    start_time = time.time()

    for iteration in range(max_iter):
        # Randomly select two positions to swap
        x1, y1, z1 = np.random.randint(0, n, 3)
        x2, y2, z2 = np.random.randint(0, n, 3)
        while (x1, y1, z1) == (x2, y2, z2):  
            x2, y2, z2 = np.random.randint(0, n, 3)

        current_cube[x1, y1, z1], current_cube[x2, y2, z2] = current_cube[x2, y2, z2], current_cube[x1, y1, z1]
        new_deviation = calculate_total_deviation(current_cube, S)

        if new_deviation < current_deviation:
            current_deviation = new_deviation
            if current_deviation < best_deviation:
                best_deviation = current_deviation
                best_cube = current_cube.copy()
        elif np.exp((current_deviation - new_deviation) / temperature) > threshold :
            current_deviation = new_deviation
            if current_deviation < best_deviation:
                best_deviation = current_deviation
                best_cube = current_cube.copy()
        else:
            # Revert the swap if not accepted
            current_cube[x1, y1, z1], current_cube[x2, y2, z2] = current_cube[x2, y2, z2], current_cube[x1, y1, z1]

        deviations.append(current_deviation)

        # Cooling schedule
        temperature *= cooling_rate
        if current_deviation == 0:
            break

        if temperature < 1 :
            break

    end_time = time.time()
    duration = end_time - start_time

    return best_cube, best_deviation, deviations, duration


def run_simulated_annealing_experiments(initial_cube, S, n=5):
    # Daftar nilai parameter yang ingin dicoba
    initial_temps = [10000, 7500, 5000, 2500, 1000]
    cooling_rates = [0.9, 0.95]
    max_iters = [10000, 20000]
    thresholds = [0.5 ,0.55, 0.65, 0.6, 0.7, 0.8]

    # Simpan hasil terbaik
    best_deviation = float('inf')
    best_params = {}
    results = []

    for initial_temp in initial_temps:
        for cooling_rate in cooling_rates:
            for max_iter in max_iters:
                for threshold in thresholds:
                    # Panggil fungsi simulated_annealing dengan kombinasi parameter
                    final_cube, final_deviation, _, duration = simulated_annealing(
                        cube=initial_cube, 
                        S=S, 
                        max_iter=max_iter, 
                        initial_temp=initial_temp, 
                        cooling_rate=cooling_rate, 
                        threshold=threshold
                    )
                    
                    # Simpan hasilnya
                    results.append({
                        'initial_temp': initial_temp,
                        'cooling_rate': cooling_rate,
                        'max_iter': max_iter,
                        'threshold': threshold,
                        'final_deviation': final_deviation,
                        'duration': duration
                    })

                    # Update hasil terbaik jika ditemukan deviasi lebih rendah
                    if final_deviation < best_deviation:
                        best_deviation = final_deviation
                        best_params = {
                            'initial_temp': initial_temp,
                            'cooling_rate': cooling_rate,
                            'max_iter': max_iter,
                            'threshold': threshold
                        }

    # Tampilkan hasil eksperimen terbaik
    print("Best Parameters Found:", best_params)
    print("Best Final Deviation:", best_deviation)

    # Tampilkan semua hasil eksperimen
    for res in results:
        print(f"Params: initial_temp={res['initial_temp']}, cooling_rate={res['cooling_rate']}, "
              f"max_iter={res['max_iter']}, threshold={res['threshold']} - "
              f"Final Deviation: {res['final_deviation']} - Duration: {res['duration']} seconds")
    
    return best_params, best_deviation


# Run the Simulated Annealing algorithm
initial_cube = initialize_cube(n)
# final_cube, final_deviation, deviations, duration = simulated_annealing(initial_cube, S)
best_params, best_deviation = run_simulated_annealing_experiments(initial_cube, S, n)

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