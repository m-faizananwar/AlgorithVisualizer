import tkinter as tk
import time

def on_button_hover(event):
    """Handles hover effects."""
    event.widget.config(bg="lightblue", fg="black")

def on_button_leave(event):
    """Reverts hover effects."""
    event.widget.config(bg="midnightblue", fg="white")

def on_button_click(size):
    """Handles button click events."""
    for widget in root.winfo_children():
        widget.destroy()
    label = tk.Label(root, text=f"You selected: {size}", font=("Arial", 24, "bold"), fg="white", bg="midnightblue")
    label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

def show_menu():
    """Draws the main menu."""
    for widget in root.winfo_children():
        widget.destroy()
    
    # Title
    title = tk.Label(root, text="Select Maze Size", font=("Arial", 28, "bold"), fg="cyan", bg="midnightblue")
    title.grid(row=0, column=0, padx=20, pady=20)

    # Menu Options
    sizes = ["3x3", "5x5", "10x10", "15x15", "20x20", "25x25", "30x30"]
    for i, size in enumerate(sizes):
        button = tk.Button(
            root,
            text=size,
            font=("Arial", 18),
            bg="midnightblue",
            fg="white",
            activebackground="blue",
            activeforeground="white",
            relief="raised",
            bd=3
        )
        button.grid(row=i + 1, column=0, padx=20, pady=10, sticky="ew")

        # Add hover effects
        button.bind("<Enter>", on_button_hover)
        button.bind("<Leave>", on_button_leave)

        # Add click event
        button.config(command=lambda size=size: on_button_click(size))

def show_welcome_screen():
    """Displays the welcome screen with animation."""
    welcome_label = tk.Label(root, text="Welcome to Algorithm Visualizer", font=("Arial", 32, "bold"), fg="white", bg="black")
    welcome_label.pack(pady=50)

    # Create an animated background effect
    canvas = tk.Canvas(root, width=400, height=400, bg="black")
    canvas.pack()

    colors = ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33A1"]
    
    def animate_background():
        for color in colors:
            canvas.config(bg=color)
            root.update()
            time.sleep(0.5)  # Change the speed of the animation here

    root.after(1000, animate_background)  # Start the animation after 1 second
    root.after(3000, show_menu)  # Show the menu after 3 seconds

# Set up the root window
root = tk.Tk()
root.title("Maze Size Selector")
root.configure(bg="black")
root.minsize(400, 400)

# Start with the welcome screen
show_welcome_screen()

# Run the main loop
root.mainloop()