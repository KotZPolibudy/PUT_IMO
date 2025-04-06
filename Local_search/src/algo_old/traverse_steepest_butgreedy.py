from random import random


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
        best_i, best_j = -1, -1
        best_score_change = 0
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                score_change = compute_score_change(path, distances, i, j)
                if score_change < best_score_change:
                    best_score_change = score_change
                    best_i, best_j = i, j

        if best_i != -1 and best_j != -1:
            if abs(best_i - best_j) == 1:
                path[best_i], path[best_j] = path[best_j], path[best_i]
            else:
                path[best_i:best_j] = path[best_i:best_j][::-1]
            improved = True

    return path


def exchange(path1, path2, distances):
    did_exchange = False
    n = len(path2)
    best_i, best_j = -1, -1
    best_score_change = 0

    for i in range(1, n - 2):
        for j in range(i + 1, n - 1):
            score_change = compute_exchange_score_change(path1, path2, distances, i, j)
            if score_change < best_score_change:
                best_score_change = score_change
                best_i, best_j = i, j

    if best_i != -1 and best_j != -1:
        path1[best_i], path2[best_j] = path2[best_j], path1[best_i]
        did_exchange = True

    return path1, path2, did_exchange


def traverse_steepest_edge(starting_paths, distances, _):
    path1, path2 = starting_paths
    again = True
    while again:
        path1 = optimize_path(path1, distances)
        path2 = optimize_path(path2, distances)
        path1, path2, again = exchange(path1, path2, distances)
    return [path1, path2]
