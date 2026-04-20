import random
import json
import os
from simulations.utilities import save_result, get_int

# theoretical return probabilities by dimension
THEORETICAL = {
    "1D": 1.0,
    "2D": 1.0,
    "3D": 0.3405   # Polya's proven constant
}

STEP_LIMITS = {
    "1D": 5_000,
    "2D": 15_000,   # needs much more room
    "3D": 5_000    # escapes fast, 10k is fine
}

def run():
    print("\n--- Polya's Random Walk ---")
    print("A walker takes random steps from the origin. Will they ever return home?")
    print("In 1D and 2D: return is theoretically guaranteed (probability = 1.0).")
    print("In 3D: the walker escapes forever with ~66% probability.")
    print("This is Polya's Theorem -- one of the most surprising results in math.\n")

    simulations = get_int(prompt="How many walks to simulate per dimension? (recommended: 5,000+): ",
                          default=5_000, min_val=500, max_val=20_000)

    print()

    results = {}

    for dim in ["1D", "2D", "3D"]:
        returns = 0

        print(f"Simulating {dim}...")

        for i in range(simulations):
            returned, steps = simulate_walk(dim, STEP_LIMITS[dim])
            if i % 500 == 0:
                print("-", end="", flush=True)
            if returned:
                returns += 1

        rate = returns / simulations
        theo = THEORETICAL[dim]
        results[dim] = {"return_rate": rate, "theoretical": theo}

        print(f"\nDone.\n")

    # print comparison table
    print(f"\n{'Dimension':<12} {'Simulated':>12} {'Theoretical':>13} {'Error':>10}")
    print("-" * 52)

    for dim, data in results.items():
        sim = data["return_rate"]
        theo = data["theoretical"]
        if theo == 1.0:
            error_str = "N/A (limit)"
        else:
            error_str = f"{abs(sim - theo) / theo * 100:.4f}%"
        print(f"{dim:<12} {sim:>11.4f}  {theo:>12.4f}  {error_str:>10}")

    print("\nKey insight: the moment you add a third dimension, the walker")
    print("can escape to infinity. 2D is the last dimension where you're")
    print("guaranteed to find your way home.\n")

    print("Note: 2D return probability is theoretically 1.0 with infinite steps.")
    print("However, 2D walks have INFINITE expected return time. Some walks")
    print(f"need billions of steps, which is why we observe ~{results['2D']['return_rate']:.2f} rather than 1.0.")
    print("This gap itself is one of the most counterintuitive results in probability.")
    input("Press enter to continue... ")

    # show one live 1D walk visualization
    print("\n--- Live 2D Walk Visualization ---")
    print("'+' marks visited cells, '*' is final position, '0' is home.\n")
    input("Press enter to run a visual sim for 2D: ")
    visualize_2d_walk(steps=3000, grid_size=15)

    save_result("polyas_walk", {
        "simulations_per_dimension": simulations,
        "1D_step_limit": STEP_LIMITS["1D"],
        "2D_step_limit": STEP_LIMITS["2D"],
        "3D_step_limit": STEP_LIMITS["3D"],
        "1D_return_rate": round(results["1D"]["return_rate"], 4),
        "2D_return_rate": round(results["2D"]["return_rate"], 4),
        "3D_return_rate": round(results["3D"]["return_rate"], 4),
        "theoretical_3D": THEORETICAL["3D"]
    })

def simulate_walk(dim, step_limit):
    # define all possible moves for each dimension
    moves_1d = [1, -1]
    moves_2d = [(0,1), (0,-1), (1,0), (-1,0)]
    moves_3d = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]

    if dim == "1D":
        position = 0
        for step in range(1, step_limit + 1):
            position += random.choice(moves_1d)
            if position == 0:
                return (True, step)

    elif dim == "2D":
        x, y = 0, 0
        for step in range(1, step_limit + 1):
            move = random.choice(moves_2d)
            x += move[0]
            y += move[1]
            if x == 0 and y == 0:
                return (True, step)

    elif dim == "3D":
        x, y, z = 0, 0, 0
        for step in range(1, step_limit + 1):
            move = random.choice(moves_3d)
            x += move[0]
            y += move[1]
            z += move[2]
            if x == 0 and y == 0 and z == 0:
                return (True, step)

    return (False, step_limit)

def visualize_2d_walk(steps=3000, grid_size=20):
    x, y = 0, 0
    path = [(0, 0)]
    moves = [(0,1), (0,-1), (1,0), (-1,0)]

    returned_at = None

    for step in range(1, steps + 1):
        move = random.choice(moves)
        x += move[0]
        y += move[1]
        path.append((x, y))

        if x == 0 and y == 0 and returned_at is None:
            returned_at = step  # note it but keep walking

    print_2d_grid(path, grid_size)

    if returned_at:
        print(f"  First return home: step {returned_at}. Walk continued for {steps} total steps.")
    else:
        print(f"  Walker never returned home in {steps} steps.")
    print(f"  Total cells visited: {len(set(path))}")


def print_2d_grid(path, grid_size):
    # build empty grid
    grid = [["." for _ in range(grid_size * 2 + 1)] for _ in range(grid_size * 2 + 1)]

    for (x, y) in path:
        # clamp to grid
        gx = max(0, min(grid_size * 2, x + grid_size))
        gy = max(0, min(grid_size * 2, y + grid_size))
        grid[gy][gx] = "+"   # trail

    # mark start
    grid[grid_size][grid_size] = "0"

    # mark current position
    cx = max(0, min(grid_size * 2, path[-1][0] + grid_size))
    cy = max(0, min(grid_size * 2, path[-1][1] + grid_size))
    grid[cy][cx] = "*"

    print()
    for row in grid:
        print("  " + " ".join(row))
    print()