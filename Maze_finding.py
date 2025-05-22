import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue
import random

ROWS, COLS = 20, 20
CELL_SIZE = 30

COLOR_EMPTY = "white"
COLOR_WALL = "black"
COLOR_START = "green"
COLOR_END = "red"
PATH_COLORS = ["yellow", "orange", "blue"]  # Colors for 1st, 2nd, 3rd paths

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_wall = False
        self.is_start = False
        self.is_end = False

    def __lt__(self, other):
        return False

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze A* Pathfinding with Multiple Paths")

        self.grid = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]
        self.start = None
        self.end = None
        self.paths = []

        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.toggle_wall)
        self.canvas.bind("<Button-3>", self.set_start_or_end)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack()

        self.find_paths_btn = tk.Button(self.btn_frame, text="Find Paths", command=self.find_all_paths)
        self.find_paths_btn.grid(row=0, column=0)

        self.reset_btn = tk.Button(self.btn_frame, text="Reset", command=self.reset)
        self.reset_btn.grid(row=0, column=1)

        self.easy_btn = tk.Button(self.btn_frame, text="Easy Maze", command=lambda: self.generate_maze('easy'))
        self.easy_btn.grid(row=0, column=2)

        self.complex_btn = tk.Button(self.btn_frame, text="Complicated Maze", command=lambda: self.generate_maze('complicated'))
        self.complex_btn.grid(row=0, column=4)

        self.path_var = tk.StringVar(value="Show Path")
        self.path_menu = tk.OptionMenu(self.btn_frame, self.path_var, "1st", "2nd", "3rd", command=self.show_path)
        self.path_menu.grid(row=0, column=5)

        self.path_info_label = tk.Label(self.btn_frame, text="", justify="left", anchor="w")
        self.path_info_label.grid(row=0, column=6, padx=20)

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                cell = self.grid[r][c]
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                if cell.is_start:
                    color = COLOR_START
                elif cell.is_end:
                    color = COLOR_END
                elif cell.is_wall:
                    color = COLOR_WALL
                else:
                    color = COLOR_EMPTY

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def toggle_wall(self, event):
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS:
            cell = self.grid[r][c]
            if not cell.is_start and not cell.is_end:
                cell.is_wall = not cell.is_wall
                self.draw_grid()

    def set_start_or_end(self, event):
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS:
            cell = self.grid[r][c]
            if cell.is_wall:
                return
            if self.start is None:
                cell.is_start = True
                self.start = cell
            elif self.end is None and not cell.is_start:
                cell.is_end = True
                self.end = cell
            else:
                if cell.is_start:
                    cell.is_start = False
                    self.start = None
                if cell.is_end:
                    cell.is_end = False
                    self.end = None
            self.draw_grid()

    def heuristic(self, a, b):
        return abs(a.row - b.row) + abs(a.col - b.col)

    def neighbors(self, cell):
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        result = []
        for dr, dc in directions:
            nr, nc = cell.row + dr, cell.col + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                neighbor = self.grid[nr][nc]
                if not neighbor.is_wall:
                    result.append(neighbor)
        return result

    def find_path(self):
        if not self.start or not self.end:
            return None

        open_set = PriorityQueue()
        open_set.put((0, self.start))
        came_from = {}

        g_score = {cell: float('inf') for row in self.grid for cell in row}
        g_score[self.start] = 0

        f_score = {cell: float('inf') for row in self.grid for cell in row}
        f_score[self.start] = self.heuristic(self.start, self.end)

        open_set_hash = {self.start}

        while not open_set.empty():
            current = open_set.get()[1]
            open_set_hash.remove(current)

            if current == self.end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self.neighbors(current):
                temp_g = g_score[current] + 1
                if temp_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g
                    f_score[neighbor] = temp_g + self.heuristic(neighbor, self.end)
                    if neighbor not in open_set_hash:
                        open_set.put((f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)

        return None

    def find_all_paths(self):
        self.paths = []
        backup_grid = [[cell.is_wall for cell in row] for row in self.grid]

        for _ in range(3):
            path = self.find_path()
            if not path:
                break
            self.paths.append(path)
            for cell in path:
                if not cell.is_start and not cell.is_end:
                    cell.is_wall = True

        # Restore walls
        for r in range(ROWS):
            for c in range(COLS):
                self.grid[r][c].is_wall = backup_grid[r][c]

        # Re-block only used paths
        for path in self.paths:
            for cell in path:
                if not cell.is_start and not cell.is_end:
                    cell.is_wall = True

        self.draw_grid()

        # Draw all paths with their colors simultaneously
        for i, path in enumerate(self.paths):
            for cell in path:
                if not cell.is_start and not cell.is_end:
                    x1 = cell.col * CELL_SIZE
                    y1 = cell.row * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=PATH_COLORS[i], outline="gray")

        # Update path info label
        info = f"{len(self.paths)} path(s) found.\n"
        for i, path in enumerate(self.paths):
            info += f"{['1st','2nd','3rd'][i]} path: {len(path)} blocks\n"
        self.path_info_label.config(text=info.strip())

    def show_path(self, value):
        index = {"1st": 0, "2nd": 1, "3rd": 2}.get(value)
        if index is None or index >= len(self.paths):
            return

        self.draw_grid()

        # Only draw the selected path to highlight it clearly
        for cell in self.paths[index]:
            if not cell.is_start and not cell.is_end:
                x1 = cell.col * CELL_SIZE
                y1 = cell.row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=PATH_COLORS[index], outline="gray")

        # Update path info label with block count
        extra_info = f"\n{value} shortest path has {len(self.paths[index])} blocks."
        self.path_info_label.config(
            text=self.path_info_label.cget("text").split('\n')[0] + '\n' + '\n'.join(
                [f"{['1st','2nd','3rd'][i]} path: {len(self.paths[i])} blocks" for i in range(len(self.paths))]
            ) + extra_info
        )

    def reset(self):
        self.paths.clear()
        for row in self.grid:
            for cell in row:
                cell.is_wall = False
                cell.is_start = False
                cell.is_end = False
        self.start = None
        self.end = None
        self.path_info_label.config(text="")
        self.draw_grid()

    def generate_maze(self, difficulty):
        self.reset()
        if difficulty == 'easy':
            for _ in range(ROWS * COLS // 6):
                r = random.randint(0, ROWS - 1)
                c = random.randint(0, COLS - 1)
                self.grid[r][c].is_wall = True
        else:
            self.generate_perfect_maze()
        self.draw_grid()

    def generate_perfect_maze(self):
        for row in self.grid:
            for cell in row:
                cell.is_wall = True

        def carve_passages(r, c):
            dirs = [(2,0), (-2,0), (0,2), (0,-2)]
            random.shuffle(dirs)
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and self.grid[nr][nc].is_wall:
                    self.grid[nr][nc].is_wall = False
                    self.grid[r + dr//2][c + dc//2].is_wall = False
                    carve_passages(nr, nc)

        start_r = random.randrange(0, ROWS, 2)
        start_c = random.randrange(0, COLS, 2)
        self.grid[start_r][start_c].is_wall = False
        carve_passages(start_r, start_c)

    def generate_hard_maze(self):
        self.generate_perfect_maze()
        extra_walls = ROWS * COLS // 8
        added = 0
        while added < extra_walls:
            r = random.randint(1, ROWS - 2)
            c = random.randint(1, COLS - 2)
            cell = self.grid[r][c]
            if not cell.is_wall and not cell.is_start and not cell.is_end:
                if sum(1 for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]
                       if self.grid[r+dr][c+dc].is_wall) < 3:
                    cell.is_wall = True
                    added += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
