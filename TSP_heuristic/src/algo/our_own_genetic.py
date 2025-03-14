# No więc, na ten algorytm nie patrzymy, bo to absolutne gówno, które nie działa XDDD
import random


def evaluate_fitness(cycle1, cycle2, distances):
    def path_length(path):
        return sum(distances[path[i]][path[i + 1]] for i in range(len(path) - 1)) + distances[path[-1]][path[0]]

    return path_length(cycle1) + path_length(cycle2)


def nearest_neighbor_split(distances):
    n = len(distances)
    cities = list(range(n))
    random.shuffle(cities)
    cycle1, cycle2 = [cities.pop()], [cities.pop()]
    while cities:
        next_city = min(cities, key=lambda c: min(distances[c][cycle1[-1]], distances[c][cycle2[-1]]))
        if len(cycle1) < len(cycle2):
            cycle1.append(next_city)
        else:
            cycle2.append(next_city)
        cities.remove(next_city)
    return cycle1, cycle2


def initialize_population(n, num_individuals, distances):
    population = [nearest_neighbor_split(distances) for _ in range(num_individuals)]
    return population


def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]
    fill_values = [x for x in parent2 if x not in child]
    missing_values = [x for x in range(size) if x not in child]
    random.shuffle(missing_values)
    fill_idx = (i for i in range(size) if child[i] is None)
    for idx in fill_idx:
        if fill_values:
            child[idx] = fill_values.pop(0)
        else:
            child[idx] = missing_values.pop(0)
    return child


def swap_between_cycles(cycle1, cycle2):
    i, j = random.randint(0, len(cycle1) - 1), random.randint(0, len(cycle2) - 1)
    cycle1[i], cycle2[j] = cycle2[j], cycle1[i]


def genetic_algorithm(distances, num_generations=100, population_size=50, mutation_rate=0.2):
    n = len(distances)
    population = initialize_population(n, population_size, distances)
    for _ in range(num_generations):
        population = sorted(population, key=lambda p: evaluate_fitness(*p, distances))
        new_population = population[:10]  # Elitism
        while len(new_population) < population_size:
            p1, p2 = random.sample(population[:25], 2)  # Tournament selection
            child1 = order_crossover(p1[0], p2[0]), order_crossover(p1[1], p2[1])
            if random.random() < mutation_rate:
                swap_between_cycles(child1[0], child1[1])
            new_population.append(child1)
        population = new_population
    return population[0]


def genetic_2tsp(_, distances, __):
    return genetic_algorithm(distances)
