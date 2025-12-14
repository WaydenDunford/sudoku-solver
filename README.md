# Sudoku Solver 🧩

A Python-based Sudoku solver using backtracking and constraint satisfaction techniques.
The project focuses on clean algorithmic design, performance optimizations, and future extensibility.

---

## ✨ Features

- Solves standard 9×9 Sudoku puzzles
- Uses **backtracking** with **MRV (Minimum Remaining Values)** heuristic
- Fast constraint checking using row/column/box sets
- Clean separation between solver logic and I/O
- Designed for future extensions (GUI, image input, file input)

---

## 🧠 How It Works (High Level)

The solver treats Sudoku as a **Constraint Satisfaction Problem (CSP)**:

- Each cell is a variable
- Possible values are 1–9
- Constraints:
  - No duplicates in rows
  - No duplicates in columns
  - No duplicates in 3×3 boxes

Optimizations used:
- **MRV heuristic** to choose the next cell with the fewest valid options
- **Set-based constraints** for O(1) validity checks
- Recursive backtracking to guarantee a correct solution

---

## ▶️ How to Run

### 1. Activate the virtual environment

```bash
venv\Scripts\activate
```


### 2. Run the solver

```bash
python solver.py
```


### 3. Example Sudoku grid

- Numbers 1–9 are fixed values
- 0 represents an empty cell

```python
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]
```
