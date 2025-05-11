from algo.local_LM import local_LM
from utils import summary_cost
import random

def random_paths(distances):
    num_nodes = len(distances)
    nodes = list(range(num_nodes))
    random.shuffle(nodes)
    split_index = num_nodes // 2
    return [nodes[:split_index], nodes[split_index:]]

def MSLS(starting_paths, distances, num_iterations=200):
    best_cost = float('inf')
    best_path1, best_path2 = None, None

    for _ in range(num_iterations):
        path1, path2 = local_LM(starting_paths, distances)
        cost = summary_cost(path1, path2, distances)
        if cost < best_cost:
            best_cost = cost
            best_path1 = path1.copy()
            best_path2 = path2.copy()
        starting_paths = random_paths(distances)

    return [best_path1, best_path2]