def split_paths_regret_TSP(distances, starting_nodes, use_weights=False):
    n = len(distances)

    start1, start2 = starting_nodes
    remaining_nodes = [node for node in range(n) if node not in {start1, start2}]

    # Oblicz odległości od start1 i start2
    distances_from_start1 = sorted(remaining_nodes, key=lambda x: distances[start1][x])
    distances_from_start2 = sorted(remaining_nodes, key=lambda x: distances[start2][x])


    nodes1, nodes2 = [start1], [start2]
    assigned = set()
    # Przydziel wierzchołki naprzemiennie do dwóch grup
    for i in range(len(remaining_nodes)):
        if i % 2 == 0:
            for node in distances_from_start1:
                if node not in assigned:
                    nodes1.append(node)
                    assigned.add(node)
                    break
        else:
            for node in distances_from_start2:
                if node not in assigned:
                    nodes2.append(node)
                    assigned.add(node)
                    break

    def two_regret_heuristic(path, nodes, distances, use_weights=False, w1=1, w2=-1):
        visited = set(path)
        while len(path) < len(nodes) + 1:
            # to +1 powoduje, że nie omijamy żadnego miasta ;) bo zaczynamy z startowym 2 razy, żeby domknąć cykl
            best_insert = None
            max_regret = -1

            for b in nodes:
                if b in visited:
                    continue

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

            if best_insert:
                insert_index, town = best_insert
                path.insert(insert_index, town)
                visited.add(town)

        return path

    # Debug prints
    path1 = two_regret_heuristic([start1, start1], nodes1, distances, use_weights)
    path2 = two_regret_heuristic([start2, start2], nodes2, distances, use_weights)

    return path1, path2

def weighted_split_paths_regret_TSP(distances, starting_nodes):
    return split_paths_regret_TSP(distances, starting_nodes, use_weights=True)
