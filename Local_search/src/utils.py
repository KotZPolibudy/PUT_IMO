import random
import matplotlib.pyplot as plt


class Town:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def distance_to(self, town):
        return ((self.x - town.x) ** 2 + (self.y - town.y) ** 2) ** 0.5


def read_data(path):
    with open(path, 'r') as file:
        data = file.readlines()
        data = [x.strip() for x in data]
        data = data[6:-1]
        data = [x.split() for x in data]
        data = [Town(id=int(x[0]), x=int(x[1]), y=int(x[2])) for x in data]
    return data


def path_cost(path, distances):
    return sum(distances[path[i]][path[i + 1]] for i in range(len(path) - 1))


def summary_cost(path1, path2, distances):
    return path_cost(path1, distances) + path_cost(path2, distances)


def measure_distances(data):
    n = len(data)
    distances = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            distances[i][j] = round(data[i].distance_to(data[j]))
            distances[j][i] = distances[i][j]
    return distances


def choose_starting_nodes(data, distances):
    n = len(data)
    first = random.randint(0, n - 1)
    second = max(range(n), key=lambda x: distances[first][x])
    return first, second


def show_paths(data, path1, path2, save_path=None, show=False):
    x = [town.x for town in data]
    y = [town.y for town in data]
    plt.scatter(x, y)
    for i in range(len(path1) - 1):
        plt.plot([data[path1[i]].x, data[path1[i + 1]].x], [data[path1[i]].y, data[path1[i + 1]].y], 'r')
    for i in range(len(path2) - 1):
        plt.plot([data[path2[i]].x, data[path2[i + 1]].x], [data[path2[i]].y, data[path2[i + 1]].y], 'b')

    if save_path:
        dir_name = os.path.dirname(save_path)
        if dir_name and not os.path.exists(dir_name):
            os.mkdir(save_path)
        plt.savefig(save_path)

    if show:
        plt.show()

    plt.close()
