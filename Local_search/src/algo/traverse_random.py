import time
import random


def random_move(path1, path2, curr_score):
    # todo
    # wybierz losowo,
    # albo zamień wierzchołki między ścieżkami
    # albo zamień kolejność wierzchołków w jakiejś ścieżce

    # score oblicz - obliczając zmianę jaką wprowadził ten ruch
    score = 0
    curr_score += score
    return path1, path2, curr_score


def traverse_random(starting_paths, distances, score, time_limit):
    time_start = time.time()
    path1 = starting_paths[0]
    path2 = starting_paths[1]
    best_path1 = starting_paths[0]
    best_path2 = starting_paths[1]
    best_score = score

    while time.time() - time_start < time_limit:
        path1, path2, score = random_move(path1, path2, score)
        if score > best_score:
            best_path1 = path1
            best_path2 = path2
            best_score = score

    return [best_path1, best_path2]
