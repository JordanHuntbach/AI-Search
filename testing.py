import math
import fileManager
from annealing import simulated_annealing
from genetic import genetic_algorithm


def algorithm_test(matrix, sim, tests):
    total = 0
    best_l = math.inf
    best_p = []
    for i in range(0, tests):
        if sim:
            result = simulated_annealing(start_temp=7500, cooling_rate=0.00001, tries=2, matrix=matrix)
        else:
            result = genetic_algorithm(matrix=matrix, pop_size=500, iterations=1250)
        total += result[0]
        if result[0] < best_l:
            best_l = result[0]
            best_p = result[1]
    average = total / tests
    print("Average:", average)
    print("Best:", best_l)
    return best_l, best_p


if __name__ == '__main__':
    simulated = True
    file_name = "AISearchfile175"
    data = fileManager.list_from_clean(file_name)
    test = algorithm_test(data, sim=simulated, tests=1)
    fileManager.write_tour_file(test[0], test[1], file_name, sim=simulated)
