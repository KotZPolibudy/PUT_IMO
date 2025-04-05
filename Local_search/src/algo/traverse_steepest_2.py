# steepest, ale z zamianą pomiędzy cyklami

def compute_score_change(path1, path2, distances, i, j):
    a, b = path1[i - 1], path1[i]
    c, d = path1[i + 1], path2[j - 1]
    e, f = path2[j], path2[j + 1]

    old_distance = distances[a][b] + distances[b][c] + distances[d][e] + distances[e][f]
    new_distance = distances[a][e] + distances[e][c] + distances[d][b] + distances[b][f]

    return new_distance - old_distance

# ale z zamianą wewnątrz cyklu
def compute_score_change2(path, distances, i, j):
    n = len(path)
    prev_i, next_i = (i - 1), (i + 1) % n
    prev_j, next_j = (j - 1), (j + 1) % n

    # old_dist = (distances[path[prev_i]][path[i]] + distances[path[i]][path[next_i]] +
    #             distances[path[prev_j]][path[j]] + distances[path[j]][path[next_j]])

    # new_dist = (distances[path[prev_i]][path[j]] + distances[path[j]][path[next_i]] +
    #             distances[path[prev_j]][path[i]] + distances[path[i]][path[next_j]])
    
    old_dist = distances[path[prev_i]][path[i]] + distances[path[prev_j]][path[j]]
    new_dist = distances[path[prev_i]][path[prev_j]] + distances[path[i]][path[j]]

    return new_dist - old_dist


def traverse_steepest_shuffle(starting_paths, distances, _):
    path1 = starting_paths[0]
    path2 = starting_paths[1]
    n = len(path2)
    improved = True
    while improved:
        improved = False
        best_i, best_j = -1, -1
        best_score_change = float('inf') # 0

        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                score_change = compute_score_change(path1, path2, distances, i, j)
                if score_change < best_score_change:
                    best_score_change = score_change
                    best_i, best_j = i, j

        if best_i != -1 and best_j != -1:
            path1[best_i], path2[best_j] = path2[best_j], path1[best_i]
            improved = True

    return [path1, path2]
