from helpful import *
import random
from operator import itemgetter


# returns two children from two given parents
def breeding(parent1, parent2, mutation):
    # BREEDING
    # convert type if necessary (to lists of integers)
    if type(parent1) is str:
        parent1 = list_to_ints(string_to_list(parent1))
        parent2 = list_to_ints(string_to_list(parent2))
    # get crossover point
    length = len(parent1)
    crossover = random.randint(1, length - 1)
    # set child cities up to crossover point
    child1 = parent1[:crossover]
    child2 = parent2[:crossover]
    # set child cities after crossover point
    for k in range(0, length):
        if parent2[k] not in child1:
            child1.append(parent2[k])
        if parent1[k] not in child2:
            child2.append(parent1[k])
    # MUTATION
    rand = random.random()
    if mutation >= rand:
        # select two cities to swap
        bit1 = random.randint(0, length - 1)
        bit2 = random.randint(0, length - 1)
        while bit1 == bit2:
            bit2 = random.randint(0, length - 1)
        if bit1 > bit2:
            bit1, bit2 = bit2, bit1
        subset = child1[bit1:bit2]
        subset.reverse()
        child1 = child1[:bit1] + subset + child1[bit2:]
        subset = child2[bit1:bit2]
        subset.reverse()
        child2 = child2[:bit1] + subset + child2[bit2:]

    # returns list of integers (the new offspring from given parents)
    return child1, child2


# returns the parents that will go on to breed in the genetic algorithm
def breeding_selection(population, tournament_size, p):
    parents = []
    # loop twice (once for each parent)
    for i in range(0, 2):
        # randomly select members from the population to compete in the tournament
        tournament = []
        for j in range(0, int(tournament_size * len(population))):
            tournament.append(random.choice(population))
        # order the tournament members by fitness (highest to lowest)
        tournament_ord = sorted(list_to_dict(tournament).items(), key=itemgetter(1), reverse=False)
        # get random float in (0,1)
        rand = random.random()
        # set the probability of the fittest member of the tournament being selected
        criteria = p
        # count is the index of the winner of the tournament
        count = 0
        # find the tournament winner - the fittest member if p >= rand
        if criteria >= rand:
            parents.append(tournament_ord[count][0])
        # if the fittest member is not selected, 'criteria' is increased until it's greater than 'rand'
        else:
            # the more times 'criteria' has to be increased, the weaker the winner of the tournament will be
            while rand > criteria:
                count += 1
                criteria += criteria * p
            # if the count is greater than the size of the tournament, the winner is weakest member
            if count >= len(tournament_ord):
                parents.append(tournament_ord[len(tournament_ord) - 1][0])
            # else, the winner is the member with index count
            else:
                parents.append(tournament_ord[count][0])
    return parents


def genetic_algorithm(matrix, pop_size, iterations):
    # define parameters
    path_length = len(matrix)
    population = {}
    sorted_pop = []
    # loop for number of generations
    for i in range(1, iterations + 1):
        print(i)
        # fill up population with random paths if the population is smaller than desired
        while len(population) < pop_size:
            path = random_path(path_length)
            population[str(path)] = evaluate_fitness(path, matrix)
        # get a sorted list of tuples representing paths and their lengths
        sorted_pop = sorted(population.items(), key=itemgetter(1), reverse=False)
        # remove the less fit paths
        indices = []
        for j in range(pop_size):
            prob = (j / pop_size) ** 0.5
            if random.random() <= prob:
                indices.append(j)
        count = 0
        for index in indices:
            sorted_pop.pop(index - count)
            count += 1
        # find how many new paths are required to fill the population
        required_new = pop_size - len(sorted_pop)
        new = []
        # go through breeding and add children to a temporary list
        for k in range(0, required_new // 2):
            parent1, parent2 = breeding_selection(sorted_pop, tournament_size=0.25, p=0.60)
            child1, child2 = breeding(parent1, parent2, mutation=0.75)
            new.append(child1)
            new.append(child2)
        # refresh the population as a dictionary
        population = list_to_dict(sorted_pop)
        # evaluate fitness of children and store in the population dictionary
        for each in new:
            population[str(each)] = evaluate_fitness(each, matrix)
        print(sorted_pop[0][1])
    print("Genetic length:", sorted_pop[0][1])
    return sorted_pop[0][1], string_to_list(sorted_pop[0][0])
