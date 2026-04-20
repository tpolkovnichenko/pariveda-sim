import json
import os

def save_result(sim_name, result_dict):
    filepath = "data/results.json"
    all_results = {}

    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, "r") as f:
            all_results = json.load(f)

    if sim_name not in all_results:
        all_results[sim_name] = []
    all_results[sim_name].append(result_dict)

    with open(filepath, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResult saved to data/results.json")