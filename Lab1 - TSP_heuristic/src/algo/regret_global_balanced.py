def calc_regret_global(distances, path1, path2, visited):
    n = len(distances)
    possibilities = [i for i in range(n) if not visited[i]]
    best_insert = None
    max_regret = float('-inf')
    best_path = None

    for b in possibilities:
        best_cost1, second_best_cost1 = float('inf'), float('inf')
        best_position1 = None

        best_cost2, second_best_cost2 = float('inf'), float('inf')
        best_position2 = None

        for i in range(len(path1) - 1):
            a, c = path1[i], path1[i + 1]
            cost = distances[a][b] + distances[b][c] - distances[a][c]
            if cost < best_cost1:
                second_best_cost1 = best_cost1
                best_cost1 = cost
                best_position1 = i + 1
            elif cost < second_best_cost1:
                second_best_cost1 = cost

        for i in range(len(path2) - 1):
            a, c = path2[i], path2[i + 1]
            cost = distances[a][b] + distances[b][c] - distances[a][c]
            if cost < best_cost2:
                second_best_cost2 = best_cost2
                best_cost2 = cost
                best_position2 = i + 1
            elif cost < second_best_cost2:
                second_best_cost2 = cost

        regret1 = second_best_cost1 - best_cost1 if second_best_cost1 != float('inf') else 0
        regret2 = second_best_cost2 - best_cost2 if second_best_cost2 != float('inf') else 0
        min_regret = min(regret1, regret2)

        if min_regret > max_regret:
            max_regret = min_regret
            if len(path1) <= len(path2):
                best_insert = (best_position1, b)
                best_path = path1
            else:
                best_insert = (best_position2, b)
                best_path = path2

    return best_insert, best_path


def two_regret_global_balanced(data, distances, starting_nodes):
    n = len(data)
    start1, start2 = starting_nodes
    path1, path2 = [start1, start1], [start2, start2]
    visited = [False for _ in range(n)]
    visited[start1], visited[start2] = True, True

    while visited.count(False) > 0:
        best_insert, best_path = calc_regret_global(distances, path1, path2, visited)

        if best_insert is None:
            break

        insertion_index, insertion_town = best_insert
        best_path.insert(insertion_index, insertion_town)
        visited[insertion_town] = True

    return path1, path2
