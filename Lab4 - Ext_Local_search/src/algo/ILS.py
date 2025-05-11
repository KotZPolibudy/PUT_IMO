import random
from algo.local_LM import local_LM
from utils import summary_cost
import time

def perturbation_ILS(path1, path2, num_vertex_swaps=4, num_edge_swaps=2):
    # Zamiana wierzchołków między cyklami
    for _ in range(num_vertex_swaps):
        idx1 = random.randint(0, len(path1) - 1)
        idx2 = random.randint(0, len(path2) - 1)
        path1[idx1], path2[idx2] = path2[idx2], path1[idx1]

    # Operacje 2-opt w cyklu 1 (zamiana krawędzi)
    for _ in range(num_edge_swaps):
        if len(path1) >= 4:
            i, j = sorted(random.sample(range(len(path1)), 2))
            if j - i > 1:  # sensowna długość do odwrócenia
                path1[i:j] = reversed(path1[i:j])

    # Operacje 2-opt w cyklu 2
    for _ in range(num_edge_swaps):
        if len(path2) >= 4:
            i, j = sorted(random.sample(range(len(path2)), 2))
            if j - i > 1:
                path2[i:j] = reversed(path2[i:j])

    return path1, path2

def ILS(starting_paths, distances, time_limit):
    path1, path2 = local_LM(starting_paths, distances)
    cost = summary_cost(path1, path2, distances)

    best_path1 = path1.copy()
    best_path2 = path2.copy()
    best_cost = cost

    num_perturbations = 0
    start_time = time.time()

    while time.time() - start_time < time_limit:
        y_path1, y_path2 = best_path1.copy(), best_path2.copy()
        y_path1, y_path2 = perturbation_ILS(y_path1, y_path2)
        new_starting_paths = [y_path1, y_path2]
        y_path1, y_path2 = local_LM(new_starting_paths, distances)
        y_cost = summary_cost(y_path1, y_path2, distances)

        if y_cost < best_cost:
            best_path1 = y_path1
            best_path2 = y_path2
            best_cost = y_cost

        num_perturbations += 1

    return [best_path1, best_path2, num_perturbations]