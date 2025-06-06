import time
from tabulate import tabulate
from utils import *
# starters
from algo.randomstart import randomstart
from algo.split_regret_starter import split_paths_regret_TSP
from algo.spectral_split_two_regret import spectral_split_two_regret


def use_starter_algo(algo, d):
    start_time = time.perf_counter_ns()
    paths = algo(distances, choose_starting_nodes(data, distances))
    czas = time.perf_counter_ns() - start_time
    koszt = summary_cost(*paths, distances)
    return paths, koszt, czas


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
            found_best_paths, cost, elapsed_time = use_starter_algo(algorithm, distances)

            results.append(
                [insta, algo_name, cost, elapsed_time])
            save_path = f"../best_paths_constructions/{i}/{os.path.basename(algo_name)}.png"
            show_paths(data, *found_best_paths, save_path)

    headers = ["Instance", "Algorytm", "Cost", "Time"]
    print(tabulate(results, headers=headers, tablefmt="grid"))
