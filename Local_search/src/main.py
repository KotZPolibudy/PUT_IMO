import os

# from TSP_heuristic.src.algo.greedy_near import greedy_nearest_neighbor
from utils import *


def algorithm_loop(_, __, ___):
    # TODO
    best_score, avg_score, worst_score = 0, 0, 0
    best_solution = [[], []]
    return best_score, avg_score, worst_score, best_solution


def use_starting_algo(algorithm, distances, n=100):
    best_cost = float('inf')
    worst_cost = float('-inf')
    total_cost = 0
    best_paths = None

    for _ in range(n):
        paths = algorithm(distances, choose_starting_nodes(data, distances))
        if paths is None:
            return None, None, None, None
        cost = summary_cost(*paths, distances)
        total_cost += cost
        if cost < best_cost:
            best_cost = cost
            best_paths = paths
        worst_cost = max(worst_cost, cost)

    return best_cost, total_cost / n, worst_cost, best_paths


def use_local_algo(algo, start, distances):
    best_score = 0
    best_solution = None
    best_score, best_solution = algo(start, distances)
    return best_score, best_solution


if __name__ == '__main__':
    instances = ['../data/kroA200.tsp', '../data/kroB200.tsp']
    algorithms = []
    starting_algorithms = []

    results = {}
    os.makedirs("../best_paths", exist_ok=True)

    for insta in instances:
        data = read_data(insta)
        distances = measure_distances(data)
        for algorithm in algorithms:
            algo_name = algorithm.__name__
            for starting_algo in starting_algorithms:
                start_best, start_avg, start_worst, starting_paths = use_starting_algo(starting_algo, distances)

                # use algo
                found_best, found_best_paths = use_local_algo(algorithm, starting_paths, distances)
                diff = start_best - found_best

    # Print results in table format
    header = "Algorytm | " + " | ".join(instances)
    print(header)
    print("-" * len(header))
    for algo, values in results.items():
        print(f"{algo} | " + " | ".join(values))
