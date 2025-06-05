import time
import random
from copy import deepcopy
from threading import Thread
from queue import Queue, Empty
from imo6_2 import *  

def run_island(island_id, strategy, init_methods, search_fn,
               distance_matrix, pop_size, T, migration_interval,
               inbound, outbound):
    population = []
    start_time = time.time()
    last_migration = start_time

    iteration_count = 0   
    migration_count = 0  

    # 1) Inicjalizacja populacji
    while len(population) < pop_size:
        init = random.choice(init_methods)
        c1, c2, cost = init(distance_matrix)
        if search_fn:
            c1, c2, cost = search_fn(distance_matrix, c1, c2)
        if not is_duplicate(cost, population):
            population.append((c1, c2, cost))

    # 2) Inicjalna migracja: wyślij losowego migranta z top3
    top3 = sorted(population, key=lambda x: x[2])[:3]
    migrant = random.choice(top3)
    outbound.put(migrant)
    migration_count += 1
    last_sent_cost = migrant[2]

    # 3) Pętla główna ewolucji / LNS
    while time.time() - start_time < T:
        iteration_count += 1

        # === generowanie nowego potomka ===
        if strategy == "LNS":
            base = random.choice(population)
            c1, c2, cost, _ = LNS(distance_matrix,
                                  time_limit=5.0,
                                  c1=base[0], c2=base[1], cost=base[2],
                                  if_LS=True)
        elif strategy == "HAE+DR":
            p1, p2 = select_two_parents(population)
            c1, c2 = recombine(p1[0], p1[1], p2[0], p2[1], distance_matrix)
            c1, c2 = mutate(c1, c2)
            c1, c2 = destroy_repair(c1, c2, distance_matrix)
            c1, c2, cost = search_fn(distance_matrix, c1, c2)
        else:  # HAE
            p1, p2 = select_two_parents(population)
            c1, c2 = recombine(p1[0], p1[1], p2[0], p2[1], distance_matrix)
            c1, c2 = mutate(c1, c2)
            c1, c2, cost = search_fn(distance_matrix, c1, c2)

        # Wymiana z najgorszym, jeśli lepsze i nie-dupikat
        if not is_duplicate(cost, population):
            worst_idx = get_worst_index(population)
            if cost < population[worst_idx][2]:
                population[worst_idx] = (c1, c2, cost)

        # === migracja co migration_interval sekund ===
        now = time.time()
        if now - last_migration >= migration_interval:
            last_migration = now

            # Wybierz losowo jednego z top3 i wyślij, jeśli inny koszt niż ostatni
            top3 = sorted(population, key=lambda x: x[2])[:3]
            candidate = random.choice(top3)
            if candidate[2] != last_sent_cost:
                outbound.put(candidate)
                migration_count += 1
                last_sent_cost = candidate[2]

            # Odbierz migranta, jeśli dostępny i nie duplikat
            try:
                migrant = inbound.get_nowait()
                mcost = migrant[2]
                if not is_duplicate(mcost, population):
                    worst_idx = get_worst_index(population)
                    population[worst_idx] = migrant
            except Empty:
                pass

    # 4) Zwróć wynik wraz z licznikami
    best_solution = min(population, key=lambda x: x[2])  # (c1, c2, cost)
    return best_solution, iteration_count, migration_count


