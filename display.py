import os

def display_title():
    print(f"{'THE KNOT':>20}")
    print("A Probability and Simulation Engine\n")
    print("Each module poses a problem where human intuition")
    print("fails and math wins. Randomness, applied at a large")
    print("enough scale, converges to mathematical truth.\n")
    print("Choose menu option 'about this program' to read more on each algorithm")
    
def display_menu():
    print("\n1. Pi Estimation (Monte Carlo)")
    print("2. Gambler's ruin")
    print("3. Polya's random walk")
    print("4. Markov chains")
    print("5. CFR: Squid Game Marbles")
    print("6. About this program")
    print("7. Exit")

def display_summary():
    filepath = "summary.txt"
    print("\n" + "-"*30)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            print(f.read())
    else:
        print("summary.txt not found.")
    print("\n" + "-"*30)
    input("\nPress enter to return to menu...")
