def two_regret(distances, starting_nodes, use_weights=False):
    n = len(distances)

    def calc_regret(path, distances, visited, use_weights=False, w1=1, w2=-1):
        possibilites = [i for i in range(n) if not visited[i]]
        max_regret = -1
        best_insert = None
        for b in possibilites:
            insertion_costs = []
            for i in range(len(path) - 1):
                a, c = path[i], path[i + 1]
                cost = distances[a][b] + distances[b][c] - distances[a][c]
                insertion_costs.append((cost, i + 1))
            insertion_costs.sort()
            if len(insertion_costs) > 1:
                if use_weights:
                    regret = w1 * insertion_costs[1][0] - w2 * insertion_costs[0][0]
                else:
                    regret = insertion_costs[1][0] - insertion_costs[0][0]
            else:
                regret = float('inf')
            if regret > max_regret:
                max_regret = regret
                best_insert = (insertion_costs[0][1], b)
        return best_insert

    start1, start2 = starting_nodes
    path1, path2 = [start1, start1], [start2, start2]
    visited = [False for _ in range(n)]
    visited[start1], visited[start2] = True, True
    while visited.count(False) > 0:
        best_insert1 = calc_regret(path1, distances, visited, use_weights)
        if best_insert1:
            insert_index1, town1 = best_insert1
            path1.insert(insert_index1, town1)
            visited[town1] = True
        best_insert2 = calc_regret(path2, distances, visited, use_weights)
        if best_insert2:
            insert_index2, town2 = best_insert2
            path2.insert(insert_index2, town2)
            visited[town2] = True
    return path1, path2


def weighted_two_regret(distances, starting_nodes):
    return two_regret(distances, starting_nodes, use_weights=True)
