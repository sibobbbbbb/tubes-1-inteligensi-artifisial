import random
import numpy as np
from collections import Counter
import time
import matplotlib.pyplot as plt

def genetic_algorithm(n_population, n_generations=100, elitism_rate=0.1):
    start_time = time.time()

    # State awal dari kubus
    cubes = random_population(n_population)
    initial_state = cubes[0].copy()  # Menyimpan state awal dari kubus pertama
    
    max_fitness_per_generation = []
    avg_fitness_per_generation = []
    
    elite_size = max(1, int(n_population * elitism_rate)) 

    for generation in range(n_generations):
        mutation_rate = max(0.05, 0.2 * (1 - generation / n_generations))
        
        fitness = count_fitness(cubes)
        sorted_indices = np.argsort(fitness)
        
        # Simpan nilai fitness maksimum dan rata-rata untuk plotting
        max_fitness_per_generation.append(np.max(fitness))
        avg_fitness_per_generation.append(np.mean(fitness))
        
        # Pertahankan beberapa individu elit
        elites = [cubes[i] for i in sorted_indices[-elite_size:]]
        
        cumulative_probabilities = count_probability_random(fitness)
        selected_cubes = selection(cumulative_probabilities, cubes)
        results = crossover(selected_cubes)
        final = mutation(results, mutation_rate)
        
        # Buat populasi generasi berikutnya
        cubes = random_population(n_population - elite_size - 1) + list(final) + elites
        fitness = count_fitness(cubes)
        
        # Seleksi kembali populasi terbaik
        cubes = [cubes[i] for i in np.argsort(fitness)[-n_population:]]

    cost_and_cubes = [(calculate_cost(cube, 315), cube) for cube in cubes]
    cost, best_array = min(cost_and_cubes, key=lambda x: x[0])
    
    end_time = time.time()
    execution_time = end_time - start_time

    # Plot 
    plt.plot(range(n_generations), max_fitness_per_generation, label="Max Fitness")
    plt.plot(range(n_generations), avg_fitness_per_generation, label="Average Fitness")
    plt.xlabel("Generasi")
    plt.ylabel("Fitness")
    plt.title("Fitness terhadap Generasi")
    plt.legend()
    plt.show()

    # Output 
    print("State awal dari kubus:")
    print(initial_state)
    print("\nState akhir dari kubus terbaik:")
    print(best_array)
    print("\nNilai objective function akhir yang dicapai:", cost)
    print("Jumlah populasi:", n_population)
    print("Banyak iterasi:", n_generations)
    print("Durasi proses pencarian:", execution_time, "detik")

    return cost, best_array

def calculate_cost(cube, magic_number):
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

def random_population(n_population):
    cubes = []
    for _ in range(n_population):
        cube = np.arange(1, 126)
        np.random.shuffle(cube)
        cube = cube.reshape((5, 5, 5))
        cubes.append(cube)
    return cubes

def count_fitness(cubes):
    fitness = []
    for cube in (cubes):
        fitness.append(1 / (1 + calculate_cost(cube,315)))
    return fitness

def count_probability_random(fitness):
    probabilities = []
    total = sum(fitness)
    for value in (fitness):
        probabilities.append(value/total)
    cumulative_probabilities = []
    cumulative_sum = 0
    for p in probabilities:
        cumulative_sum += p
        cumulative_probabilities.append(cumulative_sum)
    return cumulative_probabilities

def selection(cumulative_probabilities,cubes):
    selected_cube = []
    for _ in range(2):
        r = random.random()
        for i, cp in enumerate(cumulative_probabilities):
            if r <= cp:
                selected_cube.append(cubes[i].copy())
                break
    return selected_cube
        
def crossover(selected_cubes):
    crossover_point1 = random.randint(0, 124)
    crossover_point2 = random.randint(crossover_point1, 124)
    
    # Flatten menjadi 1D untuk crossover
    cube1 = np.array(selected_cubes[0]).flatten()
    cube2 = np.array(selected_cubes[1]).flatten()
    
    # Buat anak dengan menukar bagian antara dua titik crossover
    child1 = np.concatenate((cube1[:crossover_point1], cube2[crossover_point1:crossover_point2], cube1[crossover_point2:])).reshape((5, 5, 5))
    child2 = np.concatenate((cube2[:crossover_point1], cube1[crossover_point1:crossover_point2], cube2[crossover_point2:])).reshape((5, 5, 5))
    
    return np.array([child1, child2])

def mutation(results,mutation_rate = 0.1):
    final = []
    for i in range(2):
    
        if (not is_cube_unique(results[i])):
            # Hitung kemunculan tiap elemen
            element_counts = Counter(results[i].flatten())
            
            # Cari elemen duplikat dan elemen yang hilang
            duplicates = [item for item, count in element_counts.items() if count > 1]
            missing = [num for num in range(1, 126) if num not in element_counts]
            
            # Ganti elemen duplikat dengan elemen yang hilang
            for duplicate, miss in zip(duplicates, missing):
                duplicate_index = np.where(results[i] == duplicate)
                if len(duplicate_index[0]) > 0:
                    results[i][duplicate_index[0][0], duplicate_index[1][0], duplicate_index[2][0]] = miss
        
        if random.random() < mutation_rate:
            # Pilih dua posisi acak untuk ditukar dalam `results[i]`
            idx1, idx2 = random.sample(range(125), 2)
            pos1 = np.unravel_index(idx1, (5, 5, 5))
            pos2 = np.unravel_index(idx2, (5, 5, 5))
            # Tukar elemen di dua posisi acak tersebut
            results[i][pos1], results[i][pos2] = results[i][pos2], results[i][pos1]
        
        current_63_position = np.argwhere(results[i] == 63)
        
        # Jika ada lebih dari satu nilai 63, abaikan semua kecuali yang pertama ditemukan
        if len(current_63_position) > 1:
            # Ganti semua nilai 63 tambahan menjadi nilai yang hilang (contohnya, `missing[0]`)
            for extra_63_position in current_63_position[1:]:
                results[i][tuple(extra_63_position)] = missing.pop(0)
            current_63_position = current_63_position[:1]  # Hanya sisakan satu posisi 63
        
        # Jika nilai 63 tidak berada di posisi tengah, tukar dengan nilai yang ada di tengah
        if tuple(current_63_position[0]) != (2, 2, 2):
            temp = results[i][2][2][2]  # Simpan nilai di tengah
            results[i][2][2][2] = 63
            results[i][tuple(current_63_position[0])] = temp
            
        final.append(results[i])
    
    final = np.array(final)
    return final

def is_cube_unique(cube):
    flattened_cube = cube.flatten()
    return len(flattened_cube) == len(set(flattened_cube))

# start_time = time.time()
# cost, best_array = genetic_algorithm(n_population=200, n_generations=100)
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Waktu eksekusi: {execution_time} detik")
# print(cost)

# genetic_algorithm(n_population=50, n_generations=100)