def calc_regret(curr_path, distances, visited):
    n = len(distances)
    possibilities = [i for i in range(n) if not visited[i]]
    best_insert = None
    max_regret = float('-inf')

    for b in possibilities:
        best_cost, second_best_cost = float('inf'), float('inf')
        best_position = None

        for i in range(len(curr_path) - 1):
            a, c = curr_path[i], curr_path[i + 1]
            cost = distances[a][b] + distances[b][c] - distances[a][c]

            if cost < best_cost:
                second_best_cost = best_cost
                best_cost = cost
                best_position = i + 1
            elif cost < second_best_cost:
                second_best_cost = cost

        regret = second_best_cost - best_cost if second_best_cost != float('inf') else 0

        if regret > max_regret:
            max_regret = regret
            best_insert = (best_position, b)

    return best_insert


def two_regret_basic(data, distances, starting_nodes):
    n = len(data)
    start1, start2 = starting_nodes
    path1, path2 = [start1, start1], [start2, start2]
    visited = [False for _ in range(n)]
    visited[start1], visited[start2] = True, True

    while visited.count(False) > 0:
        best_insert1 = calc_regret(path1, distances, visited)
        best_insert2 = calc_regret(path2, distances, visited)

        if best_insert1 is None and best_insert2 is None:
            break

        if best_insert1:
            insertion_index1, insertion_town1 = best_insert1
            path1.insert(insertion_index1, insertion_town1)
            visited[insertion_town1] = True

        if best_insert2:
            insertion_index2, insertion_town2 = best_insert2
            path2.insert(insertion_index2, insertion_town2)
            visited[insertion_town2] = True

    return path1, path2
