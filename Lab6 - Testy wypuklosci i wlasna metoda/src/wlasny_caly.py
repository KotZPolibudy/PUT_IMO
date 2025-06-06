import time
from tabulate import tabulate
from utils import *
# starters
from algo.randomstart import randomstart
from algo.split_regret_starter import split_paths_regret_TSP
from algo.spectral_split_two_regret import spectral_split_two_regret
# algorithms
from algo.MSLS import MSLS
from algo.ILS import ILS
from algo.LNS import LNS
from algo.LNS_no_LS import LNS_no_LS


def use_start(distances, starters, n=100):

    best_paths = randomstart(distances, choose_starting_nodes(data, distances))
    best_koszt = summary_cost(*best_paths, distances)

    for starter in starters:
        for i in range(n):
            paths = starter(distances, choose_starting_nodes(data, distances))
            koszt = summary_cost(*paths, distances)
            if koszt < best_koszt:
                best_koszt = koszt
                best_paths = paths

    return best_paths, best_koszt

def use_local_algo(algo, distances, time_limiter=None, starters_list=None, n=3):
    if starters_list is None:
        starters_list = [randomstart, split_paths_regret_TSP, spectral_split_two_regret]
    best_score = float('inf')
    worst_score = float('-inf')
    total_score = 0
    best_solution = None
    total_time = 0
    best_time = float('inf')
    worst_time = float('-inf')
    total_diff = 0
    best_diff = 0
    all_num_perturbations = 0

    # do parallel here, please ;~;
    for i in range(n):
        print(f"Algo: {algo.__name__}, iteration: {i+1}")
        start_time = time.perf_counter()
        start, starting_score = use_start(distances, starters_list)
        if time_limiter is None:
            solution = algo(start, distances)
        else:
            solution = algo(start, distances, time_limiter)
        elapsed_time = time.perf_counter() - start_time
        if time_limiter is None:
            path1, path2 = solution
            num_perturbations = 0
        else:
            path1, path2, num_perturbations = solution
        score = summary_cost(path1, path2, distances)
        diff = starting_score - score
        total_score += score
        total_time += elapsed_time
        total_diff += diff
        all_num_perturbations += num_perturbations
        if score < best_score:
            best_score = score
            best_solution = [path1, path2]
        worst_score = max(worst_score, score)
        best_time = min(best_time, elapsed_time)
        worst_time = max(worst_time, elapsed_time)
        best_diff = max(best_diff, diff)

    return best_score, total_score / n, worst_score, best_solution, best_time, total_time / n, worst_time, best_diff, total_diff / n, all_num_perturbations / n

if __name__ == '__main__':
    instances = [
        '../data/kroA200.tsp',
        '../data/kroB200.tsp'
    ]
    starters = [
        randomstart,
        split_paths_regret_TSP,
        spectral_split_two_regret
    ]
    local_algorithms = [
        # MSLS,
        # ILS,
        LNS,
        # LNS_no_LS,
    ]

    time_limiter = None
    results = []
    os.makedirs("../best_paths_swojstarter", exist_ok=True)
    for insta in instances:
        i = insta.split('/')[-1].split('.')[0]
        os.makedirs(f"../best_paths_swojstarter/{i}", exist_ok=True)

    for insta in instances:
        data = read_data(insta)
        distances = measure_distances(data)
        i = insta.split('/')[-1].split('.')[0]
        print(f"=============================={insta}==============================")
        time_limiter = 269.287 if i == 'kroA200' else 279.947
        for algorithm in local_algorithms:
            algo_name = algorithm.__name__
            print(f"==============={algo_name}===============")
            found_best, found_avg, found_worst, found_best_paths, bt, avgt, wt, diff_best, diff_avg, pert_avg = use_local_algo(
                algorithm, distances, time_limiter, starters_list=starters)

            results.append(
                [insta, algo_name, found_best, found_avg, found_worst, bt, avgt, wt, diff_best, diff_avg, "-" if pert_avg == 0 else pert_avg])
            save_path = f"../best_paths_swojstarter/{i}/{os.path.basename(algo_name)}.png"
            show_paths(data, *found_best_paths, save_path)

    headers = ["Instance", "Algorytm", "Best", "Avg", "Worst", "Best Time", "Avg Time", "Worst Time", "Best Diff", "Avg Diff", "Avg Perturbations"]
    print(tabulate(results, headers=headers, tablefmt="grid"))