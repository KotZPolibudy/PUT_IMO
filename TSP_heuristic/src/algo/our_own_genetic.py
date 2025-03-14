import numpy as np
import random


def evaluate_fitness(cycle1, cycle2, distances):
    def path_length(path):
        return sum(distances[path[i]][path[i + 1]] for i in range(len(path) - 1)) + distances[path[-1]][path[0]]
    return path_length(cycle1) + path_length(cycle2)


def initialize_population(n, num_individuals):
    cities = list(range(n))
    population = []
    for _ in range(num_individuals):
        random.shuffle(cities)
        cycle1, cycle2 = cities[:n//2], cities[n//2:]
        population.append((cycle1, cycle2))
    return population


def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]
    fill_values = [x for x in parent2 if x not in child]
    fill_idx = (i for i in range(size) if child[i] is None)
    for idx in fill_idx:
        child[idx] = fill_values.pop(0)
    return child


def mutate(path):
    i, j = random.sample(range(len(path)), 2)
    path[i], path[j] = path[j], path[i]


def genetic_algo(distances, num_generations=100, population_size=50, mutation_rate=0.2):
    n = len(distances)
    population = initialize_population(n, population_size)
    for _ in range(num_generations):
        population = sorted(population, key=lambda p: evaluate_fitness(*p, distances))
        new_population = population[:10]  # Elitism
        while len(new_population) < population_size:
            p1, p2 = random.sample(population[:25], 2)  # Tournament selection
            child1 = order_crossover(p1[0], p2[0]), order_crossover(p1[1], p2[1])
            if random.random() < mutation_rate:
                mutate(child1[0])
                mutate(child1[1])
            new_population.append(child1)
        population = new_population
    return population[0]


def genetic_2tsp(_, distances, __):
    return genetic_algo(distances)
