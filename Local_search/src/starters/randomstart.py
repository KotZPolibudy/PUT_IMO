import random


def randomstart(distances, starting_nodes):
    n = len(distances)
    start1, start2 = starting_nodes
    remaining_nodes = [node for node in range(n) if node not in {start1, start2}]
    random.shuffle(remaining_nodes)
    nodes1 = [start1] + remaining_nodes[:len(remaining_nodes) // 2]
    nodes2 = [start2] + remaining_nodes[len(remaining_nodes) // 2:]
    nodes1.append(nodes1[0])
    nodes2.append(nodes2[0])
    return nodes1, nodes2
