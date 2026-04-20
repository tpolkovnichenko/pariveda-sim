import simulations.monte_carlo as monte_carlo
import simulations.gamblers_ruin as gamblers_ruin
import simulations.polyas_walk as polyas_walk
import simulations.markov_chains as markov_chains
from display import display_title, display_menu, display_summary

def main():
    display_title()
    input("Press enter to continue...")
    while True:
        display_menu()
        option = input("Choose a simulation (1-4): ").strip().lower()
        if option == "1":
            monte_carlo.run()
            input("Press enter to continue...")
        elif option == "2":
            gamblers_ruin.run()
            input("Press enter to continue...")
        elif option == "3":
            polyas_walk.run()
            input("Press enter to continue...")
        elif option == "4":
            markov_chains.run()
            input("Press enter to continue...")
        elif option == "5":
            display_summary()
        elif option in ("6", "exit", "quit", "q"):
            print("\nExiting The Knot. Goodbye.\n")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
