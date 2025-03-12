def greedy_nearest_neighbor(data, distances, starting_nodes):
  n = len(data)

  def nearest_neighbor(town_id, distances, visited):
    nearest = None
    for i in range(n):
      if i == town_id or visited[i]:
        continue
      if nearest is None or distances[town_id][i] < distances[town_id][nearest]:
        nearest = i
    return nearest

  start1, start2 = starting_nodes
  path1, path2 = [start1], [start2]
  visited = [False for _ in range(n)]
  visited[start1], visited[start2] = True, True
  while visited.count(False) > 0:
    path1_continuation = nearest_neighbor(path1[-1], distances, visited)
    path1.append(start1 if path1_continuation is None else path1_continuation)
    visited[path1[-1]] = True
    path2_continuation = nearest_neighbor(path2[-1], distances, visited)
    path2.append(start2 if path2_continuation is None else path2_continuation)
    visited[path2[-1]] = True
  if path1[-1] != start1:
    path1.append(start1)
  if path2[-1] != start2:
    path2.append(start2)
  return path1, path2
