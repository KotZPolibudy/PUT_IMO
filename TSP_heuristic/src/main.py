import random
import matplotlib.pyplot as plt

class Town:
  def __init__(self, id, x, y):
    self.id = id
    self.x = x
    self.y = y
  
  def distance_to(self, town):
    return ((self.x - town.x)**2 + (self.y - town.y)**2)**0.5

def read_data(path):
  with open(path, 'r') as file:
    data = file.readlines()
    data = [x.strip() for x in data]
    data = data[6:-1]
    data = [x.split() for x in data]
    data = [Town(id=int(x[0]), x=int(x[1]), y=int(x[2])) for x in data]
  return data

def measure_distances(data):
  n = len(data)
  distances = [[0 for _ in range(n)] for _ in range(n)]
  for i in range(n):
    for j in range(i+1, n):
      distances[i][j] = round(data[i].distance_to(data[j]))
      distances[j][i] = distances[i][j]
  return distances

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

def greedy_cheapest_insertion(data, distances, starting_nodes):
  n = len(data)

  def cheapest_insertion(path, distances, visited):
    possiblities = [i for i in range(n) if not visited[i]]
    cheapest_cost = float('inf')
    cheapest_insert = None
    for b in possiblities:
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

def two_regret(data, distances, starting_nodes, use_weights=False):
  n = len(data)

  def calc_regret(path, distances, visited, use_weights=False, w1=1, w2=-1):
    possibilites = [i for i in range(n) if not visited[i]]
    max_regret = -1
    best_insert = None
    for b in possibilites:
      insertion_costs = []
      for i in range(len(path)-1):
          a, c = path[i], path[i+1]
          cost = distances[a][b] + distances[b][c] - distances[a][c]
          insertion_costs.append((cost, i+1))
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
    return best_insert
  
  start1, start2 = starting_nodes
  path1, path2 = [start1, start1], [start2, start2]
  visited = [False for _ in range(n)]
  visited[start1], visited[start2] = True, True
  while visited.count(False) > 0:
    best_insert1 = calc_regret(path1, distances, visited, use_weights)
    if best_insert1:
      insert_index1, town1 = best_insert1
      path1.insert(insert_index1, town1)
      visited[town1] = True
    best_insert2 = calc_regret(path2, distances, visited, use_weights)
    if best_insert2:
      insert_index2, town2 = best_insert2
      path2.insert(insert_index2, town2)
      visited[town2] = True
  return path1, path2

def weighted_two_regret(data, distances, starting_nodes):
  return two_regret(data, distances, starting_nodes, use_weights=True)

def path_cost(path, distances):
  return sum(distances[path[i]][path[i+1]] for i in range(len(path)-1))

def summary_cost(path1, path2, distances):
  return path_cost(path1, distances) + path_cost(path2, distances)

def show_paths(data, path1, path2):
  x = [town.x for town in data]
  y = [town.y for town in data]
  plt.scatter(x, y)
  for i in range(len(path1)-1):
    plt.plot([data[path1[i]].x, data[path1[i+1]].x], [data[path1[i]].y, data[path1[i+1]].y], 'r')
  for i in range(len(path2)-1):
    plt.plot([data[path2[i]].x, data[path2[i+1]].x], [data[path2[i]].y, data[path2[i+1]].y], 'b')
  plt.show()

def choose_starting_nodes(data, distances):
  n = len(data)
  first = random.randint(0, n-1)
  second = max(range(n), key=lambda x: distances[first][x])
  return first, second

def use_algorithm(algorithm, data, distances):
  return algorithm(data, distances, choose_starting_nodes(data, distances))

def algorithm_loop(algorithm, data, distances, n=100):
  costs = 0
  best_cost = float('inf')
  best_paths = None, None
  for _ in range(n):
    paths = use_algorithm(algorithm, data, distances)
    if paths is None:
      return None, None, None
    cost = summary_cost(*paths, distances)
    costs += cost
    if cost < best_cost:
      best_cost = cost
      best_paths = paths
  return best_cost, costs/n, best_paths

if __name__ == '__main__':
  paths = ['data/' + f'kro{i}200.tsp' for i in ['A', 'B']]
  algorithms = [
      greedy_nearest_neighbor,
      greedy_cheapest_insertion,
      two_regret,
      weighted_two_regret
  ]
  for path in paths:
      data = read_data(path)
      distances = measure_distances(data)
      for algorithm in algorithms:
          best_cost, avg_cost, best_paths = algorithm_loop(algorithm, data, distances)
          if best_cost is None or avg_cost is None or best_paths is None:
              print(f'{algorithm.__name__} skipping due to lack of implementation')
              continue
          print(f'{algorithm.__name__} on {path}:')
          print(f'Best cost: {best_cost}')
          print(f'Average cost: {avg_cost}')
          show_paths(data, *best_paths)
  