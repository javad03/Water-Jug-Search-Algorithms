# Water Jug Problem Solver

A Python implementation of the Water Jug Problem using different search algorithms from Artificial Intelligence.

## Problem Description

Given two water jugs:

- One 4-liter jug
- One 3-liter jug

The goal is to obtain exactly 2 liters of water in the 4-liter jug.

The problem is modeled as a state space search problem.

---

## Implemented Algorithms

This project implements and compares:

### Uninformed Search Algorithms

- Breadth First Search (BFS)
- Depth First Search (DFS)
- Iterative Deepening Search (IDS)


### Informed Search Algorithms

- A* Search
- Recursive Best First Search (RBFS)


---

## Project Structure

```
Water-Jug-Search-Algorithms

│
├── main.py
├── state.py
│
└── algorithms
    ├── bfs.py
    ├── dfs.py
    ├── ids.py
    ├── astar.py
    └── rbfs.py

```

---

## Concepts Used

- State Space Representation
- Graph Search
- Heuristic Function
- Path Reconstruction
- Complexity Comparison
- Optimal Search

---

## Running The Project

Run:

```bash
python main.py
```

---

## Example Output

The program executes all algorithms and displays:

- Solution path
- Path length
- Number of expanded nodes
- Execution time

---

## Technologies

- Python 3

---

## Author

Javad Salehi