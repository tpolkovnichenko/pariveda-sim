# The Knot — A Probability & Simulation Engine

Terminal-based simulation engine. MIS 221 Pariveda Competition submission.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Simulations

| # | Module | Core Concept |
|---|--------|-------------|
| 1 | Pi Estimation | Monte Carlo, Law of Large Numbers |
| 2 | Gambler's Ruin + Kelly Criterion | Ruin probability, bankroll optimization |
| 3 | Polya's Random Walk | Stochastic processes, Polya's Theorem |
| 4 | Markov Chains + Dark DNA Solver | Stationary distributions, matrix iteration |
| 5 | CFR: Squid Game Marbles | Counterfactual Regret Minimization, Nash Equilibrium |

## Algorithmic Escalation

Each module builds on the last. The project peaks in CFR -
the same class of algorithm used by Libratus, the AI that defeated
professional poker players in heads-up no-limit Texas Hold'em in 2017.

## Output

All runs saved automatically to `data/results.json`.

## Requirements

Python 3.x, numpy