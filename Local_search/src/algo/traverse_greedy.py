def compute_score_change(path, distances, i, j):
    if abs(i - j) == 1:  # i oraz j są sąsiadami
        old_dist = distances[path[i]][path[j]] + distances[path[j]][path[(j + 1) % len(path)]]
        new_dist = distances[path[j]][path[i]] + distances[path[i]][path[(j + 1) % len(path)]]
    else:
        n = len(path)
        prev_i, next_i = (i - 1) % n, (i + 1) % n
        prev_j, next_j = (j - 1) % n, (j + 1) % n

        old_dist = (distances[path[prev_i]][path[i]] + distances[path[i]][path[next_i]] +
                    distances[path[prev_j]][path[j]] + distances[path[j]][path[next_j]])

        new_dist = (distances[path[prev_i]][path[j]] + distances[path[j]][path[next_i]] +
                    distances[path[prev_j]][path[i]] + distances[path[i]][path[next_j]])

    return new_dist - old_dist


def optimize_path(path, distances):
    n = len(path)
    improved = True
    count = 0
    while improved:
        improved = False
        found_improvement = False
        for i in range(n):
            for j in range(i + 1, n):
                score_change = compute_score_change(path, distances, i, j)
                print("score_change: ", score_change)
                if score_change < 0:
                    print("ij: ", i, j)
                    path[i], path[j] = path[j], path[i]
                    improved = True
                    found_improvement = True
                    break
            if found_improvement:
                break
        count += 1
        # if count % 1000000 == 0:
        print(f"Iteration {count}: {path}")
        if count > 5:
            return path
    return path


def traverse_greedy(starting_paths, distances, _):
    path1, path2 = starting_paths
    print("path1")
    path1 = optimize_path(path1, distances)
    print("path2")
    path2 = optimize_path(path2, distances)
    print("greedy-done")
    return [path1, path2]
