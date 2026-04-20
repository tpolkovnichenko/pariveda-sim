import random
import json
import os
import math

# actual pi constant to compare
PI = math.pi

def run():
    print("\n--- Pi Estimation via Monte Carlo Simulation ---")
    print("Randomly throwing darts at a unit square.")
    print("Darts landing inside the quarter-circle reveal pi.\n")

    # ask the user how many iterations to run

    iterations = input("How many darts to throw? (recommended: 100,000+): ")
    if not iterations.isdigit():
        iterations = 100_000
    else:
        iterations = min(int(iterations), 10_000_000) # cap iterations to 10 million

    hits = 0

    print("\nRunning...\n")

    print(f"{'Darts':>11}  {'Pi Estimate':>16}  {'Error %':>9}")
    print("-" * 42)

    for i in range(iterations):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1:
            hits += 1

        # print progress at every 10% milestone
        if (i + 1) % (iterations // 10) == 0:
            current_estimate = hits / (i + 1) * 4
            error = abs(current_estimate - PI) / PI * 100
            print(f"{i+1:>12}  {current_estimate:>14.6f}  {error:>9.4f}%")

    # calculate pi estimate
    pi_estimate = hits / iterations * 4

    print(f"Darts thrown:   {iterations}")
    print(f"Hits inside:    {hits}")
    print(f"Pi estimate:    {pi_estimate:.6f}")
    print(f"Actual pi:      {PI}")
    print(f"Error:          {abs(pi_estimate - PI) / PI * 100:.4f}%")

    # save results to data/results.json
    save_result("pi_estimation", {
        "iterations": iterations,
        "hits": hits,
        "pi_estimate": round(pi_estimate, 6),
        "actual_pi": PI,
        "error_percent": round(abs(pi_estimate - PI) / PI * 100, 4)
    })


def save_result(sim_name, result_dict):
    # load existing results if the file exists
    filepath = "data/results.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            all_results = json.load(f)
    else:
        all_results = {}

    # add this result under the simulation name
    if sim_name not in all_results:
        all_results[sim_name] = []
    all_results[sim_name].append(result_dict)

    # write back to file
    with open(filepath, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResult saved to {filepath}")