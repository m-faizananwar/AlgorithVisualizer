import json
import random
import turtle
from queue import PriorityQueue


class MazeSolver:
    def __init__(self, size_str):
        self.size = int(size_str.split("x")[0])
        self.start_point = [0, 0]  # Top-left corner as start
        self.maze_data = None
        self.filename = "maze_data.json"
        self.generate_and_save_maze_data()

    # Function to generate a maze
    def generate_maze_recursive(self):
        maze = [[1 for _ in range(self.size)] for _ in range(self.size)]
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]  # Directions: right, down, left, up
        last_white_cell = [0, 0]

        def carve_path(x, y):
            nonlocal last_white_cell
            maze[y][x] = 0
            last_white_cell = [x, y]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] == 1:
                    maze[(y + ny) // 2][(x + nx) // 2] = 0
                    carve_path(nx, ny)

        carve_path(0, 0)
        return maze, last_white_cell

    # Function to create maze structure
    def create_maze_structure(self, maze, last_white_cell):
        maze_structure = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                if maze[y][x] == 0:
                    if [x, y] == last_white_cell:
                        row.append("+")  # Goal
                    elif [x, y] == self.start_point:
                        row.append("=")  # Start
                    else:
                        row.append("#")  # Path
                else:
                    row.append("-")  # Block
            maze_structure.append(row)
        return maze_structure

    # Generate random costs and heuristics
    def generate_costs_and_heuristics(self, goal_position):
        costs = [[random.randint(1, 10) for _ in range(self.size)] for _ in range(self.size)]
        heuristics = [
            [abs(goal_position[0] - x) + abs(goal_position[1] - y) for x in range(self.size)]
            for y in range(self.size)
        ]
        return costs, heuristics

    # Save maze data to JSON
    def save_maze_data_to_json(self, maze_structure, costs, heuristics):
        data = {
            "maze": maze_structure,
            "costs": costs,
            "heuristics": heuristics,
        }
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    # Generate and save maze data
    def generate_and_save_maze_data(self):
        maze, last_white_cell = self.generate_maze_recursive()
        maze_structure = self.create_maze_structure(maze, last_white_cell)
        costs, heuristics = self.generate_costs_and_heuristics(last_white_cell)
        self.save_maze_data_to_json(maze_structure, costs, heuristics)
        self.maze_data = {"maze": maze_structure, "costs": costs, "heuristics": heuristics}

    # Render the maze and solve the path
    def render_maze(self, algorithm_name):
        maze = self.maze_data["maze"]
        costs = self.maze_data["costs"]
        heuristics = self.maze_data["heuristics"]
        size = self.size
        cell_size = 400 // size

        turtle.clearscreen()
        screen = turtle.Screen()
        screen.title(f"Maze Solver - {algorithm_name}")
        screen.setup(width=600, height=600)
        screen.bgcolor("white")

        t = turtle.Turtle()
        t.speed(0)
        t.hideturtle()

        def draw_cell(x, y, color):
            t.penup()
            t.goto(x * cell_size - 200, y * cell_size - 200)
            t.pendown()
            draw_square(t, cell_size, color)

        def draw_square(t, size, color):
            t.fillcolor(color)
            t.begin_fill()
            for _ in range(4):
                t.forward(size)
                t.right(90)
            t.end_fill()

        # Draw maze
        for y in range(size):
            for x in range(size):
                if maze[y][x] == "#":
                    draw_cell(x, y, "white")
                elif maze[y][x] == "-":
                    draw_cell(x, y, "black")
                elif maze[y][x] == "+":
                    draw_cell(x, y, "green")
                elif maze[y][x] == "=":
                    draw_cell(x, y, "yellow")

        screen.mainloop()

    # Solve the maze with a selected algorithm
    def solve_maze(self, algorithm_name):
        if algorithm_name == "UCS":
            return self.uniform_cost_search()
        elif algorithm_name == "IDS":
            return self.iterative_deepening_search()
        elif algorithm_name == "GBFS":
            return self.greedy_bfs()
        elif algorithm_name == "A*":
            return self.a_star_search()
        else:
            print("Invalid algorithm selected.")
            return None

    # Uniform Cost Search
    def uniform_cost_search(self):
        start = tuple(self.start_point)
        maze = self.maze_data["maze"]
        costs = self.maze_data["costs"]
        goal = None

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == "+":
                    goal = (x, y)
                    break

        if not goal:
            print("Goal not found in the maze!")
            return None

        visited = set()
        pq = PriorityQueue()
        pq.put((0, start, [start]))  # (cost, current_position, path)

        while not pq.empty():
            cost, current, path = pq.get()

            if current in visited:
                continue

            visited.add(current)

            if current == goal:
                print("UCS Path Found:", path)
                return path

            x, y = current
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] in ["#", "+"] and (nx, ny) not in visited:
                    pq.put((cost + costs[ny][nx], (nx, ny), path + [(nx, ny)]))

        print("No path found using UCS.")
        return None


    # Iterative Deepening Search
    def iterative_deepening_search(self):
        start = tuple(self.start_point)
        maze = self.maze_data["maze"]
        goal = None

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == "+":
                    goal = (x, y)
                    break

        if not goal:
            print("Goal not found in the maze!")
            return None

        def dfs_limited(node, depth, path):
            if depth == 0 and node == goal:
                return path
            if depth > 0:
                x, y = node
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] in ["#", "+"] and (nx, ny) not in path:
                        result = dfs_limited((nx, ny), depth - 1, path + [(nx, ny)])
                        if result:
                            return result
            return None

        for depth in range(self.size * self.size):
            result = dfs_limited(start, depth, [start])
            if result:
                print("IDS Path Found:", result)
                return result

        print("No path found using IDS.")
        return None


        # Greedy BFS
    def greedy_bfs(self):
        start = tuple(self.start_point)
        maze = self.maze_data["maze"]
        heuristics = self.maze_data["heuristics"]
        goal = None

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == "+":
                    goal = (x, y)
                    break

        if not goal:
            print("Goal not found in the maze!")
            return None

        visited = set()
        pq = PriorityQueue()
        pq.put((heuristics[start[1]][start[0]], start, [start]))

        while not pq.empty():
            _, current, path = pq.get()

            if current in visited:
                continue

            visited.add(current)

            if current == goal:
                print("GBFS Path Found:", path)
                return path

            x, y = current
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] in ["#", "+"] and (nx, ny) not in visited:
                    pq.put((heuristics[ny][nx], (nx, ny), path + [(nx, ny)]))

        print("No path found using GBFS.")
        return None


    def a_star_search(self):
        start = tuple(self.start_point)
        maze = self.maze_data["maze"]
        costs = self.maze_data["costs"]
        heuristics = self.maze_data["heuristics"]
        goal = None

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == "+":
                    goal = (x, y)
                    break

        if not goal:
            print("Goal not found in the maze!")
            return None

        visited = set()
        pq = PriorityQueue()
        pq.put((0 + heuristics[start[1]][start[0]], 0, start, [start]))  # (f, g, position, path)

        while not pq.empty():
            f, g, current, path = pq.get()

            if current in visited:
                continue

            visited.add(current)

            if current == goal:
                print("A* Path Found:", path)
                return path

            x, y = current
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] in ["#", "+"] and (nx, ny) not in visited:
                    new_g = g + costs[ny][nx]
                    new_f = new_g + heuristics[ny][nx]
                    pq.put((new_f, new_g, (nx, ny), path + [(nx, ny)]))

        print("No path found using A*.")
        return None

# Example usage
solver = MazeSolver("10x10")
solver.render_maze("UCS")
