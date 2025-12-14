from __future__ import annotations

from typing import List, Optional, Tuple

Grid = List[List[int]]  # 9 rows x 9 cols; 0 = empty

DIGITS = set(range(1, 10))


def box_index(row: int, col: int) -> int:
    return (row // 3) * 3 + (col // 3)


def build_constraints(grid: Grid):
    """
    Build row/col/box sets from the current grid.
    Raises ValueError if the starting grid is invalid (duplicate in row/col/box).
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            if v not in DIGITS:
                raise ValueError(f"Invalid value {v} at ({r},{c})")

            b = box_index(r, c)
            if v in rows[r] or v in cols[c] or v in boxes[b]:
                raise ValueError(f"Invalid grid: duplicate {v} at ({r},{c})")

            rows[r].add(v)
            cols[c].add(v)
            boxes[b].add(v)

    return rows, cols, boxes


def is_valid(grid: Grid, row: int, col: int, value: int) -> bool:
    """Check if placing `value` at (row, col) keeps Sudoku rules valid."""
    if not (1 <= value <= 9):
        return False

    # Row check
    for c in range(9):
        if grid[row][c] == value:
            return False

    # Column check
    for r in range(9):
        if grid[r][col] == value:
            return False

    # 3x3 box check
    box_r0 = (row // 3) * 3
    box_c0 = (col // 3) * 3
    for r in range(box_r0, box_r0 + 3):
        for c in range(box_c0, box_c0 + 3):
            if grid[r][c] == value:
                return False

    return True

def candidates_fast(rows, cols, boxes, row: int, col: int) -> list[int]:
    """Valid candidates using constraint sets (fast)."""
    b = box_index(row, col)
    possible = DIGITS - rows[row] - cols[col] - boxes[b]
    return list(possible)


def find_mrv_cell_fast(grid: Grid, rows, cols, boxes):
    """
    MRV: pick empty cell with fewest candidates.
    Returns ((row,col), candidates) or (None, []) if solved.
    If a cell has 0 candidates => dead end.
    """
    best_cell = None
    best_cands: list[int] = []
    best_len = 10

    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cands = candidates_fast(rows, cols, boxes, r, c)
                l = len(cands)

                if l == 0:
                    return (r, c), []  # dead end now

                if l < best_len:
                    best_len = l
                    best_cell = (r, c)
                    best_cands = cands
                    if best_len == 1:
                        return best_cell, best_cands

    return best_cell, best_cands


def solve(grid: Grid, rows, cols, boxes) -> bool:
    cell, cands = find_mrv_cell_fast(grid, rows, cols, boxes)
    if cell is None:
        return True  # solved

    row, col = cell
    b = box_index(row, col)

    for value in cands:
        # place
        grid[row][col] = value
        rows[row].add(value)
        cols[col].add(value)
        boxes[b].add(value)

        if solve(grid, rows, cols, boxes):
            return True

        # backtrack
        grid[row][col] = 0
        rows[row].remove(value)
        cols[col].remove(value)
        boxes[b].remove(value)

    return False


def pretty_print(grid: Grid) -> None:
    """Print the grid in a readable 9x9 format."""
    for r in range(9):
        if r != 0 and r % 3 == 0:
            print("-" * 21)
        row_parts = []
        for c in range(9):
            if c != 0 and c % 3 == 0:
                row_parts.append("|")
            v = grid[r][c]
            row_parts.append(str(v) if v != 0 else ".")
        print(" ".join(row_parts))


def solve_grid(grid: Grid) -> bool:
    """
    Validates and solves the given grid in-place.
    Returns True if solved, False if no solution exists.
    Raises ValueError if the starting grid is invalid.
    """
    rows, cols, boxes = build_constraints(grid)
    return solve(grid, rows, cols, boxes)


if __name__ == "__main__":
    # Hard-coded example grid (0 = empty)
    grid: Grid = [
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

    rows, cols, boxes = build_constraints(grid)

    print("Original:")
    pretty_print(grid)

    if solve(grid, rows, cols, boxes):
        print("\nSolved:")
        pretty_print(grid)
    else:
        print("\nNo solution found.")