def island_model_run(filename, T=180, pop_size=10, migration_interval=20):
    distance_matrix, coords = load_tsplib_instance(filename)

    # Kolejki migracyjne: 0 → 1 → 2 → 0
    q01 = Queue()
    q12 = Queue()
    q20 = Queue()

    # Wyniki per-wyspa: każda komórka to (best_solution, iteration_count, migration_count)
    island_results = [None] * 3

    def wrapper(i, strategy, init_methods, search_fn, inbound, outbound):
        island_results[i] = run_island(
            i, strategy, init_methods, search_fn,
            distance_matrix, pop_size, T, migration_interval,
            inbound, outbound
        )

    threads = [
        Thread(
            target=wrapper,
            args=(0, "HAE",
                  [nearest_neighbor, greedy_cycle],
                  local_search,
                  q20, q01)
        ),
        Thread(
            target=wrapper,
            args=(1, "HAE+DR",
                  [greedy_cycle,
                   lambda dm: weighted_regret_heuristic(dm, 1.0, -1.0)],
                  local_search,
                  q01, q12)
        ),
        Thread(
            target=wrapper,
            args=(2, "LNS",
                  [lambda dm: weighted_regret_heuristic(dm, 1.0, -1.0)],
                  local_search,
                  q12, q20)
        ),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Wyciągnij wyniki per-wyspa
    # island_results[i] = ((c1, c2, cost), iteration_count, migration_count)
    best_per_island = [res[0] for res in island_results]
    iter_counts = [res[1] for res in island_results]
    migration_counts = [res[2] for res in island_results]

    # Najlepsze rozwiązanie globalne (spośród 3 wysp)
    best_solutions = best_per_island  # lista trzech krotek (c1, c2, cost)
    best_global = min(best_solutions, key=lambda x: x[2])  # (c1, c2, cost)

    return best_global, iter_counts, migration_counts, coords


if __name__ == "__main__":
    filename = "kroA200.tsp"
    T = 461
    pop_size = 10
    migration_interval = 20

    num_runs = 10
    all_costs = []
    sum_iter_per_island = [0, 0, 0]
    sum_mig_per_island = [0, 0, 0]
    sum_total_migrations_per_run = 0

    best_of_all = None  # Najlepsze rozwiązanie spośród wszystkich 10 runów

    for run_idx in range(1, num_runs + 1):
        print(f"=== Uruchomienie {run_idx}/{num_runs} ===")
        best_global, iter_counts, migration_counts, coords = island_model_run(
            filename, T, pop_size, migration_interval
        )
        c1_best, c2_best, cost_best = best_global
        all_costs.append(cost_best)

        # Zaktualizuj najlepsze globalne
        if best_of_all is None or cost_best < best_of_all[2]:
            best_of_all = (c1_best, c2_best, cost_best)

        for i in range(3):
            sum_iter_per_island[i] += iter_counts[i]
            sum_mig_per_island[i] += migration_counts[i]
        sum_total_migrations_per_run += sum(migration_counts)

        print(f"Run {run_idx}: najlepszy koszt = {cost_best:.2f}")
        print(f"  Iteracje per wyspa: {iter_counts}")
        print(f"  Migracje per wyspa: {migration_counts}")
        print()

    # Oblicz statystyki kosztów
    avg_cost = sum(all_costs) / len(all_costs)
    min_cost = min(all_costs)
    max_cost = max(all_costs)

    # Oblicz średnie iteracje i migracje per wyspa
    avg_iter_per_island = [
        sum_iter_per_island[i] / num_runs for i in range(3)
    ]
    avg_mig_per_island = [
        sum_mig_per_island[i] / num_runs for i in range(3)
    ]
    avg_total_migrations_per_run = sum_total_migrations_per_run / num_runs

    print("==== Podsumowanie dla 10 uruchomień ====")
    print(f"Średni koszt: {avg_cost:.2f}")
    print(f"Minimalny koszt: {min_cost:.2f}")
    print(f"Maksymalny koszt: {max_cost:.2f}\n")

    print("Średnia liczba iteracji per wyspa:")
    for i in range(3):
        print(f"  Wyspa {i}: {avg_iter_per_island[i]:.1f}")

    print("\nŚrednia liczba migracji per wyspa:")
    for i in range(3):
        print(f"  Wyspa {i}: {avg_mig_per_island[i]:.1f}")

    print(f"\nŚrednia liczba wszystkich migracji (suma 3 wysp) na 1 run: "
          f"{avg_total_migrations_per_run:.1f}")

    c1_global, c2_global, cost_global = best_of_all
    print(f"\nNajlepsze rozwiązanie spośród 10 uruchomień ma koszt: {cost_global:.2f}")
    plot_solution(coords, c1_global, c2_global, cost_global,
                  title="Najlepsze rozwiązanie spośród 10 uruchomień")
