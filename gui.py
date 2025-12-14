import tkinter as tk
from tkinter import messagebox

from solver import solve_grid, Grid  # uses your solver.py


CELL_SIZE = 50
PAD = 8


class SudokuGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sudoku Solver")

        self.canvas = tk.Canvas(
            root,
            width=9 * CELL_SIZE + 2 * PAD,
            height=9 * CELL_SIZE + 2 * PAD,
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.btn_solve = tk.Button(root, text="Solve", command=self.on_solve, width=12)
        self.btn_solve.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 10))

        self.btn_clear = tk.Button(root, text="Clear", command=self.on_clear, width=12)
        self.btn_clear.grid(row=1, column=1, sticky="e", padx=10, pady=(0, 10))

        # Internal grid: 9x9 of ints (0 empty)
        self.grid: Grid = [[0 for _ in range(9)] for _ in range(9)]

        # Selected cell (row, col)
        self.sel_r = 0
        self.sel_c = 0

        # Bindings
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Key>", self.on_key)

        self.draw()

    def draw(self) -> None:
        self.canvas.delete("all")

        # Background
        self.canvas.create_rectangle(
            PAD, PAD,
            PAD + 9 * CELL_SIZE, PAD + 9 * CELL_SIZE,
            outline=""
        )

        # Highlight selected cell
        x0, y0, x1, y1 = self.cell_bbox(self.sel_r, self.sel_c)
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="", fill="#dbeafe")  # light highlight

        # Grid lines (thick for 3x3)
        for i in range(10):
            w = 3 if i % 3 == 0 else 1
            # vertical
            x = PAD + i * CELL_SIZE
            self.canvas.create_line(x, PAD, x, PAD + 9 * CELL_SIZE, width=w)
            # horizontal
            y = PAD + i * CELL_SIZE
            self.canvas.create_line(PAD, y, PAD + 9 * CELL_SIZE, y, width=w)

        # Numbers
        for r in range(9):
            for c in range(9):
                v = self.grid[r][c]
                if v != 0:
                    cx = PAD + c * CELL_SIZE + CELL_SIZE / 2
                    cy = PAD + r * CELL_SIZE + CELL_SIZE / 2
                    self.canvas.create_text(cx, cy, text=str(v), font=("Segoe UI", 18))

    def cell_bbox(self, r: int, c: int):
        x0 = PAD + c * CELL_SIZE
        y0 = PAD + r * CELL_SIZE
        x1 = x0 + CELL_SIZE
        y1 = y0 + CELL_SIZE
        return x0, y0, x1, y1

    def on_click(self, event: tk.Event) -> None:
        x, y = event.x, event.y
        if not (PAD <= x <= PAD + 9 * CELL_SIZE and PAD <= y <= PAD + 9 * CELL_SIZE):
            return
        c = int((x - PAD) // CELL_SIZE)
        r = int((y - PAD) // CELL_SIZE)
        self.sel_r, self.sel_c = r, c
        self.draw()

    def on_key(self, event: tk.Event) -> None:
        key = event.keysym

        # Arrow navigation
        if key == "Left":
            self.sel_c = (self.sel_c - 1) % 9
            self.draw()
            return
        if key == "Right":
            self.sel_c = (self.sel_c + 1) % 9
            self.draw()
            return
        if key == "Up":
            self.sel_r = (self.sel_r - 1) % 9
            self.draw()
            return
        if key == "Down":
            self.sel_r = (self.sel_r + 1) % 9
            self.draw()
            return

        # Clear cell
        if key in ("BackSpace", "Delete"):
            self.grid[self.sel_r][self.sel_c] = 0
            self.draw()
            return

        # Digit input
        ch = event.char
        if ch in "123456789":
            self.grid[self.sel_r][self.sel_c] = int(ch)
            self.draw()
            return
        if ch == "0":
            self.grid[self.sel_r][self.sel_c] = 0
            self.draw()
            return

    def on_clear(self) -> None:
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.sel_r, self.sel_c = 0, 0
        self.draw()

    def on_solve(self) -> None:
        # Work on a copy so we can show error without partially changing UI grid
        grid_copy: Grid = [row[:] for row in self.grid]

        try:
            solved = solve_grid(grid_copy)
        except ValueError as e:
            messagebox.showerror("Invalid Sudoku", str(e))
            return

        if not solved:
            messagebox.showinfo("No solution", "No solution exists for this grid.")
            return

        self.grid = grid_copy
        self.draw()
        messagebox.showinfo("Solved", "Sudoku solved successfully!")


def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
