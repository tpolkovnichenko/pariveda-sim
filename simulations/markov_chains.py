import random
import json
import os
import numpy as np

# Part 1: Simple Markov Chain warm-up

# 5 states with transition probabilities
# each row must sum to 1.0
TRANSITIONS = {
    "A": {"A": 0.1, "B": 0.4, "C": 0.2, "D": 0.2, "E": 0.1},
    "B": {"A": 0.3, "B": 0.1, "C": 0.3, "D": 0.1, "E": 0.2},
    "C": {"A": 0.1, "B": 0.2, "C": 0.1, "D": 0.4, "E": 0.2},
    "D": {"A": 0.2, "B": 0.1, "C": 0.3, "D": 0.1, "E": 0.3},
    "E": {"A": 0.3, "B": 0.2, "C": 0.1, "D": 0.3, "E": 0.1},
}

STATES = list(TRANSITIONS.keys())


def run():
    print("\n--- Markov Chain Simulator ---")
    print("A Markov chain is a system that jumps between states randomly.")
    print("The key property: the next state depends only on the current state.")
    print("Run it long enough and it settles into a stationary distribution -")
    print("a stable probability of being in each state regardless of where you started.\n")

    run_warmup()

    input("\nPress enter to continue to the Dark DNA solver...")
    run_dark()


# Warm-up: simulate the 5-state chain

def run_warmup():
    print("-- Part 1: Simple 5-State Markov Chain --\n")
    print("States: A B C D E")
    print("Each state has defined probabilities of jumping to any other state.")
    print("We simulate a random walker and track how often it visits each state.\n")

    steps = int(input("How many steps to simulate? (recommended: 50,000+): "))
    steps = min(steps, 500_000)

    state = random.choice(STATES)
    counts = {s: 0 for s in STATES}

    for i in range(steps):
        if i % 10_000 == 0:
            print("-", end="", flush=True)
        # pick next state based on transition probabilities
        transitions = TRANSITIONS[state]
        roll = random.random()
        cumulative = 0.0
        for next_state, prob in transitions.items():
            cumulative += prob
            if roll < cumulative:
                state = next_state
                break
        counts[state] += 1

    print(f"\n{'State':<8} {'Visits':>8} {'Simulated %':>13} {'Bar'}")
    print("-" * 50)

    for s in STATES:
        pct = counts[s] / steps * 100
        bar = "#" * int(pct / 2)
        print(f"{s:<8} {counts[s]:>8} {pct:>12.2f}%  {bar}")

    print("\nNo matter which state you start from, these proportions stay the same.")
    print("That's the stationary distribution - the chain's equilibrium.\n")


# Dark DNA solver

# character list - N = Normal timeline, A = Alternate timeline
NAMES = [
    "N jonas", "A martha", "N martha", "AN unknown",
    "A hannah", "N hannah", "N jana", "A jana",
    "N mikkel", "A mikkel", "A ulrich", "N ulrich",
    "N katharina", "A katharina", "N tronte", "A tronte",
    "N agnes", "A agnes", "N bart", "A bart",
    "N regina", "A regina", "N alexander", "A alexander",
    "A silja", "N silja", "A claudia", "N claudia",
    "A bernd", "N bernd", "A egon", "N egon",
    "A doris", "N doris", "A noah", "N noah",
    "N charlotte", "A charlotte", "N elizabeth", "A elizabeth",
    "N franziska", "A franziska", "N peter", "A peter",
    "N magnus", "A magnus", "N mads", "A mads",
    "N helge", "A helge", "N greta", "A greta"
]

