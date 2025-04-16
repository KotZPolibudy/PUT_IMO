import time
from tabulate import tabulate
from utils import *
# starters
from starters.randomstart import randomstart
# algorithms
from algo.split_regret import split_paths_regret_TSP
from algo.traverse_steepest_edge import traverse_steepest_edge
from algo.steepest_LM import steepest_LM
from algo.steepest_kandydackie import steepest_kandydackie


def use_randomstart(distances):
    paths = randomstart(distances, choose_starting_nodes(data, distances))
    cost = summary_cost(*paths, distances)
    return paths, cost


def use_construction_algo(algo, distances, n=100):
    best_score = float('inf')
    worst_score = float('-inf')
    total_score = 0
    best_solution = None
    total_time = 0
    best_time = float('inf')
    worst_time = float('-inf')

    # do parallel here, please ;~;
    for _ in range(n):
        start_time = time.perf_counter()
        solution = algo(distances, choose_starting_nodes(data, distances))
        elapsed_time = time.perf_counter() - start_time
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

    return best_score, total_score / n, worst_score, best_solution, best_time, total_time / n, worst_time


def use_local_algo(algo, distances, n=100):
    best_score = float('inf')
    worst_score = float('-inf')
    total_score = 0
    best_solution = None
    total_time = 0
    best_time = float('inf')
    worst_time = float('-inf')
    total_diff = 0
    best_diff = 0

    # do parallel here, please ;~;
    for _ in range(n):
        start_time = time.perf_counter()
        start, starting_score = use_randomstart(distances)
        solution = algo(start, distances)
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

    return best_score, total_score / n, worst_score, best_solution, best_time, total_time / n, worst_time, best_diff, total_diff / n


if __name__ == '__main__':
    instances = [
        '../data/kroA200.tsp',
        '../data/kroB200.tsp'
        ]
    construction_algorithms = [
        split_paths_regret_TSP,
        # tu można dodać np. greedy cycle też z pierwszego, ale nasz był ofc lepszy
    ]
    local_algorithms = [
        traverse_steepest_edge,
        steepest_LM,
        steepest_kandydackie,
    ]

    results = []
    os.makedirs("../best_paths", exist_ok=True)
    for insta in instances:
        i = insta.split('/')[-1].split('.')[0]
        os.makedirs(f"../best_paths/{i}", exist_ok=True)

    for insta in instances:
        data = read_data(insta)
        distances = measure_distances(data)
        i = insta.split('/')[-1].split('.')[0]
        print(f"=============================={insta}==============================")

        for algorithm in construction_algorithms:
            algo_name = algorithm.__name__
            print(f"==============={algo_name}===============")
            found_best, found_avg, found_worst, found_best_paths, bt, avgt, wt = use_construction_algo(algorithm, distances)

            results.append(
                [insta, algo_name, found_best, found_avg, found_worst, bt, avgt, wt, None, None])
            save_path = f"../best_paths/{i}/{os.path.basename(algo_name)}.png"
            show_paths(data, *found_best_paths, save_path)

        for algorithm in local_algorithms:
            algo_name = algorithm.__name__
            print(f"==============={algo_name}===============")
            found_best, found_avg, found_worst, found_best_paths, bt, avgt, wt, diff_best, diff_avg = use_local_algo(
                algorithm, distances)

            results.append(
                [insta, algo_name, found_best, found_avg, found_worst, bt, avgt, wt, diff_best, diff_avg])
            save_path = f"../best_paths/{i}/{os.path.basename(algo_name)}.png"
            show_paths(data, *found_best_paths, save_path)

        # for algorithm in other_algorithms:
            # algo_name = algorithm.__name__
            # print(f"==============={algo_name}===============")
            # ... po prostu nasz algo z lokalnym przeszukiwaniem na sobie? - można dodać for fun, dla lepszego sprawka
            # bo on mam wrażenie docenia takie własne eksperymenty

    headers = ["Instance", "Algorytm", "Best", "Avg", "Worst", "Best Time", "Avg Time", "Worst Time", "Best Diff", "Avg Diff"]
    print(tabulate(results, headers=headers, tablefmt="grid"))
