import random
import json
import os
from simulations.utilities import save_result

def run():
    print("\n--- Gambler's Ruin + Kelly Criterion ---")
    print("A gambler bets $1 per round until they reach their target or go broke.")
    print("Watch how a tiny house edge changes everything.\n")

    # get user inputs
    start = int(input("Starting amount (e.g. 100): "))
    target = int(input("Target amount (e.g. 200): "))
    p = float(input("Win probability per round (fair = 0.5): "))
    p = max(0.001, min(0.999, p))  # clamp to valid range
    q = 1 - p
    iterations = int(input("How many simulations to run? (recommended: 10,000+): "))
    iterations = min(iterations, 100_000)

    ruins = 0
    total_rounds = 0

    print("\nRunning...")

    for i in range(iterations):
        wallet = start
        rounds = 0
        if i % 1000 == 0:
            print("-", end="", flush=True)
        # play until broke or target reached
        while wallet > 0 and wallet < target:
            rounds += 1
            if random.random() <= p:
                wallet += 1
            else:
                wallet -= 1

        total_rounds += rounds
        if wallet == 0:
            ruins += 1

    # simulated results
    sim_ruin_prob = ruins / iterations
    avg_rounds = total_rounds / iterations

    # theoretical ruin probability
    theo_ruin_prob = theoretical_ruin(start, target, p, q)

    print(f"{'Simulated ruin probability:':30} {sim_ruin_prob:.4f}  ({sim_ruin_prob*100:.2f}%)")
    print(f"{'Theoretical ruin probability:':30} {theo_ruin_prob:.4f}  ({theo_ruin_prob*100:.2f}%)")

    if theo_ruin_prob == 0:
        print(f"{'Error:':30} N/A (theoretical ruin = 0%)")
    else:
        print(f"{'Error:':30} {abs(sim_ruin_prob - theo_ruin_prob) / theo_ruin_prob * 100:.4f}%")

    print(f"{'Average rounds survived:':30} {avg_rounds:.1f}")

    # kelly criterion
    kelly = p - q
    print(f"\n--- Kelly Criterion ---")
    if kelly <= 0:
        print(f"No edge detected (p <= 0.5). Kelly says: don't bet.")
    else:
        print(f"Win edge:                 {kelly*100:.2f}%")
        print(f"Optimal bet fraction:     {kelly*100:.2f}% of bankroll per round")
        print(f"Optimal bet (your start): ${start * kelly:.2f} per round")
        print(f"(Betting more than this increases ruin risk even with an edge)")

    save_result("gamblers_ruin", {
        "start": start,
        "target": target,
        "win_probability": p,
        "simulations": iterations,
        "sim_ruin_probability": round(sim_ruin_prob, 4),
        "theoretical_ruin_probability": round(theo_ruin_prob, 4),
        "avg_rounds_survived": round(avg_rounds, 1),
        "kelly_fraction": round(kelly, 4) if kelly > 0 else "no edge"
    })


def theoretical_ruin(start, target, p, q):
    if p == 0.5:
        return (target - start) / target
    else:
        ratio = q / p
        win_probability = (1 - ratio ** start) / (1 - ratio ** target)
        return 1 - win_probability