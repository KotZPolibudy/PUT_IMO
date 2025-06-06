import math
import time
from tabulate import tabulate
from utils import *
# starters
from algo.randomstart import randomstart
from algo.split_regret_starter import split_paths_regret_TSP
from algo.spectral_split_two_regret import spectral_split_two_regret


def use_starter_algo(algo, d, n=100):
    total_time = 0
    total_score = 0
    best_paths = None
    fbest = math.inf
    fworst = 0
    wt = 0
    bt = math.inf

    for i in range(n):
        start_time = time.perf_counter()
        paths = algo(distances, choose_starting_nodes(data, distances))
        czas = time.perf_counter() - start_time
        koszt = summary_cost(*paths, distances)

        total_score += koszt
        total_time += czas
        fworst = max(fworst, koszt)
        bt = min(bt, czas)
        wt = max(wt, czas)
        if koszt < fbest:
            fbest = koszt
            best_paths = paths

    return fbest, total_score/n, fworst, best_paths, bt, total_time/n, wt



if __name__ == '__main__':
    instances = [
        '../data/kroA200.tsp',
        '../data/kroB200.tsp'
    ]
    algorithms = [
        randomstart,
        split_paths_regret_TSP,
        spectral_split_two_regret
    ]

    results = []
    os.makedirs("../best_paths_constructions", exist_ok=True)
    for insta in instances:
        i = insta.split('/')[-1].split('.')[0]
        os.makedirs(f"../best_paths_constructions/{i}", exist_ok=True)

    for insta in instances:
        data = read_data(insta)
        distances = measure_distances(data)
        i = insta.split('/')[-1].split('.')[0]
        print(f"=============================={insta}==============================")
        for algorithm in algorithms:
            algo_name = algorithm.__name__
            print(f"==============={algo_name}===============")
            found_best, found_avg, found_worst, found_best_paths, bt, avgt, wt = use_starter_algo(algorithm, distances)


            results.append(
                [insta, algo_name, found_best, found_avg, found_worst, bt, avgt, wt])
            save_path = f"../best_paths/{i}/{os.path.basename(algo_name)}.png"
            show_paths(data, *found_best_paths, save_path)

    headers = ["Instance", "Algorytm", "Best", "Avg", "Worst", "Best Time", "Avg Time", "Worst Time"]
    print(tabulate(results, headers=headers, tablefmt="grid"))
