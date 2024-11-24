import turtle
import random
import tkinter as tk
from tkinter import simpledialog
import heapq
import json
import os

class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = self.generate_maze_bfs(size)
        self.cell_size = 400 // size
        self.start = (0, 0)
        self.end = (size - 1, size - 1)
        self.screen = turtle.Screen()
        self.t = turtle.Turtle()
        self.data_file = "maze_data.json"

    def draw_square(self, x, y, color):
        self.t.penup()
        self.t.goto(x * self.cell_size - 200, y * self.cell_size - 200)
        self.t.pendown()
        self.t.fillcolor(color)
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(self.cell_size)
            self.t.right(90)
        self.t.end_fill()

    def draw_maze(self):
        self.t.speed(0)
        self.t.hideturtle()
        self.screen.tracer(0)
        for y in range(self.size):
            for x in range(self.size):
                color = 'white' if self.maze[y][x] == 0 else 'black'
                self.draw_square(x, y, color)
        self.draw_square(*self.start, 'yellow')
        self.draw_square(*self.end, 'green')
        self.screen.tracer(1)

    def generate_maze_bfs(self, size):
        maze = [[1 for _ in range(size)] for _ in range(size)]
        queue = [(0, 0)]
        maze[0][0] = 0
        while queue:
            x, y = queue.pop(0)
            neighbors = []
            if x > 1 and maze[y][x - 2] == 1:
                neighbors.append((x - 2, y))
            if x < size - 2 and maze[y][x + 2] == 1:
                neighbors.append((x + 2, y))
            if y > 1 and maze[y - 2][x] == 1:
                neighbors.append((x, y - 2))
            if y < size - 2 and maze[y + 2][x] == 1:
                neighbors.append((x, y + 2))
            random.shuffle(neighbors)
            for nx, ny in neighbors:
                if maze[ny][nx] == 1:
                    maze[ny][nx] = 0
                    maze[(ny + y) // 2][(nx + x) // 2] = 0
                    queue.append((nx, ny))
        return maze

    def neighbors(self, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.maze[ny][nx] == 0:
                yield nx, ny

    def heuristic(self, pos):
        x, y = pos
        ex, ey = self.end
        return abs(x - ex) + abs(y - ey)

    def save_maze_data(self):
        data = {
            "maze": self.maze,
            "size": self.size,
            "start": self.start,
            "end": self.end,
            "heuristics": {f"{x},{y}": self.heuristic((x, y)) for y in range(self.size) for x in range(self.size)}
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f)

    def load_maze_data(self):
        if not os.path.exists(self.data_file):
            raise FileNotFoundError("Maze data file not found!")
        with open(self.data_file, "r") as f:
            data = json.load(f)
            self.maze = data["maze"]
            self.size = data["size"]
            self.start = tuple(data["start"])
            self.end = tuple(data["end"])
            return data["heuristics"]

    def solve_and_draw(self, algorithm):
        heuristics = self.load_maze_data()
        if algorithm == "UCS":
            path = self.uniform_cost_search()
        elif algorithm == "IDS":
            path = self.iterative_deepening_search()
        elif algorithm == "GBFS":
            path = self.greedy_bfs(heuristics)
        elif algorithm == "A*":
            path = self.a_star_search(heuristics)
        else:
            return
        for x, y in path:
            self.draw_square(x, y, 'blue')

    def uniform_cost_search(self):
        visited = set()
        heap = [(0, self.start, [])]
        while heap:
            cost, (x, y), path = heapq.heappop(heap)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            path = path + [(x, y)]
            if (x, y) == self.end:
                return path
            for nx, ny in self.neighbors(x, y):
                heapq.heappush(heap, (cost + 1, (nx, ny), path))

    def iterative_deepening_search(self):
        def dfs(x, y, depth, path):
            if depth < 0 or (x, y) in path:
                return None
            path = path + [(x, y)]
            if (x, y) == self.end:
                return path
            for nx, ny in self.neighbors(x, y):
                result = dfs(nx, ny, depth - 1, path)
                if result:
                    return result
            return None

        for depth in range(self.size * self.size):
            result = dfs(self.start[0], self.start[1], depth, [])
            if result:
                return result

    def greedy_bfs(self, heuristics):
        visited = set()
        heap = [(heuristics[f"{x},{y}"], (x, y), []) for x, y in [self.start]]
        while heap:
            _, (x, y), path = heapq.heappop(heap)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            path = path + [(x, y)]
            if (x, y) == self.end:
                return path
            for nx, ny in self.neighbors(x, y):
                heapq.heappush(heap, (heuristics[f"{nx},{ny}"], (nx, ny), path))

    def a_star_search(self, heuristics):
        visited = set()
        heap = [(heuristics[f"{x},{y}"], 0, (x, y), []) for x, y in [self.start]]
        while heap:
            f, g, (x, y), path = heapq.heappop(heap)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            path = path + [(x, y)]
            if (x, y) == self.end:
                return path
            for nx, ny in self.neighbors(x, y):
                new_g = g + 1
                heapq.heappush(heap, (new_g + heuristics[f"{nx},{ny}"], new_g, (nx, ny), path))

    def close(self):
        self.screen.bye()

    def run(self):
        self.screen.title("Maze Solver")
        self.screen.setup(width=600, height=600)
        self.draw_maze()
        self.save_maze_data()

        root = tk.Tk()
        root.title("Maze Solver")
        root.geometry("200x300")

        tk.Button(root, text="Uniform Cost Search", command=lambda: self.solve_and_draw("UCS")).pack(fill=tk.BOTH)
        tk.Button(root, text="Iterative Deepening Search", command=lambda: self.solve_and_draw("IDS")).pack(fill=tk.BOTH)
        tk.Button(root, text="Greedy BFS", command=lambda: self.solve_and_draw("GBFS")).pack(fill=tk.BOTH)
        tk.Button(root, text="A* Search", command=lambda: self.solve_and_draw("A*")).pack(fill=tk.BOTH)
        tk.Button(root, text="Close", command=lambda: [root.destroy(), self.close()]).pack(fill=tk.BOTH)

        root.mainloop()


# Run the Maze Solver
size = int(simpledialog.askstring("Input", "Enter maze size (e.g., 20):", parent=tk.Tk()))
maze = Maze(size)
maze.run()
