import random


def compute_score_change(path, distances, i, j):
    n = len(path)
    prev_i, next_i = (i - 1), (i + 1) % n
    prev_j, next_j = (j - 1), (j + 1) % n
    old_dist = distances[path[prev_i]][path[i]] + distances[path[prev_j]][path[j]]
    new_dist = distances[path[prev_i]][path[prev_j]] + distances[path[i]][path[j]]
    return new_dist - old_dist


def compute_exchange_score_change(path1, path2, distances, i, j):
    a, b = path1[i - 1], path1[i]
    c, d = path1[i + 1], path2[j - 1]
    e, f = path2[j], path2[j + 1]

    old_distance = distances[a][b] + distances[b][c] + distances[d][e] + distances[e][f]
    new_distance = distances[a][e] + distances[e][c] + distances[d][b] + distances[b][f]

    return new_distance - old_distance


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
    did_exchange = False
    n = len(path2)

    possible_changes = []
    for i in range(1, n - 2):
        for j in range(i + 1, n - 1):
            possible_changes.append((i, j))
    random.shuffle(possible_changes)

    for i, j in possible_changes:
        score_change = compute_exchange_score_change(path1, path2, distances, i, j)
        if score_change < 0:
            path1[i], path2[j] = path2[j], path1[i]
            did_exchange = True

    return path1, path2, did_exchange


def traverse_greedy_edge(starting_paths, distances):
    path1, path2 = starting_paths
    again = True
    while again:
        path1 = optimize_path(path1, distances)
        path2 = optimize_path(path2, distances)
        path1, path2, again = exchange(path1, path2, distances)
    return [path1, path2]