# child -> (parent1, parent2)
PARENTS = {
    "AN unknown": ("N jonas", "A martha"),
    "N jonas": ("N mikkel", "N hannah"),
    "N mikkel": ("N ulrich", "N katharina"),
    "A mikkel": ("A ulrich", "A katharina"),
    "N ulrich": ("N tronte", "N jana"),
    "A ulrich": ("A jana", "A tronte"),
    "N tronte": ("N agnes", "AN unknown"),
    "N agnes": ("N bart", "N silja"),
    "N silja": ("N hannah", "N egon"),
    "N bart": ("N regina", "N alexander"),
    "N regina": ("N claudia", "N bernd"),
    "N claudia": ("N doris", "N egon"),
    "A martha": ("A ulrich", "A katharina"),
    "N martha": ("N ulrich", "N katharina"),
    "A tronte": ("AN unknown", "A agnes"),
    "A agnes": ("A bart", "A silja"),
    "A silja": ("A hannah", "A egon"),
    "A bart": ("A regina", "A alexander"),
    "A regina": ("A claudia", "A bernd"),
    "A claudia": ("A doris", "A egon"),
    "N magnus": ("N ulrich", "N katharina"),
    "A magnus": ("A ulrich", "A katharina"),
    "N mads": ("N jana", "N tronte"),
    "A mads": ("A jana", "A tronte"),
    "N elizabeth": ("N charlotte", "N peter"),
    "N charlotte": ("N noah", "N elizabeth"),
    "A elizabeth": ("A charlotte", "A peter"),
    "A charlotte": ("A noah", "A elizabeth"),
    "A noah": ("A silja", "A bart"),
    "N noah": ("N silja", "N bart"),
    "N franziska": ("N charlotte", "N peter"),
    "A franziska": ("A charlotte", "A peter"),
}


def run_dark():
    print("Part 2: The Dark Knot: Paradoxical Ancestry through Markov Chains\n")
    print("Dark is a German sci-fi series built around time-travel paradoxes.")
    print("Characters travel between timelines and become their own ancestors,")
    print("creating family loops with no clear origin - called 'the knot'.\n")
    print("We model each character's genetics as a Markov chain inheritance matrix.")
    print("Each character gets 50% DNA from each parent. But parents can be")
    print("descendants of the child - a logical impossibility.")
    print("Multiplying the matrix by itself 1000 times finds the stable equilibrium:")
    print("what percentage of each ancestor a character actually IS.\n")
    print("Note: this Markov chain model was originally developed as a personal")
    print("side project and adapted here for demonstration.\n")

    # show available characters
    unique = sorted(set(n.split(" ", 1)[1] for n in NAMES))
    print("Characters available:")
    for i, name in enumerate(unique):
        print(f"  {i+1:>2}. {name}")

    choice = input("\nEnter character name exactly as shown (e.g. jonas, martha): ").strip().lower()

    # try both timelines
    n_target = "N " + choice
    a_target = "A " + choice

    if n_target not in NAMES and a_target not in NAMES and "AN " + choice not in NAMES:
        print(f"Character '{choice}' not found.")
        return

    targets = []
    if n_target in NAMES:
        targets.append(n_target)
    if a_target in NAMES:
        targets.append(a_target)
    if "AN " + choice in NAMES:
        targets.append("AN " + choice)

    for target in targets:
        print(f"\n--- Solving: {target} ---\n")
        result = solve_dna(target)

        print(f"{'Ancestor':<14} {'DNA %':>8}")
        print("-" * 26)
        for name, val in sorted(result.items(), key=lambda x: -x[1]):
            if val > 1e-6:
                bar = "#" * int(val * 40)
                print(f"{name:<14} {val*100:>7.3f}%  {bar}")


def solve_dna(target):
    N = len(NAMES)
    name_to_idx = {name: i for i, name in enumerate(NAMES)}
    idx_to_name = {i: name for i, name in enumerate(NAMES)}

    # build inheritance matrix
    M = np.zeros((N, N))
    for i in range(N):
        M[i, i] = 1.0  # default: inherit from self

    for child, (p1, p2) in PARENTS.items():
        i = name_to_idx[child]
        j1 = name_to_idx[p1]
        j2 = name_to_idx[p2]
        M[i, :] = 0.0
        M[i, j1] = 0.5
        M[i, j2] = 0.5

    # initial vector - start as 100% this character
    v = np.zeros(N)
    v[name_to_idx[target]] = 1.0

    # iterate 1000 times - find the equilibrium
    for _ in range(1000):
        v = v @ M

    v /= v.sum()

    # merge A/N versions of same person
    merged = {}
    for i in range(N):
        name = idx_to_name[i]
        for prefix in ("AN ", "N ", "A "):
            name = name.removeprefix(prefix)
            break
        merged[name] = merged.get(name, 0.0) + v[i]

    return merged


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

    print(f"\nResult saved to {filepath}")