def compute_score_change(path, distances, i, j):
    n = len(path)
    if i == 0 or j == 0 or i == n - 1 or j == n - 1:
        return float('inf') # zapobiega przesuwaniu ostatniego elementu
    elif abs(i - j) == 1:
        b, c = min(i, j), max(i, j)
        a = b - 1
        d = (c + 1) % n
        old_dist = distances[path[a]][path[b]] + distances[path[c]][path[d]]
        new_dist = distances[path[a]][path[c]] + distances[path[b]][path[d]]
    else:
        prev_i, next_i = (i - 1), (i + 1) % n
        prev_j, next_j = (j - 1), (j + 1) % n
        old_dist = distances[path[prev_i]][path[i]] + distances[path[prev_j]][path[j]] + distances[path[i]][path[next_i]] + distances[path[j]][path[next_j]]
        new_dist = distances[path[prev_i]][path[j]] + distances[path[j]][path[next_i]] + distances[path[prev_j]][path[i]] + distances[path[i]][path[next_j]]
    return new_dist - old_dist


def compute_score_change_shuffle(path1, path2, distances, i, j):
    a, b = path1[i - 1], path1[i]
    c, d = path1[i + 1], path2[j - 1]
    e, f = path2[j], path2[j + 1]
    old_distance = distances[a][b] + distances[b][c] + distances[d][e] + distances[e][f]
    new_distance = distances[a][e] + distances[e][c] + distances[d][b] + distances[b][f]
    return new_distance - old_distance


def traverse_steepest_vertex(starting_paths, distances, _):
    path1 = starting_paths[0]
    path2 = starting_paths[1]
    n = len(path2)
    improved = True
    while improved:
        improved = False
        best_i, best_j = -1, -1
        best_score_change = 0
        method = False  # False - exchange, True - vertex
        best_path = False  # False - path1, True - path2

        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                score_change = compute_score_change(path1, distances, i, j)
                if score_change < best_score_change:
                    best_score_change = score_change
                    best_i, best_j = i, j
                    method = True
                    best_path = False
                score_change = compute_score_change(path2, distances, i, j)
                if score_change < best_score_change:
                    best_score_change = score_change
                    best_i, best_j = i, j
                    method = True
                    best_path = True

        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                score_change = compute_score_change_shuffle(path1, path2, distances, i, j)
                if score_change < best_score_change:
                    best_score_change = score_change
                    best_i, best_j = i, j
                    method = False

        if best_i != -1 and best_j != -1:
            if method:
                if best_path:
                    path2[best_i], path2[best_j] = path2[best_j], path2[best_i]
                else:
                    path1[best_i], path1[best_j] = path1[best_j], path1[best_i]
            else:
                path1[best_i], path2[best_j] = path2[best_j], path1[best_i]
            improved = True

    return [path1, path2]
