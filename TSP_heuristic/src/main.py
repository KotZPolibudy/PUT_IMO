import os
from utils import *
from algo.greedy_near import greedy_nearest_neighbor
from algo.greedy_cheap import greedy_cheapest_insertion
from algo.regret_first import two_regret, weighted_two_regret
from algo.regret_basic import two_regret_basic
from algo.regret_global import two_regret_global
from algo.regret_global_balanced import two_regret_global_balanced
from algo.our_own_genetic import genetic_2tsp


def show_paths(data, path1, path2, save_path=None):
    x = [town.x for town in data]
    y = [town.y for town in data]
    plt.scatter(x, y)
    for i in range(len(path1) - 1):
        plt.plot([data[path1[i]].x, data[path1[i + 1]].x], [data[path1[i]].y, data[path1[i + 1]].y], 'r')
    for i in range(len(path2) - 1):
        plt.plot([data[path2[i]].x, data[path2[i + 1]].x], [data[path2[i]].y, data[path2[i + 1]].y], 'b')

    if save_path:
        plt.savefig(save_path)
    plt.show()
    plt.close()


def use_algorithm(algorithm, data, distances):
    return algorithm(data, distances, choose_starting_nodes(data, distances))


def algorithm_loop(algorithm, data, distances, n=100):
    best_cost = float('inf')
    worst_cost = float('-inf')
    total_cost = 0
    best_paths = None

    for _ in range(n):
        paths = use_algorithm(algorithm, data, distances)
        if paths is None:
            return None, None, None, None
        cost = summary_cost(*paths, distances)
        total_cost += cost
        if cost < best_cost:
            best_cost = cost
            best_paths = paths
        worst_cost = max(worst_cost, cost)

    return best_cost, total_cost / n, worst_cost, best_paths


if __name__ == '__main__':
    # paths = ['data/' + f'kro{i}200.tsp' for i in ['A', 'B']]
    paths = ['data/kroA200.tsp', 'data/kroB200.tsp']
    # paths = ['data/kroA200.tsp']
    algorithms = [
        greedy_nearest_neighbor,
        greedy_cheapest_insertion,
        # two_regret,
        # weighted_two_regret,
        # two_regret_basic,
        # two_regret_global,
        # two_regret_global_balanced,
        # genetic_2tsp,
    ]

    results = {}
    os.makedirs("best_paths", exist_ok=True)

    for algorithm in algorithms:
        algo_name = algorithm.__name__
        results[algo_name] = []
        for path in paths:
            data = read_data(path)
            distances = measure_distances(data)
            best, avg, worst, best_paths = algorithm_loop(algorithm, data, distances)
            if best is None:
                results[algo_name].append("N/A")
            else:
                results[algo_name].append(f"{avg:.2f} ; {best:.2f} ; {worst:.2f}")
                save_path = f"best_paths/{algo_name}_{os.path.basename(path)}.png"
                show_paths(data, *best_paths, save_path)

    # Print results in table format
    header = "Algorytm | " + " | ".join(paths)
    print(header)
    print("-" * len(header))
    for algo, values in results.items():
        print(f"{algo} | " + " | ".join(values))
