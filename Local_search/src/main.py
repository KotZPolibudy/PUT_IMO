import time
from utils import *
# starters
from starters.randomstart import randomstart
from starters.split_regret import split_paths_regret_TSP
# algorithms
from algo.random import traverse_random
from algo.traverse_greedy import traverse_greedy


def use_starting_algo(algorithm, distances, n=1):
    # n = 1, bo to tylko startowe
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

    # return best_cost, total_cost / n, worst_cost, best_paths
    return best_paths, best_cost


def use_local_algo(algo, start, distances, n=100):
    best_score = float('inf')
    worst_score = float('-inf')
    total_score = 0
    best_solution = None
    total_time = 0
    best_time = float('inf')
    worst_time = float('-inf')

    for _ in range(n):
        start_time = time.time()
        solution = algo(start, distances)
        elapsed_time = time.time() - start_time
        path1, path2 = solution
        score = summary_cost(path1, path2, distances)
        total_score += score
        total_time += elapsed_time
        if score < best_score:
            best_score = score
            best_solution = solution
        worst_score = max(worst_score, score)
        best_time = min(best_time, elapsed_time)
        worst_time = max(worst_time, elapsed_time)

    return best_score, total_score / n, worst_score, best_solution, best_time, elapsed_time / n, worst_time


if __name__ == '__main__':
    instances = ['../data/kroA200.tsp', '../data/kroB200.tsp']
    algorithms = [
        traverse_random,
        traverse_greedy
    ]
    starting_algorithms = [
        randomstart,
        split_paths_regret_TSP
    ]

    results = {}
    os.makedirs("../best_paths", exist_ok=True)

    for insta in instances:
        data = read_data(insta)
        distances = measure_distances(data)
        for algorithm in algorithms:
            algo_name = algorithm.__name__
            for starting_algo in starting_algorithms:
                starting_paths, start_best = use_starting_algo(starting_algo, distances)

                found_best, found_avg, found_worst, found_best_paths, bt, avgt, wt = use_local_algo(
                    algorithm, starting_paths, distances)
                diff = start_best - found_best

                results[(algo_name, starting_algo.__name__, insta)] = (found_best, found_avg, found_worst, bt, avgt, wt, diff)

    # Print results in table format
    header = "Algorytm | Start Alg. | Instance | Best | Avg | Worst | Time | Diff"
    print(header)
    print("-" * len(header))
    for (algo, start_algo, instance), values in results.items():
        print(f"{algo} | {start_algo} | {instance} | " + " | ".join(map(str, values)))
