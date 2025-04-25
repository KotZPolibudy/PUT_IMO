from utils import summary_cost
from collections import deque

def steepest_LM(starting_paths, distances):
    path1 = starting_paths[0]
    path2 = starting_paths[1]
    n = len(path2)

    # Sprawdza czy dana krawędź występuje w zbiorze (w obie strony)
    def edge_in_edges(edge, edge_list):
        return edge in edge_list or (edge[1], edge[0]) in edge_list

    # Sprawdza, czy ruch jest nadal możliwy do wykonania
    def is_move_applicable(removed_edges, path1, path2):
        current_edges = {(path1[i], path1[(i + 1) % n]) for i in range(n)}
        current_edges.update((path2[i], path2[(i + 1) % n]) for i in range(n))
        all_present = True
        same_direction = True
        for e in removed_edges:
            if e not in current_edges and (e[1], e[0]) not in current_edges:
                return "remove"  # edges no longer exist
            elif e not in current_edges:
                same_direction = False
        return "apply" if same_direction else "skip"

    # Inicjalizacja LM lub generowanie nowych ruchów na podstawie ostatniego ruchu
    def add_new_moves(LM, path1, path2, distances, recent_move):
        tmoves = []
        # Inicjalizacja LM
        if recent_move is None:
            for i in range(n):
                for j in range(n):
                    tmoves.append((i, j, "swap"))
            for path, path_id in [(path1, 1), (path2, 2)]:
                for i in range(len(path)):
                    for j in range(i + 1, len(path)):
                        tmoves.append((i, j, "edge_swap", path_id))
        # Generowanie nowych ruchów na podstawie ostatniego ruchu
        else:
            if recent_move[0] == "swap":
                i, j = recent_move[1], recent_move[2]
                # indeksy elementów, na które miał wpływ ostatni ruch
                indices1 = {i, (i - 1) % n, (i + 1) % n}
                indices2 = {j, (j - 1) % n, (j + 1) % n}
                # generujemy możliwe swapy
                for ni in indices1:
                    for nj in range(n):
                        tmoves.append((ni, nj, "swap"))
                for nj in indices2:
                    for ni in range(n):
                        tmoves.append((ni, nj, "swap"))
                # generujemy możliwe edge_swapy
                for idx in indices1:
                    for jdx in range(n):
                        if idx != jdx:
                            tmoves.append((min(idx, jdx), max(idx, jdx), "edge_swap", 1))
                for idx in indices2:
                    for jdx in range(n):
                        if idx != jdx:
                            tmoves.append((min(idx, jdx), max(idx, jdx), "edge_swap", 2))
            elif recent_move[0] == "edge_swap":
                i, j, path_id = recent_move[1], recent_move[2], recent_move[3]
                current_path = path1 if path_id == 1 else path2
                # indeksy elementów, na które miał wpływ ostatni ruch
                affected_indices = [k % len(current_path) for k in range(i - 1, j + 2)]
                # generujemy możliwe edge_swapy
                for a in affected_indices:
                    for b in range(a + 1, a + len(current_path)):
                        idx_b = b % len(current_path)
                        tmoves.append((min(a, idx_b), max(a, idx_b), "edge_swap", path_id))
                affected_nodes = {current_path[k] for k in affected_indices}
                # generujemy możliwe swapy
                for i, v1 in enumerate(path1):
                    if v1 in affected_nodes:
                        for j in range(n):
                            tmoves.append((i, j, "swap"))
                for j, v2 in enumerate(path2):
                    if v2 in affected_nodes:
                        for i in range(n):
                            tmoves.append((i, j, "swap"))
        # dla każdego wygenerowanego ruchu liczymy delte i wstawiamy go do LM
        for move in tmoves:
            if move[2] == "swap":
                i, j = move[0], move[1]
                try:
                    a, b = path1[i], path2[j]
                    prev_i, next_i = path1[(i - 1) % n], path1[(i + 1) % n]
                    prev_j, next_j = path2[(j - 1) % n], path2[(j + 1) % n]
                except IndexError:
                    continue
                delta = -distances[prev_i][a] - distances[a][next_i]
                delta -= distances[prev_j][b] + distances[b][next_j]
                delta += distances[prev_i][b] + distances[b][next_i]
                delta += distances[prev_j][a] + distances[a][next_j]
                if delta < 0:
                    LM.append([("swap", i, j), delta, [(prev_i, a), (a, next_i), (prev_j, b), (b, next_j)]])
            else:
                i, j, _, path_id = move
                if i == j:
                    continue
                current_path = path1 if path_id == 1 else path2
                a, b = current_path[i], current_path[(i + 1) % len(current_path)]
                c, d = current_path[j], current_path[(j + 1) % len(current_path)]
                delta = -distances[a][b] - distances[c][d]
                delta += distances[a][c] + distances[b][d]
                if delta < 0:
                    LM.append([("edge_swap", i, j, path_id), delta, [(a, b), (c, d)]])

    # aktualizacja LM po ostatnim ruchu
    def update_LM_after_move(LM, last_move, path1, path2, distances):
        def is_affected(move_data, changed_nodes, removed_edges):
            if move_data[0] == "swap":
                _, i, j = move_data
                try:
                    v1, v2 = path1[i], path2[j]
                    return v1 in changed_nodes or v2 in changed_nodes
                except IndexError:
                    return True
            elif move_data[0] == "edge_swap":
                _, i, j, path_id = move_data
                current_path = path1 if path_id == 1 else path2
                e1 = (current_path[i], current_path[(i + 1) % len(current_path)])
                e2 = (current_path[j], current_path[(j + 1) % len(current_path)])
                return edge_in_edges(e1, removed_edges) or edge_in_edges(e2, removed_edges)
            return False

        if last_move[0] == "swap":
            i, j = last_move[1], last_move[2]
            changed_nodes = {
                path1[i], path2[j],
                path1[(i - 1) % n], path1[(i + 1) % n],
                path2[(j - 1) % n], path2[(j + 1) % n]
            }
            removed_edges = [
                (path1[(i - 1) % n], path1[i]),
                (path1[i], path1[(i + 1) % n]),
                (path2[(j - 1) % n], path2[j]),
                (path2[j], path2[(j + 1) % n])
            ]
        else:
            i, j, path_id = last_move[1], last_move[2], last_move[3]
            current_path = path1 if path_id == 1 else path2
            start, end = (i - 1) % len(current_path), (j + 1) % len(current_path)
            if start <= end:
                changed_nodes = set(current_path[k] for k in range(start, end + 1))
                removed_edges = [(current_path[k], current_path[(k + 1) % len(current_path)]) for k in range(start, end)]
            else:
                indices = list(range(start, len(current_path))) + list(range(0, end + 1))
                changed_nodes = set(current_path[k] for k in indices)
                removed_edges = [(current_path[k], current_path[(k + 1) % len(current_path)]) for k in indices[:-1]]

        LM = [move for move in LM if not is_affected(move[0], changed_nodes, removed_edges)]
        add_new_moves(LM, path1, path2, distances, last_move)
        return sorted(LM, key=lambda x: (x[1], x[0][1], x[0][2], -ord(x[0][0][0])))


    current_cost = summary_cost(path1, path2, distances)
    LM = deque()
    add_new_moves(LM, path1, path2, distances, None)
    LM = deque(sorted(LM, key=lambda x: (x[1], x[0][1], x[0][2], -ord(x[0][0][0]))))

    while True:
        best_move = None
        length = len(LM)
        for _ in range(length):
            move = LM.popleft()
            move_data, delta, removed_edges = move
            applicability = is_move_applicable(removed_edges, path1, path2)

            if applicability == "remove":
                continue  # nie wrzucamy z powrotem do LM - nieaplikowalny
            elif applicability == "skip":
                LM.append(move)  # odłóż z powrotem do LM - krawędzie są w przeciwnym kierunku
            elif applicability == "apply":
                best_move = move # aplikowalny - wykonaj ruch
                break

        if not best_move:
            break  # brak ruchów aplikowalnych

        # wykonujemy ruch
        move_data, delta, removed_edges = best_move
        if move_data[0] == "swap":
            i, j = move_data[1], move_data[2]
            path1[i], path2[j] = path2[j], path1[i]
        else:
            i, j, path_id = move_data[1], move_data[2], move_data[3]
            current_path = path1 if path_id == 1 else path2
            segment = [current_path[(k) % len(current_path)] for k in range(i + 1, j + 1)]
            for k, idx in enumerate(range(i + 1, j + 1)):
                current_path[idx % len(current_path)] = segment[-(k + 1)]
        # aktualizuj koszt
        current_cost += delta
        # zaktualizuj LM
        LM = deque(update_LM_after_move(list(LM), move_data, path1, path2, distances))
        
    return [path1, path2]