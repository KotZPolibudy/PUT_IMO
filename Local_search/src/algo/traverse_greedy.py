# algorytm greedy ale tylko z wymianą wewnątrz cykli
import random

def compute_score_change(path, distances, i, j):
    n = len(path)
    # warunek stopu dla zamian pierwszy i ostatni element (to powinien być ten sam i mieć 0 dist różnicy)
    if i == 0 or j == 0:
        return float('inf')
    prev_i, next_i = (i - 1), (i + 1) % n
    prev_j, next_j = (j - 1), (j + 1) % n

    # old_dist = (distances[path[prev_i]][path[i]] + distances[path[i]][path[next_i]] +
    #             distances[path[prev_j]][path[j]] + distances[path[j]][path[next_j]])

    # new_dist = (distances[path[prev_i]][path[j]] + distances[path[j]][path[next_i]] +
    #             distances[path[prev_j]][path[i]] + distances[path[i]][path[next_j]])
    old_dist = distances[path[prev_i]][path[i]] + distances[path[prev_j]][path[j]]
    new_dist = distances[path[prev_i]][path[prev_j]] + distances[path[i]][path[j]]
    
    # print("ij dist: ", i, j, old_dist, new_dist)
    return new_dist - old_dist


def optimize_path(path, distances):
    n = len(path)
    improved = True
    while improved:
        improved = False
        found_improvement = False
        
        indices = list(range(1, n - 1))
        random.shuffle(indices)
        
        for i in indices:
            for j in range(i + 1, n):
                score_change = compute_score_change(path, distances, i, j)
                if score_change < 0:
                    path[i:j] = path[i:j][::-1]
                    improved = True
                    found_improvement = True
                    break
            if found_improvement:
                break
    return path


def traverse_greedy(starting_paths, distances, _):
    path1, path2 = starting_paths
    # print("path1")
    path1 = optimize_path(path1, distances)
    # print("path2")
    path2 = optimize_path(path2, distances)
    # print("greedy-done")
    return [path1, path2]
