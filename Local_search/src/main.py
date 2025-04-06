import time
from tabulate import tabulate
from utils import *
# starters
from starters.randomstart import randomstart
from starters.split_regret import split_paths_regret_TSP
# algorithms
from algo.traverse_greedy_edge import traverse_greedy_edge
from algo.traverse_greedy_vertex import traverse_greedy_vertex
from algo.traverse_steepest_edge import traverse_steepest_edge
from algo.traverse_steepest_vertex import traverse_steepest_vertex
from algo.traverse_random import traverse_random


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


def use_local_algo(algo, distances, starting_algo, random_time_limiter, n=100):
    best_score = float('inf')
    worst_score = float('-inf')
    total_score = 0
    best_solution = None
    total_time = 0
    best_time = float('inf')
    worst_time = float('-inf')
    elapsed_time = 0
    total_diff = 0
    best_diff = 0

    # do parallel here, please ;~;
    for _ in range(n):
        start, starting_score = use_starting_algo(starting_algo, distances)
        start_time = time.perf_counter()
        solution = algo(start, distances, random_time_limiter)
        elapsed_time = time.perf_counter() - start_time
        path1, path2 = solution
        score = summary_cost(path1, path2, distances)
        diff = starting_score - score
        total_score += score
        total_time += elapsed_time
        total_diff += diff
        if score < best_score:
            best_score = score
            best_solution = solution
        worst_score = max(worst_score, score)
        best_time = min(best_time, elapsed_time)
        worst_time = max(worst_time, elapsed_time)
        best_diff = max(best_diff, diff)

    return best_score, total_score / n, worst_score, best_solution, best_time, elapsed_time / n, worst_time, best_diff, total_diff / n


if __name__ == '__main__':
    instances = [
        '../data/kroA200.tsp',
        '../data/kroB200.tsp'
        ]
    algorithms = [
        traverse_greedy_edge,
        traverse_greedy_vertex,
        traverse_steepest_edge,
        traverse_steepest_vertex,
        traverse_random
    ]
    starting_algorithms = [
        split_paths_regret_TSP,
        randomstart,
    ]

    results = []
    os.makedirs("../best_paths", exist_ok=True)
    for insta in instances:
        i = insta.split('/')[-1].split('.')[0]
        os.makedirs(f"../best_paths/{i}", exist_ok=True)
        for algo in algorithms:
            os.makedirs(f"../best_paths/{i}/{algo.__name__}", exist_ok=True)

    for insta in instances:
        data = read_data(insta)
        distances = measure_distances(data)
        global_wt = 0.1
        i = insta.split('/')[-1].split('.')[0]
        print(f"=============================={insta}==============================")
        for algorithm in algorithms:
            algo_name = algorithm.__name__
            print(f"==============={algo_name}===============")
            for starting_algo in starting_algorithms:
                print(f"====={starting_algo.__name__}=====")
                found_best, found_avg, found_worst, found_best_paths, bt, avgt, wt, diff_best, diff_avg = use_local_algo(
                    algorithm, distances, starting_algo, global_wt
                )
                global_wt = max(global_wt, wt)

                results.append([insta, algo_name, starting_algo.__name__, found_best, found_avg, found_worst, bt, avgt, wt, diff_best, diff_avg])
                save_path = f"../best_paths/{i}/{algo_name}/{os.path.basename(starting_algo.__name__)}.png"
                show_paths(data, *found_best_paths, save_path)

    headers = ["Instance", "Algorytm", "Start Alg.", "Best", "Avg", "Worst", "Best Time", "Avg Time", "Worst Time", "Best Diff", "Avg Diff"]
    print(tabulate(results, headers=headers, tablefmt="grid"))
