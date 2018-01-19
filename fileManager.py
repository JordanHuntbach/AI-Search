from helpful import *


def clean(name):
    filename = name + ".txt"
    file = open("./raw/" + filename, "r")
    read = file.read()
    file.close()
    read = read.lower().replace("\n", "").replace("\r", "").split("=")[2]
    read = re.sub("[^,|\d]", "", read)
    numbers = read.split(",")
    size = int(numbers[0])
    numbers = numbers[1::]
    array = []
    for num in range(1, size + 1):
        array.append([])
        for city in range(1, size + 1):
            if num == city:
                array[num - 1].append(0)
            elif city < num:
                array[num - 1].append(array[city - 1][num - 1])
            else:
                distance = int(numbers[0])
                numbers = numbers[1::]
                array[num - 1].append(distance)
    clean_name = name + "Clean.txt"
    file = open("./clean/" + clean_name, "w")
    file.write("NAME = " + name + "\n")
    file.write("SIZE = " + str(size) + "\n")
    for line in array:
        file.write(str(line) + "\n")
    file.close()
    return array


# returns a 2d list (must be run on a 'clean' file)
def list_from_clean(name):
    filename = "./clean/" + name + "Clean.txt"
    file = open(filename, "r")
    list_out = []
    i = 0
    # ignores the first two lines, then converts each line to a list of distances
    for line in file:
        i += 1
        if i > 2:
            list_out.append(list_to_ints(string_to_list(line)))
    file.close()
    return list_out


def write_tour_file(length, tour, filename, sim):
    if sim:
        name = "./SAtours/tour" + filename + ".txt"
    else:
        name = "./GAtours/tour" + filename + ".txt"
    target = ""
    file = open(name, "r")
    for line in file:
        if line.startswith("LENGTH"):
            target = line
    file.close()
    best = int(target[9:len(target) - 2])
    if length <= best:
        file = open(name, "w")
        file.write("NAME = " + filename + ",\n")
        file.write("TOURSIZE = " + str(len(tour)) + ",\n")
        file.write("LENGTH = " + str(length) + ",\n")
        file.write(list_to_string(list_to_ints(tour)))
        file.close()


if __name__ == '__main__':
    clean("AISearchfile180")
