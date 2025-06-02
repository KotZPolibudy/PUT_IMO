import numpy as np
from algo.HAE import run_single_instance
import os
from utils import read_data, measure_distances, summary_cost, show_paths
from tabulate import tabulate

def main_repeated_runs(distances, time_limiter=60, pop_size=20, use_local_search=True, use_mutation=False, mutation_rate=0.1, runs=10):
    costs = []
    times = []
    iterations_list = []
    best_overall = None
    best_cost = float('inf')

    for i in range(runs):
        print(f"\nRun {i + 1}/{runs}")
        best_solution, elapsed, iterations = run_single_instance(
            distances, time_limiter, pop_size,
            use_local_search, use_mutation, mutation_rate
        )
        cost = summary_cost(best_solution[0], best_solution[1], distances)
        costs.append(cost)
        times.append(elapsed)
        iterations_list.append(iterations)

        print(f"Cost: {cost:.2f} | Time: {elapsed:.2f}s | Iterations num: {iterations}")

        if best_overall is None or cost < best_cost:
            best_overall = best_solution
            best_cost = cost

    # # Statystyki
    # print("\n   Statystyki po 10 uruchomieniach:")
    # print(f"   ➤ Średni koszt:      {np.mean(costs):.2f}")
    # print(f"   ➤ Min koszt:         {np.min(costs):.2f}")
    # print(f"   ➤ Max koszt:         {np.max(costs):.2f}")
    # print(f"   ➤ Średni czas:       {np.mean(times):.2f}s")
    # print(f"   ➤ Min czas:          {np.min(times):.2f}s")
    # print(f"   ➤ Max czas:          {np.max(times):.2f}s")
    # print(f"   ➤ Średnia liczba iteracji HEA: {np.mean(iterations_list):.1f}")
    # print(f"   ➤ Min iteracji:      {np.min(iterations_list)}")
    # print(f"   ➤ Max iteracji:      {np.max(iterations_list)}")

    return np.min(costs), np.mean(costs), np.max(costs), best_overall, np.min(times), np.mean(times), np.max(times), np.mean(iterations_list)


if __name__ == "__main__":
    instances = [
        '../data/kroA200.tsp',
        '../data/kroB200.tsp'
    ]
    time_limiter = None
    results = []
    flags = [
        { "mutation": False, "local_search": False },
        { "mutation": False, "local_search": True },
        { "mutation": True, "local_search": False },
        { "mutation": True, "local_search": True }
    ]
    os.makedirs("../best_paths", exist_ok=True)
    for insta in instances:
        i = insta.split('/')[-1].split('.')[0]
        os.makedirs(f"../best_paths/{i}", exist_ok=True)

    for insta in instances:
        data = read_data(insta)
        distances = measure_distances(data)
        i = insta.split('/')[-1].split('.')[0]
        print(f"=============================={insta}==============================")
        time_limiter = 269.287 if i == 'kroA200' else 279.947 # wyniki dla poprzedniego sprawozdania, avg. czas MSLS
        for flag in flags:
            found_best, found_avg, found_worst, found_best_paths, bt, avgt, wt, iter_avg = main_repeated_runs(
                distances=distances,
                time_limiter=time_limiter,
                pop_size=20,
                use_local_search=flag["local_search"],
                use_mutation=flag["mutation"],
                mutation_rate=0.1,
                runs=10
            )
            algo_name = "HAE" + ("+Mutation" if flag["mutation"] else "") + ("+LS" if flag["local_search"] else "")
            results.append(
                [insta, algo_name, found_best, found_avg, found_worst, bt, avgt, wt, iter_avg]
            )
            save_path = f"../best_paths/{i}/{os.path.basename(algo_name)}.png"
            show_paths(data, *found_best_paths, save_path)
    
    headers = ["Instance", "Algorytm", "Best", "Avg", "Worst", "Best Time", "Avg Time", "Worst Time", "Avg Iterations Number"]
    print(tabulate(results, headers=headers, tablefmt="grid"))