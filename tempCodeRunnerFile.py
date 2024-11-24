import tkinter as tk

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

def draw_menu():
    """Draws the main menu."""
    global root
    root = tk.Tk()
    root.title("Maze Size Selector")
    root.configure(bg="black")

    # Set minimum size
    root.minsize(400, 400)

    # Title
    title = tk.Label(root, text="Select Maze Size", font=("Arial", 28, "bold"), fg="cyan", bg="midnightblue")
    title.grid(row=0, column=0, padx=20, pady=20)

    # Configure grid
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

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

    root.mainloop()

# Run the menu
draw_menu()