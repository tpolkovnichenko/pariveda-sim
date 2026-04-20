import random
from collections import defaultdict
from simulations.utilities import save_result, get_int

# Game rules

def get_payoff(hider_bet, guesser_guess):
    # guesser wins the bet if they guess parity correctly, loses it otherwise
    actual_parity = "odd" if hider_bet % 2 == 1 else "even"
    if guesser_guess == actual_parity:
        return hider_bet
    else:
        return -hider_bet

# CFR (Counterfactual Regret Minimization) Algorithm Core

def regret_to_strategy(regrets, actions):
    # convert accumulated regrets into a probability distribution
    positive = [max(0, regrets[a]) for a in actions]
    total = sum(positive)
    if total > 0:
        return [p / total for p in positive]
    return [1 / len(actions)] * len(actions)  # uniform if no regrets yet

def pick_action(actions, strategy):
    return random.choices(actions, weights=strategy)[0]

# Full two-player CFR (Nash Equilibrium Solve)

def train_nash(iterations):
    hider_regrets = defaultdict(lambda: defaultdict(float))
    guesser_regrets = defaultdict(lambda: defaultdict(float))
    hider_strategy_sum = defaultdict(lambda: defaultdict(float))
    guesser_strategy_sum = defaultdict(lambda: defaultdict(float))

    print("\n  Training", end="", flush=True)

    for i in range(iterations):
        if i % (iterations // 20) == 0:
            print(".", end="", flush=True)

        hider_coins = 10
        guesser_coins = 10

        while hider_coins > 0 and guesser_coins > 0:
            state = (hider_coins, guesser_coins)
            hider_actions = list(range(1, hider_coins + 1))
            guesser_actions = ["odd", "even"]

            hider_strat = regret_to_strategy(hider_regrets[state], hider_actions)
            guesser_strat = regret_to_strategy(guesser_regrets[state], guesser_actions)

            for a, s in zip(hider_actions, hider_strat):
                hider_strategy_sum[state][a] += s
            for a, s in zip(guesser_actions, guesser_strat):
                guesser_strategy_sum[state][a] += s

            bet = pick_action(hider_actions,   hider_strat)
            guess = pick_action(guesser_actions, guesser_strat)

            guesser_gain = get_payoff(bet, guess)
            hider_coins -= guesser_gain
            guesser_coins += guesser_gain

            # hider regrets: what if i had bet differently?
            actual_hider = -guesser_gain
            for possible_bet in hider_actions:
                hypothetical = -get_payoff(possible_bet, guess)
                hider_regrets[state][possible_bet] += hypothetical - actual_hider

            # guesser regrets: what if i had guessed the other parity?
            actual_guesser = guesser_gain
            for possible_guess in guesser_actions:
                hypothetical = get_payoff(bet, possible_guess)
                guesser_regrets[state][possible_guess] += hypothetical - actual_guesser

            hider_coins, guesser_coins = guesser_coins, hider_coins

    print(" done.\n")
    return hider_strategy_sum, guesser_strategy_sum

# Exploitative strategy demo (fixed opponent strategy)

def train_guesser_vs_fixed_hider(fixed_hider_bets, iterations=10_000):
    guesser_regrets      = defaultdict(lambda: defaultdict(float))
    guesser_strategy_sum = defaultdict(lambda: defaultdict(float))
    guesser_actions      = ["odd", "even"]

    for _ in range(iterations):
        hider_coins = 10
        guesser_coins = 10
        rounds = 0

        while hider_coins > 0 and guesser_coins > 0 and rounds < 100:
            rounds += 1
            state = (hider_coins, guesser_coins)
            guesser_strat = regret_to_strategy(guesser_regrets[state], guesser_actions)

            for a, s in zip(guesser_actions, guesser_strat):
                guesser_strategy_sum[state][a] += s

            max_bet = min(hider_coins, 10)
            available_bets = list(range(1, max_bet + 1))
            available_probs = fixed_hider_bets[:max_bet]
            total = sum(available_probs)
            normalized = [p / total for p in available_probs]

            bet = pick_action(available_bets, normalized)
            guess = pick_action(guesser_actions, guesser_strat)

            guesser_gain = get_payoff(bet, guess)
            hider_coins -= guesser_gain
            guesser_coins += guesser_gain

            actual_guesser = guesser_gain
            for possible_guess in guesser_actions:
                hypothetical = get_payoff(bet, possible_guess)
                guesser_regrets[state][possible_guess] += hypothetical - actual_guesser

            hider_coins, guesser_coins = guesser_coins, hider_coins

    return guesser_strategy_sum

# Display helpers

def print_nash_results(hider_sum, guesser_sum):
    state = (10, 10)

    print("--- Nash Equilibrium at starting state (10 coins each) ---\n")

    # guesser
    g = guesser_sum[state]
    total = sum(g.values())
    if total > 0:
        odd_pct  = g["odd"]  / total * 100
        even_pct = g["even"] / total * 100
        print(f"  Guesser strategy:")
        print(f"    odd:  {odd_pct:.1f}%  {'-' * int(odd_pct * 0.4)}")
        print(f"    even: {even_pct:.1f}%  {'-' * int(even_pct * 0.4)}")
        print(f"  (Nash prediction: 50% / 50%)\n")

    # hider
    h = hider_sum[state]
    total = sum(h.values())
    if total > 0:
        print(f"  Hider bet distribution:")
        for bet in sorted(h):
            pct = h[bet] / total * 100
            bar = "-" * int(pct * 0.5)
            print(f"    bet {bet:2d}: {pct:5.1f}%  {bar}")
        print(f"\n  (Hider mixes bets to keep guesser indifferent)")


def print_exploitation(label, hider_bets, result):
    state = (10, 10)
    sums  = result[state]
    total = sum(sums.values())
    if total == 0:
        return
    odd_pct  = sums["odd"]  / total * 100
    even_pct = sums["even"] / total * 100

    print(f"\n  Scenario: {label}")
    print(f"    Guesser best response:  odd {odd_pct:.0f}%  even {even_pct:.0f}%")
    dominant = "odd" if odd_pct > even_pct else "even" if even_pct > odd_pct else "50/50"
    if dominant != "50/50":
        print(f"    CFR correctly exploits by guessing {dominant} more often.")
    else:
        print(f"    No exploitable pattern -- guesser stays 50/50.")

# Main run simulation function

def run():
    print("\n--- CFR: Squid Game Marbles (Coins) ---")
    print("Two players each start with 10 coins.")
    print("Each round: the HIDER secretly bets 1-10 coins.")
    print("The GUESSER calls odd or even.")
    print("If correct, guesser wins the bet. If wrong, hider wins it.")
    print("Play continues until one player has all the coins.\n")
    print("Counterfactual Regret Minimization (CFR) is an algorithm that")
    print("learns optimal strategy through self-play. Each iteration it asks:")
    print("'What if I had played differently?' and shifts toward better choices.")
    print("Over millions of iterations it converges to the Nash Equilibrium --")
    print("the strategy no opponent can exploit, no matter what they do.\n")

    iterations = get_int(prompt="Training iterations (recommended: 200,000): ",
                         default=200_000, min_val=50_000, max_val=1_000_000)

    hider_sum, guesser_sum = train_nash(iterations)
    print_nash_results(hider_sum, guesser_sum)

    input("\nPress enter to see exploitation demos...")

    print("\n--- Exploitation: What if the hider plays a fixed strategy? ---")
    print("If the hider deviates from Nash, CFR finds and exploits it.\n")

    # hider bet distributions to test against
    experiments = [
        ("Hider always bets 1 (safest bet)", [1.0] + [0]*9),
        ("Hider always bets 10 (all in)", [0]*9 + [1.0]),
        ("Hider only bets odd amounts", [0.2,0,0.2,0,0.2,0,0.2,0,0.2,0]),
        ("Hider only bets even amounts", [0,0.2,0,0.2,0,0.2,0,0.2,0,0.2]),
        ("Hider bets small (1-3 only)", [0.34,0.33,0.33]+[0]*7)
    ]

    for label, hider_bets in experiments:
        result = train_guesser_vs_fixed_hider(hider_bets, iterations=10_000)
        print_exploitation(label, hider_bets, result)

    print("\nKey insight: at Nash equilibrium the guesser stays 50/50 and")
    print("cannot be exploited. The moment the hider shows any pattern,")
    print("CFR detects it and shifts to punish it.\n")

    save_result("cfr_marbles", {
        "iterations": iterations,
        "game": "squid_game_marbles",
        "algorithm": "counterfactual_regret_minimization",
        "note": "converges to Nash equilibrium through self-play"
    })