def greedy_cheapest_insertion(data, distances, starting_nodes):
  n = len(data)

  def cheapest_insertion(path, distances, visited):
    possibilities = [i for i in range(n) if not visited[i]]
    cheapest_cost = float('inf')
    cheapest_insert = None
    for b in possibilities:
      if visited[b]:
        continue
      for i in range(len(path)-1):
        a, c = path[i], path[i+1]
        cost = distances[a][b] + distances[b][c] - distances[a][c]
        if cost < cheapest_cost:
          cheapest_cost = cost
          cheapest_insert = (i+1, b)
    return cheapest_insert

  start1, start2 = starting_nodes
  path1, path2 = [start1, start1], [start2, start2]
  visited = [False for _ in range(n)]
  visited[start1], visited[start2] = True, True
  while visited.count(False) > 0:
    cheapest_insertion1 = cheapest_insertion(path1, distances, visited)
    if cheapest_insertion1 is None:
      break
    insertion_index1, insertion_town1 = cheapest_insertion1
    path1.insert(insertion_index1, insertion_town1)
    visited[insertion_town1] = True

    cheapest_insertion2 = cheapest_insertion(path2, distances, visited)
    if cheapest_insertion2 is None:
      break
    insertion_index2, insertion_town2 = cheapest_insertion2
    path2.insert(insertion_index2, insertion_town2)
    visited[insertion_town2] = True
  return path1, path2
