import re
import random


def string_to_list(string):
    string = re.sub("[^,|\d]", "", string)
    return_list = string.split(",")
    return return_list


def list_to_ints(list_in):
    output = []
    for each in list_in:
        output.append(int(each))
    return output


def list_to_string(list_in):
    string = ''
    for each in list_in:
        string += str(each) + ','
    return string[:-1]


def list_to_dict(list_in):
    dictionary = {}
    for item in list_in:
        dictionary[item[0]] = item[1]
    return dictionary


# returns a list of integers representing a path through cities e.g [1, 3, 4, 2] - not zero indexed.
def random_path(length):
    path = [i for i in range(1, length + 1)]
    random.shuffle(path)
    return path


# find the length of the tour
def evaluate_fitness(genotype, matrix):
    # convert path type if necessary to a list of ints
    if type(genotype) is str:
        genotype = string_to_list(genotype)
    if type(genotype[0]) is not int:
        genotype = list_to_ints(genotype)
    # for every city in path, add distance to next city
    length = matrix[genotype[0] - 1][genotype[len(genotype) - 1] - 1]
    for i in range(0, len(genotype) - 1):
        length += matrix[genotype[i] - 1][genotype[i + 1] - 1]
    # return total distance
    return length
