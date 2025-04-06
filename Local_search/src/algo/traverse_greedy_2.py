# greedy, ale z zamianą pomiędzy cyklami zamiast wewnątrz cyklu
import random

def compute_score_change(path1, path2, distances, i, j):
    a, b = path1[i - 1], path1[i]
    c, d = path1[i + 1], path2[j - 1]
    e, f = path2[j], path2[j + 1]

    old_distance = distances[a][b] + distances[b][c] + distances[d][e] + distances[e][f]
    new_distance = distances[a][e] + distances[e][c] + distances[d][b] + distances[b][f]

    return new_distance - old_distance


def traverse_greedy_shuffle(starting_paths, distances, _):
    path1 = starting_paths[0]
    path2 = starting_paths[1]
    n = len(path2)
    improved = True
    while improved:
        improved = False
        possible_changes = []
        for i in range(1, n-2):
            for j in range(i+1, n-1):
                possible_changes.append((i, j))
        random.shuffle(possible_changes)
        
        for i, j in possible_changes:
            score_change = compute_score_change(path1, path2, distances, i, j)
            if score_change < 0:
                path1[i], path2[j] = path2[j], path1[i]
                improved = True

    return [path1, path2]
