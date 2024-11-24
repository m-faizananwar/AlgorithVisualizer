import json
import random
import turtle
from queue import PriorityQueue
import time
import sys

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

        # Solve the maze and draw the solution path
        path, metrics = self.solve_maze(algorithm_name)
        if path:
            for (x, y) in path:
                draw_cell(x, y, "blue")

        print(f"Algorithm: {algorithm_name}")
        print(f"Cost: {metrics['cost']}")
        print(f"Nodes Explored: {metrics['nodes_explored']}")
        print(f"Number of Nodes Expanded: {metrics['nodes_expanded']}")
        print(f"Time Taken: {metrics['time_taken']} seconds")

        button = turtle.Turtle()
        button.penup()
        button.goto(0, 250)
        button.shape("square")
        button.shapesize(stretch_wid=1, stretch_len=5)
        button.fillcolor("lightblue")

        # Create a separate turtle for the button text
        text_turtle = turtle.Turtle()
        text_turtle.penup()
        text_turtle.hideturtle()
        text_turtle.goto(0, 250)
        text_turtle.write("Select Algorithm", align="center", font=("Arial", 18, "bold"))

        # Make the button clickable
        button.onclick(lambda x, y: self.select_algorithm())

        screen.mainloop()

    # Solve the maze with a selected algorithm
    def solve_maze(self, algorithm_name):
        start_time = time.time()
        if algorithm_name == "UCS":
            path, metrics = self.uniform_cost_search()
        elif algorithm_name == "IDS":
            path, metrics = self.iterative_deepening_search()
        elif algorithm_name == "GBFS":
            path, metrics = self.greedy_bfs()
        elif algorithm_name == "A*":
            path, metrics = self.a_star_search()
        else:
            print("Invalid algorithm selected.")
            return None, None
        end_time = time.time()
        metrics['time_taken'] = end_time - start_time
        return path, metrics

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
            return None, {}

        visited = set()
        pq = PriorityQueue()
        pq.put((0, start, [start]))  # (cost, current_position, path)
        nodes_explored = 0
        nodes_expanded = 0

        while not pq.empty():
            cost, current, path = pq.get()
            nodes_explored += 1

            if current in visited:
                continue

            visited.add(current)
            nodes_expanded += 1

            if current == goal:
                return path, {"cost": cost, "nodes_explored": nodes_explored, "nodes_expanded": nodes_expanded}

            x, y = current
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] in ["#", "+"] and (nx, ny) not in visited:
                    pq.put((cost + costs[ny][nx], (nx, ny), path + [(nx, ny)]))

        print("No path found using UCS.")
        return None, {"cost": 0, "nodes_explored": nodes_explored, "nodes_expanded": nodes_expanded}

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
            return None, {}

        nodes_explored = 0
        nodes_expanded = 0

        def dfs_limited(node, depth, path):
            nonlocal nodes_explored, nodes_expanded
            nodes_explored += 1
            if depth == 0 and node == goal:
                return path
            if depth > 0:
                x, y = node
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] in ["#", "+"] and (nx, ny) not in path:
                        nodes_expanded += 1
                        result = dfs_limited((nx, ny), depth - 1, path + [(nx, ny)])
                        if result:
                            return result
            return None

        for depth in range(self.size * self.size):
            result = dfs_limited(start, depth, [start])
            if result:
                return result, {"cost": depth, "nodes_explored": nodes_explored, "nodes_expanded": nodes_expanded}

        print("No path found using IDS.")
        return None, {"cost": 0, "nodes_explored": nodes_explored, "nodes_expanded": nodes_expanded}

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
            return None, {}

        visited = set()
        pq = PriorityQueue()
        pq.put((heuristics[start[1]][start[0]], start, [start]))
        nodes_explored = 0
        nodes_expanded = 0

        while not pq.empty():
            _, current, path = pq.get()
            nodes_explored += 1

            if current in visited:
                continue

            visited.add(current)
            nodes_expanded += 1

            if current == goal:
                return path, {"cost": len(path), "nodes_explored": nodes_explored, "nodes_expanded": nodes_expanded}

            x, y = current
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] in ["#", "+"] and (nx, ny) not in visited:
                    pq.put((heuristics[ny][nx], (nx, ny), path + [(nx, ny)]))

        print("No path found using GBFS.")
        return None, {"cost": 0, "nodes_explored": nodes_explored, "nodes_expanded": nodes_expanded}

    # A* Search
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
            return None, {}

        visited = set()
        pq = PriorityQueue()
        pq.put((0 + heuristics[start[1]][start[0]], 0, start, [start]))  # (f, g, position, path)
        nodes_explored = 0
        nodes_expanded = 0

        while not pq.empty():
            f, g, current, path = pq.get()
            nodes_explored += 1

            if current in visited:
                continue

            visited.add(current)
            nodes_expanded += 1

            if current == goal:
                return path, {"cost": g, "nodes_explored": nodes_explored, "nodes_expanded": nodes_expanded}

            x, y = current
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and maze[ny][nx] in ["#", "+"] and (nx, ny) not in visited:
                    new_g = g + costs[ny][nx]
                    new_f = new_g + heuristics[ny][nx]
                    pq.put((new_f, new_g, (nx, ny), path + [(nx, ny)]))

        print("No path found using A*.")
        return None, {"cost": 0, "nodes_explored": nodes_explored, "nodes_expanded": nodes_expanded}

    def select_algorithm(self):
        valid_algorithms = ["UCS", "IDS", "GBFS", "A*"]
        algorithm = turtle.textinput("Select Algorithm", "Enter algorithm (UCS, IDS, GBFS, A*):")
        if algorithm is None:
            print("Program closed by user.")
            sys.exit()
        elif algorithm:
            algorithm = algorithm.strip().upper()
            if algorithm in valid_algorithms:
                self.render_maze(algorithm)
            else:
                print("Invalid algorithm selected. Please enter one of the following: UCS, IDS, GBFS, A*")
                self.select_algorithm()
        else:
            print("No algorithm entered. Please enter one of the following: UCS, IDS, GBFS, A*")
            self.select_algorithm()

def main():
    solver = MazeSolver("15x15")
    solver.select_algorithm()

if __name__ == "__main__":
    main()