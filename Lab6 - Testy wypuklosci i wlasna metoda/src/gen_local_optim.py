import json
import os
from tqdm import trange
from utils import read_data, measure_distances, choose_starting_nodes, summary_cost
from starters.randomstart import randomstart
from algo.traverse_greedy_edge import traverse_greedy_edge


def generuj_lokalne_optimy(data, distances, liczba=1000):
    optimy = []
    for _ in trange(liczba, desc="Generowanie lokalnych optymów"):
        starting_paths = randomstart(distances, choose_starting_nodes(data, distances))
        path1, path2 = traverse_greedy_edge(starting_paths, distances)
        koszt = summary_cost(path1, path2, distances)
        optimy.append({
            "cykl1": path1,
            "cykl2": path2,
            "koszt": koszt
        })
    return optimy


if __name__ == "__main__":
    instances = [
        '../data/kroA200.tsp',
        '../data/kroB200.tsp'
    ]

    for insta in instances:
        print(f"\nPrzetwarzanie instancji: {insta}")
        data = read_data(insta)
        distances = measure_distances(data)
        optimy = generuj_lokalne_optimy(data, distances, liczba=1000)

        base = os.path.basename(insta) # Wyodrębnienie np. "kroA" z "../data/kroA200.tsp"
        tag = base.replace("200.tsp", "")  # np. "kroA"
        filename = f"lokalne_optimy_{tag}.json"

        with open(filename, "w") as f:
            json.dump(optimy, f, indent=2)

        print(f"Zapisano do pliku: {filename}")
