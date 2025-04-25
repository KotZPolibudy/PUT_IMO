import numpy as np
from utils import summary_cost

def steepest_kandydackie(starting_paths, distances):
    path1 = starting_paths[0]
    path2 = starting_paths[1]
    n = len(path2)
    
    def compute_candidate_edges(distances, k=10):
        num_nodes = len(distances)
        candidate_edges = {}
        for i in range(num_nodes):
            neighbors = np.argsort(distances[i])[1:k+1]
            candidate_edges[i] = set(neighbors)
        return candidate_edges

    candidate_edges = compute_candidate_edges(distances)
    
    improved = True
    current_cost = summary_cost(path1, path2, distances)  # koszt początkowy rozwiązania

    while improved:
        improved = False
        best_delta = 0
        best_move = None

        # --- Ruchy między cyklami ---
        for i in range(n):
            for j in range(n):
                a, b = path1[i], path2[j]

                # rozważamy tylko wierzchołki, które są kandydatami
                if b not in candidate_edges[a] and a not in candidate_edges[b]:
                    continue

                # sąsiedzi a w path1
                a_prev = path1[i - 1]
                a_next = path1[(i + 1) % n]
                # sąsiedzi b w path2
                b_prev = path2[j - 1]
                b_next = path2[(j + 1) % n]

                # oblicz zmianę kosztu po zamianie a <-> b
                delta = 0
                delta -= distances[a_prev][a] + distances[a][a_next]
                delta -= distances[b_prev][b] + distances[b][b_next]
                delta += distances[a_prev][b] + distances[b][a_next]
                delta += distances[b_prev][a] + distances[a][b_next]

                # aktualizuj najlepszy ruch, jeśli poprawia rozwiązanie
                if delta < best_delta:
                    best_delta = delta
                    best_move = ("swap", i, j)

        # --- Ruchy wewnątrz jednego cyklu ---
        for path in [path1, path2]:
            n = len(path)
            for i in range(n):
                n1 = path[i]
                next_i = (i + 1) % n
                prev_i = (i - 1) % n
                for j in range(n):
                    if i == j:
                        continue
                    n2 = path[j]
                    if n2 not in candidate_edges[n1]:
                        continue

                    next_j = (j + 1) % n
                    prev_j = (j - 1) % n

                    # przypadek: krawędzie (n1, next_n1) oraz (n2, next_n2)
                    a, b = n1, path[next_i]
                    c, d = n2, path[next_j]
                    if len({a, b, c, d}) == 4:
                        delta = -distances[a][b] - distances[c][d] + distances[a][c] + distances[b][d]
                        if (c in candidate_edges[a] or a in candidate_edges[c]):
                            if delta < best_delta:
                                best_delta = delta
                                best_move = ("intra_next", i, j, path)

                    # przypadek: krawędzie (prev_n1, n1) oraz (prev_n2, n2)
                    a, b = path[prev_i], n1
                    c, d = path[prev_j], n2
                    if len({a, b, c, d}) == 4:
                        delta = -distances[a][b] - distances[c][d] + distances[a][c] + distances[b][d]
                        if b in candidate_edges[d] or d in candidate_edges[b]:
                            if delta < best_delta:
                                best_delta = delta
                                best_move = ("intra_prev", i, j, path)

        # wykonujemy najlepszy znaleziony ruch
        if best_move:
            improved = True
            move_type = best_move[0]

            if move_type == "swap":
                i, j = best_move[1], best_move[2]
                path1[i], path2[j] = path2[j], path1[i]

            elif move_type == "intra_next":
                i, j, path = best_move[1:]
                i_next = (i + 1) % len(path)
                j_next = (j + 1) % len(path)
                # odwrócenie fragmentu cyklu między sąsiednimi krawędziami
                if i_next < j:
                    path[i_next:j + 1] = reversed(path[i_next:j + 1])
                else:
                    path[j_next:i + 1] = reversed(path[j_next:i + 1])

            elif move_type == "intra_prev":
                i, j, path = best_move[1:]
                i_prev = (i - 1) % len(path)
                j_prev = (j - 1) % len(path)
                # odwrócenie fragmentu cyklu między sąsiednimi krawędziami
                if j < i_prev:
                    path[j:i_prev + 1] = reversed(path[j:i_prev + 1])
                else:
                    path[i:j_prev + 1] = reversed(path[i:j_prev + 1])

            # zaktualizuj całkowity koszt rozwiązania
            current_cost += best_delta

    # zwróć nowe cykle
    return [path1, path2]