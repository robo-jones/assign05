"""
For this assignment there is no automated testing. You will instead submit
your *.py file in Canvas. I will download and test your program from Canvas.
"""

import time
import random
import math


def adjMatFromFile(filename):
    """ Create an adj/weight matrix from a file with verts, neighbors, and weights. """
    f = open(filename, "r")
    n_verts = int(f.readline())
    print(f" n_verts = {n_verts}")
    adjmat = [[None] * n_verts for i in range(n_verts)]
    for i in range(n_verts):
        adjmat[i][i] = 0
    for line in f:
        int_list = [int(i) for i in line.split()]
        vert = int_list.pop(0)
        assert len(int_list) % 2 == 0
        n_neighbors = len(int_list) // 2
        neighbors = [int_list[n] for n in range(0, len(int_list), 2)]
        distances = [int_list[d] for d in range(1, len(int_list), 2)]
        for i in range(n_neighbors):
            adjmat[vert][neighbors[i]] = distances[i]
    f.close()
    return adjmat


def TSPwGenAlgo(g, max_num_generations=1000, population_size=50,
        mutation_rate=0.01, explore_rate=0.5):
    """ A genetic algorithm to attempt to find an optimal solution to TSP  """

    solution_cycle_distance = None # the distance of the final solution cycle/path
    solution_cycle_path = [] # the sequence of vertices representing final sol path to be returned
    shortest_path_each_generation = [] # store shortest path found in each generation
    num_verts = len(g[0])
    parent_cutoff_index = math.ceil(explore_rate * population_size)
    tournament_size = max(math.floor(0.1 * population_size), 2)

    # create individual members of the population
    population = [(0, list(range(num_verts))) for _ in range(population_size)]

    # initialize individuals to an initial 'solution'
    for (_, individual) in population:
        random.shuffle(individual)

    # loop for x number of generations (with possibly other early-stopping criteria)
    for _ in range(max_num_generations):
        # calculate fitness of each individual in the population
        for i in range(population_size):
            (_, path) = population[i]
            population[i] = (circuit_len(path, g), path)

        # (and append distance of the 'fittest' to shortest_path_each_generation)
        population.sort(key=lambda tup: tup[0])
        (shortest_path, _) = population[0]
        shortest_path_each_generation.append(shortest_path)

        # select the individuals to be used to spawn the generation, then create
        # individuals of the new generation (using some form of crossover)
        next_generation = []
        for _ in range(population_size):
            parent_1 = tournament_select(population[0:parent_cutoff_index], tournament_size)
            parent_2 = tournament_select(population[0:parent_cutoff_index], tournament_size)
            next_generation.append(cross(parent_1[1], parent_2[1]))

        # allow for mutations (this should not happen too often)
        for (_, individual) in next_generation:
            if (random.random() <= mutation_rate):
                swap1 = random.randrange(0, num_verts)
                swap2 = random.randrange(0, num_verts)
                individual[swap1], individual[swap2] = individual[swap2], individual[swap1]

        # ...
        population = next_generation

    # calculate and verify final solution, and update solution_cycle_distance,
    # solution_path, etc.
    population.sort(key=lambda tup: tup[0])
    (_, solution_cycle_path) = population[0]
    solution_cycle_distance = circuit_len(solution_cycle_path, g)
    # ...

    return {
            'solution': solution_cycle_path,
            'solution_distance': solution_cycle_distance,
            'evolution': shortest_path_each_generation
           }


def circuit_len(path, graph):
    """ Determine the length of the provided Hamiltonian circuit of the given graph. 
        Returns infinity if path is not a valid circuit. """
    try:
        length = 0
        for i in range(len(path) - 1):
            length += graph[path[i]][path[i + 1]]
        length += graph[path[i]][path[0]]
        return length
    except TypeError:
        return math.inf


def cross(parent_1, parent_2):
    """ Cross two parents to produce an offspring """
    parent_len = len(parent_1)
    cross_point_1 = random.randrange(0, parent_len)
    cross_point_2 = random.randrange(0, parent_len)
    crossStart = min(cross_point_1, cross_point_2)
    crossEnd = max(cross_point_1, cross_point_2)

    child = [None for _ in range(parent_len)]
    for i in range(crossStart, crossEnd):
        child[i] = parent_1[i]
    child_index = 0
    parent_index = 0
    while (child_index < crossStart):
        if (parent_2[parent_index] not in child):
            child[child_index] = parent_2[parent_index]
            child_index += 1
            parent_index += 1
        else:
            parent_index += 1
    child_index = crossEnd
    while (child_index < parent_len):
        if (parent_2[parent_index] not in child):
            child[child_index] = parent_2[parent_index]
            child_index += 1
            parent_index += 1
        else:
            parent_index += 1

    return (0, child)


def tournament_select(population, tournament_size):
    """ 'Tournament' selection: take a random sample of the population, and return the fittest member """
    contestants = []
    for _ in range(tournament_size):
        contestants.append(population[random.randrange(0, len(population))])
    contestants.sort(key=lambda tup: tup[0])
    return contestants[0]


def TSPwDynProg(g):
    """ (10pts extra credit) A dynamic programming approach to solve TSP """
    solution_cycle_distance = None # the distance of the final solution cycle/path
    solution_cycle_path = [] # the sequence of vertices representing final sol path to be returned

    #...

    return {
            'solution': solution_cycle_path,
            'solution_distance': solution_cycle_distance,
           }


def TSPwBandB(g):
    """ (10pts extra credit) A branch and bound approach to solve TSP """
    solution_cycle_distance = None # the distance of the final solution cycle/path
    solution_cycle_path = [] # the sequence of vertices representing final sol path to be returned

    #...

    return {
            'solution': solution_cycle_path,
            'solution_distance': solution_cycle_distance,
           }


def assign05_main():
    """ Load the graph (change the filename when you're ready to test larger ones) """
    g = adjMatFromFile("complete_graph_n08.txt")

    # Run genetic algorithm to find best solution possible
    start_time = time.time()
    res_ga = TSPwGenAlgo(g)
    elapsed_time_ga = time.time() - start_time
    print(f"GenAlgo runtime: {elapsed_time_ga:.2f}")
    print(f"  sol dist: {res_ga['solution_distance']}")
    print(f"  sol path: {res_ga['solution']}")

    # (Try to) run Dynamic Programming algorithm only when n_verts <= 10
    if len(g) <= 10:
        start_time = time.time()
        res_dyn_prog = TSPwDynProg(g)
        elapsed_time = time.time() - start_time
        if len(res_dyn_prog['solution']) == len(g) + 1:
            print(f"Dyn Prog runtime: {elapsed_time:.2f}")
            print(f"  sol dist: {res_dyn_prog['solution_distance']}")
            print(f"  sol path: {res_dyn_prog['solution']}")

    # (Try to) run Branch and Bound only when n_verts <= 10
    if len(g) <= 10:
        start_time = time.time()
        res_bnb = TSPwBandB(g)
        elapsed_time = time.time() - start_time
        if len(res_bnb['solution']) == len(g) + 1:
            print(f"Branch & Bound runtime: {elapsed_time:.2f}")
            print(f"  sol dist: {res_bnb['solution_distance']}")
            print(f"  sol path: {res_bnb['solution']}")


# Check if the program is being run directly (i.e. not being imported)
if __name__ == '__main__':
    assign05_main()

