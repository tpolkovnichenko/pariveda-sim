import simulations.monte_carlo as monte_carlo
import simulations.gamblers_ruin as gamblers_ruin
import simulations.polyas_walk as polyas_walk
import simulations.markov_chains as markov_chains
import simulations.cfr_marbles as cfr_marbles
from display import display_title, display_menu, display_summary

def main():
    display_title()
    input("\nPress enter to continue...")
    while True:
        display_menu()
        option = input("Choose a simulation (1-5): ").strip().lower()
        if option == "1":
            monte_carlo.run()
            input("\nPress enter to continue...")
        elif option == "2":
            gamblers_ruin.run()
            input("\nPress enter to continue...")
        elif option == "3":
            polyas_walk.run()
            input("\nPress enter to continue...")
        elif option == "4":
            markov_chains.run()
            input("\nPress enter to continue...")
        elif option == "5":
            cfr_marbles.run()
            input("\nPress enter to continue...")
        elif option == "6":
            display_summary()
        elif option in ("7", "exit", "quit", "q"):
            print("\nExiting The Knot. Goodbye.\n")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
