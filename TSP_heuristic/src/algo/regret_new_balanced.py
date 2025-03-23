def two_regret_global_balanced(distances, starting_nodes):
    n = len(distances)

    def calc_global_regret(path1, path2, distances, visited):
        possibilites = [i for i in range(n) if not visited[i]]
        max_regret1 = -1
        max_regret2 = -1
        best_insert1 = None
        best_insert2 = None

        for b in possibilites:
            insertion_costs = [[], []]
            for i in range(len(path1) - 1):
                a, c = path1[i], path1[i + 1]
                cost = distances[a][b] + distances[b][c] - distances[a][c]
                insertion_costs[0].append((cost, i + 1))
            insertion_costs[0].sort()

            for i in range(len(path2) - 1):
                a, c = path2[i], path2[i + 1]
                cost = distances[a][b] + distances[b][c] - distances[a][c]
                insertion_costs[1].append((cost, i + 1))
            insertion_costs[1].sort()

            regret1 = insertion_costs[0][1][0] - insertion_costs[0][0][0] if len(insertion_costs[0]) > 1 else float(
                'inf')
            regret2 = insertion_costs[1][1][0] - insertion_costs[1][0][0] if len(insertion_costs[1]) > 1 else float(
                'inf')

            if regret1 > max_regret1:
                max_regret1 = regret1
                best_insert1 = (insertion_costs[0][0][1], b)
            if regret2 > max_regret2:
                max_regret2 = regret2
                best_insert2 = (insertion_costs[1][0][1], b)

        return best_insert1, best_insert2, max_regret1, max_regret2

    start1, start2 = starting_nodes
    path1, path2 = [start1, start1], [start2, start2]
    visited = [False for _ in range(n)]
    visited[start1], visited[start2] = True, True

    while visited.count(False) > 0:
        best_insert1, best_insert2, max_regret1, max_regret2 = calc_global_regret(path1, path2, distances, visited)

        if len(path1) < len(path2) and best_insert1:
            insert_index1, town1 = best_insert1
            path1.insert(insert_index1, town1)
            visited[town1] = True
        elif len(path2) < len(path1) and best_insert2:
            insert_index2, town2 = best_insert2
            path2.insert(insert_index2, town2)
            visited[town2] = True
        else:
            if best_insert1 and best_insert2:
                if max_regret1 > max_regret2:
                    insert_index1, town1 = best_insert1
                    path1.insert(insert_index1, town1)
                    visited[town1] = True
                else:
                    insert_index2, town2 = best_insert2
                    path2.insert(insert_index2, town2)
                    visited[town2] = True
            elif best_insert1:
                insert_index1, town1 = best_insert1
                path1.insert(insert_index1, town1)
                visited[town1] = True
            elif best_insert2:
                insert_index2, town2 = best_insert2
                path2.insert(insert_index2, town2)
                visited[town2] = True

    return path1, path2
