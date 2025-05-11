import random
from algo.local_LM import local_LM
from utils import summary_cost
import time

def destroy_repair(path1, path2, distances, destroy_frac=0.3):
    def get_edges_with_lengths(path):
        edges = []
        for i in range(len(path)):
            u = path[i]
            v = path[(i + 1) % len(path)]
            length = distances[u][v]
            edges.append((length, i, u, v))  # długość, indeks, węzły
        edges.sort(reverse=True)
        return edges

    def is_near_other_path(u, v, other_path, threshold=20):
        return any(
            distances[u][node] < threshold or distances[v][node] < threshold
            for node in other_path
        )

    def collect_region(path, index, region_size):
        n = len(path)
        return {path[(index + offset) % n] for offset in range(-region_size, region_size + 1)}

    total_nodes = len(path1) + len(path2)
    nodes_per_region = int((destroy_frac * total_nodes) // 3)
    region_size = max(1, (nodes_per_region - 1) // 2)

    region1 = set()
    region2 = set()

    # Region 1: długa krawędź z path1 blisko path2
    for length, idx, u, v in get_edges_with_lengths(path1):
        if is_near_other_path(u, v, path2):
            region1 = collect_region(path1, idx, region_size)
            break
    if not region1:
        # najdłuższa krawędź
        _, idx, _, _ = get_edges_with_lengths(path1)[0]
        region1 = collect_region(path1, idx, region_size)

    # Region 2: długa krawędź z path2 blisko path1
    for length, idx, u, v in get_edges_with_lengths(path2):
        if is_near_other_path(u, v, path1):
            region2 = collect_region(path2, idx, region_size)
            break
    if not region2:
        # najdłuższa krawędź
        _, idx, _, _ = get_edges_with_lengths(path2)[0]
        region2 = collect_region(path2, idx, region_size)

    # Region 3: losowy
    rand_path = random.choice([path1, path2])
    rand_index = random.randint(0, len(rand_path) - 1)
    region3 = collect_region(rand_path, rand_index, region_size)

    # Połącz
    to_remove = region1.union(region2).union(region3)
    max_remove = int(destroy_frac * total_nodes)
    if len(to_remove) > max_remove:
        to_remove = set(random.sample(to_remove, max_remove))

    # Rozdziel pozostałe węzły
    all_nodes = path1 + path2
    remaining = [node for node in all_nodes if node not in to_remove]
    half = len(remaining) // 2
    new_path1 = remaining[:half]
    new_path2 = remaining[half:]

    # Naprawa: wstaw usunięte węzły tam, gdzie koszt rośnie najmniej
    for node in to_remove:
        best_increase = float('inf')
        best_path = None
        best_pos = None

        for path in [new_path1, new_path2]:
            for i in range(len(path)):
                prev = path[i - 1]
                next = path[i % len(path)]
                increase = (
                    distances[prev][node]
                    + distances[node][next]
                    - distances[prev][next]
                )
                if increase < best_increase:
                    best_increase = increase
                    best_path = path
                    best_pos = i

        best_path.insert(best_pos, node)

    return new_path1, new_path2

def LNS(starting_paths, distances, time_limit, if_LS=True):
    path1, path2 = local_LM(starting_paths, distances)
    cost = summary_cost(path1, path2, distances)

    best_path1 = path1.copy()
    best_path2 = path2.copy()
    best_cost = cost

    num_perturbations = 0
    start_time = time.time()

    while time.time() - start_time < time_limit:
        y_path1, y_path2 = best_path1.copy(), best_path2.copy()
        y_path1, y_path2 = destroy_repair(y_path1, y_path2, distances)
        if if_LS:
            new_starting_paths = [y_path1, y_path2]
            y_path1, y_path2 = local_LM(new_starting_paths, distances)
        y_cost = summary_cost(y_path1, y_path2, distances)

        if y_cost < best_cost:
            best_path1 = y_path1
            best_path2 = y_path2
            best_cost = y_cost

        num_perturbations += 1

    return [best_path1, best_path2, num_perturbations]