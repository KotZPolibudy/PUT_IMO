import numpy as np
from scipy.sparse.csgraph import laplacian
from scipy.sparse.linalg import eigsh

def spectral_split_two_regret(distances, starting_nodes):
    distances = np.array(distances)

    def balanced_spectral_split(distances_submatrix):
        m = len(distances_submatrix)

        # Zamień odległości na podobieństwo
        similarity = 1 / (distances_submatrix + 1e-6)
        np.fill_diagonal(similarity, 0)

        # Oblicz Laplasjan i wektor Fiedlera
        L = laplacian(similarity, normed=True)
        _, vecs = eigsh(L, k=2, which='SM')
        fiedler = vecs[:, 1]

        # Podział na dwie równe grupy
        sorted_nodes = np.argsort(fiedler)
        mid = m // 2
        group1 = sorted_nodes[:mid]
        group2 = sorted_nodes[mid:]
        return group1.tolist(), group2.tolist()

    def two_regret_heuristic(path, nodes, distances, use_weights=False, w1=1, w2=-1):
        visited = set(path)
        while len(path) < len(nodes) + 1:
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
                        regret = w1 * insertion_costs[1][0] + w2 * insertion_costs[0][0]
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

    n = len(distances)
    start1, start2 = starting_nodes
    all_nodes = [i for i in range(n) if i not in starting_nodes]
    sub_distances = distances[np.ix_(all_nodes, all_nodes)]

    group1_idx, group2_idx = balanced_spectral_split(sub_distances)

    nodes1 = [all_nodes[i] for i in group1_idx]
    nodes2 = [all_nodes[i] for i in group2_idx]

    path1 = two_regret_heuristic([start1, start1], [start1] + nodes1, distances)
    path2 = two_regret_heuristic([start2, start2], [start2] + nodes2, distances)

    return path1, path2
