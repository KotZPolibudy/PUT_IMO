import time
import random


def random_move(path1, path2):
    # todo
    score = 0
    return path1, path2, score


def traverse_random(starting_paths, distances, time_limit):
    time_start = time.time()
    path1 = starting_paths[0]
    path2 = starting_paths[1]
    best_path1 = starting_paths[0]
    best_path2 = starting_paths[1]
    best_score = 0  # todo scoring

    while time.time() - time_start < time_limit:
        path1, path2, score = random_move(path1, path2)
        if score > best_score:
            best_path1 = path1
            best_path2 = path2
            best_score = score

    return [best_path1, best_path2]