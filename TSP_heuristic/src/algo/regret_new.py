def two_regret_global(distances, starting_nodes):
    n = len(distances)

    def calc_global_regret(path1, path2, distances, visited):
        possibilites = [i for i in range(n) if not visited[i]]
        max_regret1 = -1
        max_regret2 = -1
        best_insert1 = None
        best_insert2 = None
        """
        for b in possibilites:
            insertion_costs = []
            for i in range(len(path) - 1):
                a, c = path[i], path[i + 1]
                cost = distances[a][b] + distances[b][c] - distances[a][c]
                insertion_costs.append((cost, i + 1))
            insertion_costs.sort()
            if len(insertion_costs) > 1:
                regret = insertion_costs[1][0] - insertion_costs[0][0]     
            else:
                regret = float('inf')
            if regret > max_regret:
                max_regret = regret
                best_insert = (insertion_costs[0][1], b)
        """
        for b in possibilites:
            insertion_costs = [[], []]
            for i in range(len(path1) - 1):
                a, c = path1[i], path1[i+1]
                cost = distances[a][b] + distances[b][c] - distances[a][c]
                insertion_costs[0].append((cost, i + 1))
            insertion_costs[0].sort()  # czy tu powinno się oddać key = ??
            for i in range(len(path2) - 1):
                a, c = path2[i], path2[i+1]
                cost = distances[a][b] + distances[b][c] - distances[a][c]
                insertion_costs[1].append((cost, i + 1))
            insertion_costs[1].sort()  # czy tu powinno się oddać key = ??
            if len(insertion_costs[0]) > 1:
                regret1 = insertion_costs[0][1][0] - insertion_costs[0][0][0]
            else:
                regret1 = float('inf')
            if len(insertion_costs[1]) > 1:
                regret2 = insertion_costs[1][1][0] - insertion_costs[1][0][0]
            else:
                regret2 = float('inf')
            if regret1 < regret2:
                if regret1 > max_regret1:
                    max_regret1 = regret1
                    best_insert1 = (insertion_costs[0][0][1], b)
            else:
                if regret2 > max_regret2:
                    max_regret2 = regret2
                    best_insert2 = (insertion_costs[1][0][1], b)

        return best_insert1, best_insert2

    start1, start2 = starting_nodes
    path1, path2 = [start1, start1], [start2, start2]
    visited = [False for _ in range(n)]
    visited[start1], visited[start2] = True, True
    while visited.count(False) > 0:
        best_insert1, best_insert2 = calc_global_regret(path1, path2, distances, visited)
        if best_insert1:
            insert_index1, town1 = best_insert1
            path1.insert(insert_index1, town1)
            visited[town1] = True
        if best_insert2:
            insert_index2, town2 = best_insert2
            path2.insert(insert_index2, town2)
            visited[town2] = True
    return path1, path2