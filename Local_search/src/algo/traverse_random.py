import time
import random


def compute_score_change(path, distances, i, j):
    n = len(path)
    if i == 0 or j == 0:
        return float('inf')
    prev_i, next_i = (i - 1) % n, (i + 1) % n
    prev_j, next_j = (j - 1) % n, (j + 1) % n

    old_dist = distances[path[prev_i]][path[i]] + distances[path[prev_j]][path[j]]
    new_dist = distances[path[prev_i]][path[prev_j]] + distances[path[i]][path[j]]

    return new_dist - old_dist


def compute_score_change_shuffle(path1, path2, distances, i, j):
    a, b = path1[i - 1], path1[i]
    c, d = path1[i + 1], path2[j - 1]
    e, f = path2[j], path2[j + 1]

    old_distance = distances[a][b] + distances[b][c] + distances[d][e] + distances[e][f]
    new_distance = distances[a][e] + distances[e][c] + distances[d][b] + distances[b][f]

    return new_distance - old_distance


def random_move(path1, path2, distances, curr_score):
    # todo
    # wybierz losowo,
    # albo zamień wierzchołki między ścieżkami
    # albo zamień kolejność wierzchołków w jakiejś ścieżce
    score_change = 0
    choice = random.choice([True, False])
    if choice:
        # zamień wierzchołki wewnątrz jakiejś ścieżki
        path = random.choice([path1, path2])
        i, j = random.sample(range(len(path)), 2)
        score_change = compute_score_change(path, distances, i, j)
        if abs(i - j) == 1:
            path[i], path[j] = path[j], path[i]
        else:
            path[i:j] = path[i:j][::-1]
    else:
        # zamień wierzchołki między ścieżkami
        i, j = random.randint(1, len(path1) - 2), random.randint(1, len(path2) - 2)
        while i == j:
            i, j = random.randint(1, len(path1) - 2), random.randint(1, len(path2) - 2)
        score_change = compute_score_change_shuffle(path1, path2, distances, i, j)
        path1[i], path2[j] = path2[j], path1[i]  # Zamiana wierzchołków między cyklami

    # score oblicz - obliczając zmianę jaką wprowadził ten ruch
    curr_score += score_change
    return path1, path2, curr_score


def traverse_random(starting_paths, distances, time_limit):
    time_start = time.time()
    path1, path2 = starting_paths
    best_path1, best_path2 = path1[:], path2[:]
    best_score = 0
    new_score = 0

    # print(time_limit)
    while time.time() - time_start < time_limit:
        path1, path2, new_score = random_move(path1[:], path2[:], distances, new_score)
        if new_score < best_score:
            best_path1, best_path2, best_score = path1.copy(), path2.copy(), new_score

    return [best_path1, best_path2]
