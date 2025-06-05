import json
from utils import *
from tqdm import trange  # dla paska postępu, opcjonalne
from starters.randomstart import randomstart
from algo.traverse_greedy_edge import traverse_greedy_edge
import random


def generuj_lokalne_optimy(data, distances, liczba=1000):
    optimy = []
    for _ in trange(liczba, desc="Generowanie lokalnych optymów"):
        starting_paths = randomstart(distances, choose_starting_nodes(data, distances))
        local_optim = traverse_greedy_edge(starting_paths, distances)
        optimy.append({
            "cykl1": local_optim["cykl1"],
            "cykl2": local_optim["cykl2"],
            "koszt": local_optim["koszt"]
        })
    return optimy


if __name__ == "__main__":
    instances = [
        '../data/kroA200.tsp',
        '../data/kroB200.tsp'
    ]
    for insta in instances:
        data = read_data(insta)
        distances = measure_distances(data)
        optimy = generuj_lokalne_optimy(data, distances, liczba=1000)

    with open("lokalne_optimy.json", "w") as f:
        json.dump(optimy, f, indent=2)
