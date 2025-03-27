import random


def randomstart(distances, starting_nodes):
    n = len(distances)
    start1, start2 = starting_nodes
    remaining_nodes = [node for node in range(n) if node not in {start1, start2}]
    random.shuffle(remaining_nodes)
    nodes1 = [start1] + remaining_nodes[:len(remaining_nodes) // 2]
    nodes2 = [start2] + remaining_nodes[len(remaining_nodes) // 2:]
    return nodes1, nodes2
