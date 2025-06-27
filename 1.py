import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver with 3x3 Lines")
        self.canvas = tk.Canvas(root, width=450, height=450)
        self.canvas.grid(row=0, column=0, columnspan=9)
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.draw_grid_lines()
        self.create_buttons()

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(
                    self.root, width=2, font=('Arial', 18),
                    justify='center', borderwidth=1, relief='ridge'
                )
                entry_window = self.canvas.create_window(
                    col * 50 + 25, row * 50 + 25, window=entry, width=48, height=48
                )
                self.cells[row][col] = entry

    def draw_grid_lines(self):
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            # Horizontal lines
            self.canvas.create_line(0, i * 50, 450, i * 50, width=line_width)
            # Vertical lines
            self.canvas.create_line(i * 50, 0, i * 50, 450, width=line_width)

    def create_buttons(self):
        solve_btn = tk.Button(self.root, text="Solve", command=self.solve_board, bg='lightgreen')
        solve_btn.grid(row=10, column=0, columnspan=3, sticky='we')

        check_btn = tk.Button(self.root, text="Check Mistakes", command=self.check_mistakes, bg='lightblue')
        check_btn.grid(row=10, column=3, columnspan=3, sticky='we')

        clear_btn = tk.Button(self.root, text="Clear", command=self.clear_board, bg='lightcoral')
        clear_btn.grid(row=10, column=6, columnspan=3, sticky='we')

    def get_board(self):
        for row in range(9):
            for col in range(9):
                val = self.cells[row][col].get()
                self.board[row][col] = int(val) if val.isdigit() else 0

    def fill_board(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].delete(0, tk.END)
                if self.board[row][col] != 0:
                    self.cells[row][col].insert(0, str(self.board[row][col]))

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[box_row + i][box_col + j] == num:
                    return False
        return True

    def solve(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def solve_board(self):
        self.get_board()
        if self.solve(self.board):
            self.fill_board()
        else:
            messagebox.showerror("No Solution", "The Sudoku puzzle has no solution.")

    def check_mistakes(self):
        self.get_board()
        for row in range(9):
            for col in range(9):
                val = self.board[row][col]
                if val != 0:
                    self.board[row][col] = 0
                    if not self.is_valid(self.board, row, col, val):
                        self.cells[row][col].config(bg='red')
                    else:
                        self.cells[row][col].config(bg='white')
                    self.board[row][col] = val
                else:
                    self.cells[row][col].config(bg='white')

    def clear_board(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].delete(0, tk.END)
                self.cells[row][col].config(bg='white')
        self.board = [[0 for _ in range(9)] for _ in range(9)]

if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

