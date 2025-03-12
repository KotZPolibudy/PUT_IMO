from utils import *
from algo.greedy_near import greedy_nearest_neighbor
from algo.greedy_cheap import greedy_cheapest_insertion
from algo.regret import two_regret, weighted_two_regret


def show_paths(data, path1, path2):
    x = [town.x for town in data]
    y = [town.y for town in data]
    plt.scatter(x, y)
    for i in range(len(path1) - 1):
        plt.plot([data[path1[i]].x, data[path1[i + 1]].x], [data[path1[i]].y, data[path1[i + 1]].y], 'r')
    for i in range(len(path2) - 1):
        plt.plot([data[path2[i]].x, data[path2[i + 1]].x], [data[path2[i]].y, data[path2[i + 1]].y], 'b')
    plt.show()


def use_algorithm(algorithm, data, distances):
    return algorithm(data, distances, choose_starting_nodes(data, distances))


def algorithm_loop(algorithm, data, distances, n=100):
    costs = 0
    best_cost = float('inf')
    best_paths = None, None
    for _ in range(n):
        paths = use_algorithm(algorithm, data, distances)
        if paths is None:
            return None, None, None
        cost = summary_cost(*paths, distances)
        costs += cost
        if cost < best_cost:
            best_cost = cost
            best_paths = paths
    return best_cost, costs / n, best_paths


if __name__ == '__main__':
    paths = ['data/' + f'kro{i}200.tsp' for i in ['A', 'B']]
    algorithms = [
        greedy_nearest_neighbor,
        greedy_cheapest_insertion,
        # two_regret,
        # weighted_two_regret
    ]
    for path in paths:
        data = read_data(path)
        distances = measure_distances(data)
        for algorithm in algorithms:
            best_cost, avg_cost, best_paths = algorithm_loop(algorithm, data, distances)
            if best_cost is None or avg_cost is None or best_paths is None:
                print(f'{algorithm.__name__} skipping due to lack of implementation')
                continue
            print(f'{algorithm.__name__} on {path}:')
            print(f'Best cost: {best_cost}')
            print(f'Average cost: {avg_cost}')
            show_paths(data, *best_paths)
