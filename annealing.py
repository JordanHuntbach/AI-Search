from helpful import *
import random
import math
import copy


# self explanatory - returns probability of accepting a new state
def prob_of_acceptance(new_length, current_length, temp):
    if new_length < current_length:
        return 1.0
    else:
        try:
            prob = math.exp((current_length - new_length) / temp)
            return prob
        except OverflowError:
            return 0


def simulated_annealing(start_temp, cooling_rate, tries, matrix):
    # set up variables
    temperature = start_temp
    path_length = len(matrix)
    # initialise random path to begin
    current_solution = random_path(path_length)
    current_length = evaluate_fitness(current_solution, matrix)
    # initialise best path variables
    best_solution = current_solution
    best_length = evaluate_fitness(best_solution, matrix)
    # loop until temperature is low enough
    while temperature > 0.2:
        # loop until a successor state is selected, or a sufficient number have been tried
        count = 1
        while count <= tries:
            # pick two cities and reverse the sub-path between them
            position1 = random.randint(0, path_length - 1)
            position2 = random.randint(0, path_length - 1)
            while position1 == position2:
                position2 = random.randint(0, path_length - 1)
            new_solution = copy.copy(current_solution)
            if position1 > position2:
                position1, position2 = position2, position1
            subset = new_solution[position1:position2]
            subset.reverse()
            new_solution = new_solution[:position1] + subset + new_solution[position2:]
            # evaluate new solution, and select it if path is short enough
            new_length = evaluate_fitness(new_solution, matrix)
            if new_length < best_length:
                best_length, best_solution = new_length, new_solution
                current_length, current_solution = new_length, new_solution
                count = tries
            elif prob_of_acceptance(new_length, current_length, temperature) >= random.random():
                current_solution = new_solution
                current_length = new_length
                count = tries
            count += 1
        # reduce temperature
        print(temperature)
        print(best_length)
        temperature *= (1 - cooling_rate)
    # return the best path and it's length
    return best_length, best_solution
