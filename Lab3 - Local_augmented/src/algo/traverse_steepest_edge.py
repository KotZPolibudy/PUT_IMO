from utils import summary_cost

def traverse_steepest_edge(starting_paths, distances):
    cycle1 = starting_paths[0]
    cycle2 = starting_paths[1]
    n = len(cycle2)
    
    current_cost = summary_cost(cycle1, cycle2, distances)
    improved = True
    while improved:
        improved = False
        best_move = None
        best_delta = 0
        moves = []

        for i in range(n):
            for j in range(n):
                moves.append((i, j, "swap"))

        for cycle in [cycle1, cycle2]:
            for i in range(n - 1):
                for j in range(i + 1, n):
                    moves.append((i, j, "edge_swap", cycle))

        for move in moves:
            if move[2] == "swap":
                i, j, _ = move
                a, b = cycle1[i], cycle2[j]
                delta = 0
                for ni, cycle, node in [(i, cycle1, a), (j, cycle2, b)]:
                    prev = cycle[ni - 1]
                    next = cycle[(ni + 1) % n]
                    new_node = b if cycle is cycle1 else a
                    delta += distances[prev][new_node] + distances[new_node][next]
                    delta -= distances[prev][node] + distances[node][next]
                if delta < best_delta or (best_move is not None and (delta == best_delta and i < best_move[1])) or (best_move is not None and (delta == best_delta and i == best_move[1] and j < best_move[2]) or (best_move is not None and (delta == best_delta and i == best_move[1] and j == best_move[2] and move[2] == "swap"))):
                    best_delta = delta
                    best_move = ("swap", i, j)
            else:
                i, j, _, cycle = move
                if i >= j:
                    continue
                a, b = cycle[i], cycle[(i + 1) % n]
                c, d = cycle[j], cycle[(j + 1) % n]
                delta = -distances[a][b] - distances[c][d]
                delta += distances[a][c] + distances[b][d]
                if delta < best_delta or (best_move is not None and (delta == best_delta and i < best_move[1])) or (best_move is not None and (delta == best_delta and i == best_move[1] and j < best_move[2]) or (best_move is not None and (delta == best_delta and i == best_move[1] and j == best_move[2] and move[2] == "swap"))):
                    best_delta = delta
                    best_move = ("edge_swap", i, j, cycle)

        if best_move:
            improved = True
            move_type = best_move[0]
            if move_type == "swap":
                i, j = best_move[1], best_move[2]
                cycle1[i], cycle2[j] = cycle2[j], cycle1[i]
            else:
                i, j, cycle = best_move[1], best_move[2], best_move[3]
                cycle[i + 1:j + 1] = reversed(cycle[i + 1:j + 1])
            current_cost += best_delta

    return [cycle1, cycle2]