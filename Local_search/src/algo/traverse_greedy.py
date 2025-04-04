# algorytm greedy ale tylko z wymianą wewnątrz cykli

def compute_score_change(path, distances, i, j):
    # n = len(path)
    # warunek stopu dla zamian pierwszy i ostatni element (to powinien być ten sam i mieć 0 dist różnicy)
    if i == 0 or j == 0:
        return 9999
    prev_i, next_i = (i - 1), (i + 1)
    prev_j, next_j = (j - 1), (j + 1)

    old_dist = (distances[path[prev_i]][path[i]] + distances[path[i]][path[next_i]] +
                distances[path[prev_j]][path[j]] + distances[path[j]][path[next_j]])

    new_dist = (distances[path[prev_i]][path[j]] + distances[path[j]][path[next_i]] +
                distances[path[prev_j]][path[i]] + distances[path[i]][path[next_j]])
    # print("ij dist: ", i, j, old_dist, new_dist)
    return new_dist - old_dist


def optimize_path(path, distances):
    n = len(path)
    improved = True
    count = 0
    while improved:
        improved = False
        found_improvement = False
        for i in range(1, n-1):
            for j in range(i + 1, n):
                score_change = compute_score_change(path, distances, i, j)
                # print("score_change: ", score_change)
                if score_change < 0:
                    # print("ij: ", i, j)
                    path[i], path[j] = path[j], path[i]
                    improved = True
                    found_improvement = True
                    break
            if found_improvement:
                break
        count += 1
        # if count % 1000000 == 0:
        # print(f"Iteration {count}: {path}")
        # if count > 5:
        #     return path
    return path


def traverse_greedy(starting_paths, distances, _):
    path1, path2 = starting_paths
    # print("path1")
    # path1 = optimize_path(path1, distances)
    # print("path2")
    # path2 = optimize_path(path2, distances)
    # print("greedy-done")
    return [path1, path2]
