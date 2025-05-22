import random
import time
from algo.local_LM import local_LM
from utils import summary_cost
from starters.randomstart import randomstart

def generate_initial_population(distances, pop_size=20):
    population = []
    for _ in range(pop_size):
        starting_nodes = random.sample(range(len(distances)), 2)
        starting_paths = randomstart(distances, starting_nodes)
        path1, path2 = local_LM(starting_paths, distances)
        cost = summary_cost(path1, path2, distances)
        population.append((path1, path2, cost))
    return population

def is_duplicate(candidate_cost, population):
    return any(abs(candidate_cost - indiv[2]) < 1e-6 for indiv in population)

def get_worst_index(population):
    return max(range(len(population)), key=lambda i: population[i][2])

def select_two_parents(population):
    return random.sample(population, 2)

def recombine(c1_a, c2_a, c1_b, c2_b, distances):
    def edges(path):
        return {(path[i], path[(i + 1) % len(path)]) for i in range(len(path))} | \
               {(path[(i + 1) % len(path)], path[i]) for i in range(len(path))}

    # Wybierz rodzica bazowego
    if random.random() < 0.5:
        base_c1, base_c2 = c1_a[:], c2_a[:]
        other_c1, other_c2 = c1_b, c2_b
    else:
        base_c1, base_c2 = c1_b[:], c2_b[:]
        other_c1, other_c2 = c1_a, c2_a

    # Zbiór krawędzi drugiego rodzica
    ref_edges = edges(other_c1) | edges(other_c2)

    # Usuń krawędzie niewspólne z bazowego rozwiązania
    def filter_path(path):
        new_path = []
        n = len(path)
        for i in range(n):
            u, v = path[i], path[(i + 1) % n]
            if (u, v) in ref_edges or (v, u) in ref_edges:
                new_path.append(u)
        return list(dict.fromkeys(new_path))  # usuń duplikaty

    base_c1 = filter_path(base_c1)
    base_c2 = filter_path(base_c2)

    # Zbierz wierzchołki pozostałe do wstawienia
    all_nodes = set(range(len(distances)))
    used_nodes = set(base_c1 + base_c2)
    remaining_nodes = list(all_nodes - used_nodes)
    random.shuffle(remaining_nodes)

    # Naprawa – greedy insertion
    def insert_best(node, path):
        best_pos = None
        best_increase = float("inf")
        for i in range(len(path)):
            prev, nxt = path[i], path[(i + 1) % len(path)]
            increase = (
                distances[prev][node]
                + distances[node][nxt]
                - distances[prev][nxt]
            )
            if increase < best_increase:
                best_increase = increase
                best_pos = i + 1
        path.insert(best_pos, node)

    # Wstawiamy każdy node do najkrótszego cyklu
    while remaining_nodes:
        node = remaining_nodes.pop()
        if len(base_c1) < len(base_c2):
            insert_best(node, base_c1)
        else:
            insert_best(node, base_c2)

    # Upewnij się, że cykle są równo liczne
    while len(base_c1) > len(base_c2):
        insert_best(base_c1.pop(), base_c2)
    while len(base_c2) > len(base_c1):
        insert_best(base_c2.pop(), base_c1)

    return base_c1, base_c2

def mutate(c1, c2, mutation_rate=0.1):
    for path in (c1, c2):
        if random.random() < mutation_rate:
            choice = random.choice(['swap', 'invert', 'relocate'])
            n = len(path)
            if choice == 'swap':
                i, j = random.sample(range(n), 2)
                path[i], path[j] = path[j], path[i]
            elif choice == 'invert' and n > 2:
                i, j = sorted(random.sample(range(n), 2))
                path[i:j+1] = reversed(path[i:j+1])
            elif choice == 'relocate':
                i = random.randrange(n)
                node = path.pop(i)
                j = random.randrange(n)
                path.insert(j, node)
    return c1, c2
  
def run_single_instance(distances, time_limiter, pop_size, use_local_search, use_mutation, mutation_rate):
    population = generate_initial_population(distances, pop_size=pop_size)

    start_time = time.time()
    best_cost = min(population, key=lambda x: x[2])[2]
    best_solution = min(population, key=lambda x: x[2])

    iterations = 0

    while time.time() - start_time < time_limiter:
        iterations += 1
        parent1, parent2 = select_two_parents(population)

        child_c1, child_c2 = recombine(
            parent1[0], parent1[1],
            parent2[0], parent2[1],
            distances
        )

        if use_mutation:
            child_c1, child_c2 = mutate(child_c1, child_c2, mutation_rate)

        if use_local_search:
            child_c1, child_c2 = local_LM([child_c1, child_c2], distances)
            child_cost = summary_cost(child_c1, child_c2, distances)
        else:
            child_cost = summary_cost(child_c1, child_c2, distances)

        worst_idx = get_worst_index(population)
        if child_cost < population[worst_idx][2] and not is_duplicate(child_cost, population):
            population[worst_idx] = (child_c1, child_c2, child_cost)
            if child_cost < best_cost:
                best_cost = child_cost
                best_solution = [child_c1, child_c2]

    elapsed_time = time.time() - start_time
    return best_solution, elapsed_time, iterations