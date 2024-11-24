import turtle
import random
import time

# Function to draw a square
def draw_square(t, size, color):
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()

# Function to generate a maze using DFS
def generate_maze(size):
    maze = [[1 for _ in range(size)] for _ in range(size)]
    stack = [(0, 0)]
    maze[0][0] = 0

    while stack:
        x, y = stack[-1]
        neighbors = []

        if x > 1 and maze[y][x - 2] == 1:
            neighbors.append((x - 2, y))
        if x < size - 2 and maze[y][x + 2] == 1:
            neighbors.append((x + 2, y))
        if y > 1 and maze[y - 2][x] == 1:
            neighbors.append((x, y - 2))
        if y < size - 2 and maze[y + 2][x] == 1:
            neighbors.append((x, y + 2))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[(ny + y) // 2][(nx + x) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

# Function to draw the maze
def draw_maze(t, maze, cell_size):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            color = 'white' if maze[y][x] == 0 else 'black'
            t.penup()
            t.goto(x * cell_size - 200, y * cell_size - 200)
            t.pendown()
            draw_square(t, cell_size, color)

    # Highlight start and end points
    t.penup()
    t.goto(-200, -200)
    t.pendown()
    draw_square(t, cell_size, 'yellow')  # Start point

    t.penup()
    t.goto((len(maze[0]) - 1) * cell_size - 200, (len(maze) - 1) * cell_size - 200)
    t.pendown()
    draw_square(t, cell_size, 'green')  # End point

# Function to handle menu selection
def menu_selection(x, y):
    global selected_size
    if -50 < x < 50:
        if 100 < y < 150:
            selected_size = 3
        elif 50 < y < 100:
            selected_size = 5
        elif 0 < y < 50:
            selected_size = 10
        elif -50 < y < 0:
            selected_size = 15
        elif -100 < y < -50:
            selected_size = 20
        turtle.clearscreen()
        screen.bgcolor("lightblue")
        screen.title("Generating Maze...")
        time.sleep(0.5)  # Pause for better user experience

        turtle.speed(0)
        maze = generate_maze(selected_size)
        cell_size = 400 // selected_size
        draw_maze(turtle, maze, cell_size)
        screen.title("Maze Generated!")

# Function to draw the menu with animations
def draw_menu():
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(0, 125)
    turtle.write("Select Maze Size", align="center", font=("Arial", 24, "bold"))

    sizes = ["3x3", "5x5", "10x10", "15x15", "20x20"]
    for i, size in enumerate(sizes):
        turtle.goto(0, 100 - i * 50)
        turtle.write(size, align="center", font=("Arial", 18, "normal"))
        time.sleep(0.2)  # Animation effect

# Setup turtle screen
screen = turtle.Screen()
screen.title("Maze Generator")
screen.setup(width=600, height=600)
screen.bgcolor("red")

# Draw menu with animations
draw_menu()

# Bind click event
screen.onclick(menu_selection)

# Start the turtle main loop
turtle.done()
