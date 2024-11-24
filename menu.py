import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from generateMaze import MazeSolver

def on_button_click(size):
    """Handles button click events."""
    for widget in root.winfo_children():
        widget.destroy()
    root.destroy()
    solver = MazeSolver(size)
    solver.select_algorithm()

def draw_menu():
    """Draws the main menu."""
    global root
    for widget in root.winfo_children():
        widget.destroy()

    # Title
    title = ttk.Label(root, text="Select Maze Size", font=("Helvetica", 24, "bold"), bootstyle="primary",foreground='white' , background='#2F6C60')
    title.pack(pady=30, anchor='center')  # Center the title

    # Menu Options
    sizes = ["3x3", "5x5", "10x10", "15x15", "20x20", "25x25", "30x30"]
    for size in sizes:
        button = ttk.Button(
            root,
            text=size,
            command=lambda size=size: on_button_click(size),
            bootstyle="info-outline",
            width=15,
            style="Custom.TButton"
        )
        button.pack(pady=10)

# Initialize the app
root = ttk.Window(themename="darkly")  # Use a modern theme
root.title("Maze Size Selector")
root.geometry("1000x600")
root.resizable(False, False)
root.configure(bg='#2F6C60')

# Create a custom style for buttons
style = ttk.Style()
style.configure("Custom.TButton", borderwidth=1, relief="solid", bordercolor="black", focusthickness=3, focuscolor="none")
style.map("Custom.TButton", background=[("active", "black")], foreground=[("active", "white")])

draw_menu()

    # Run the application
root.mainloop()

if __name__ == "__main__":
    # Draw the main menu
    draw_menu()

    # Run the application
    root.mainloop()