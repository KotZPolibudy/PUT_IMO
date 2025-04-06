import random


def compute_score_change(path, distances, i, j):
    n = len(path)
    prev_i, next_i = (i - 1), (i + 1) % n
    prev_j, next_j = (j - 1), (j + 1) % n
    old_dist = distances[path[prev_i]][path[i]] + distances[path[prev_j]][path[j]]
    new_dist = distances[path[prev_i]][path[prev_j]] + distances[path[i]][path[j]]
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
                    if abs(i - j) == 1:
                        path[i], path[j] = path[j], path[i]
                    else:
                        path[i:j] = path[i:j][::-1]
                    improved = True
                    found_improvement = True
                    break
            if found_improvement:
                break
    return path


def exchange(path1, path2, distances):
    # try to exchange between paths!
    did_exchange = False
    # todo
    return path1, path2, did_exchange


def traverse_greedy(starting_paths, distances, _):
    path1, path2 = starting_paths
    again = True
    while again:
        path1 = optimize_path(path1, distances)
        path2 = optimize_path(path2, distances)
        path1, path2, again = exchange(path1, path2, distances)
    return [path1, path2]
