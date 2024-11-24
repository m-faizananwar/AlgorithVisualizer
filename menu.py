import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def on_button_click(size):
    """Handles button click events."""
    for widget in root.winfo_children():
        widget.destroy()
    label = ttk.Label(root, text=f"You selected: {size}", font=("Helvetica", 24, "bold"), bootstyle="info")
    label.pack(pady=50, fill=X, expand=True)

    back_button = ttk.Button(
        root,
        text="Back to Menu",
        command=draw_menu,
        bootstyle="dark-outline"
    )
    back_button.pack(pady=20)

def draw_menu():
    """Draws the main menu."""
    global root
    for widget in root.winfo_children():
        widget.destroy()

    # Title
    title = ttk.Label(root, text="Select Maze Size", font=("Helvetica", 28, "bold"), bootstyle="primary")
    title.pack(pady=30, fill=X, expand=True)

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
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg='cyan')

# Create a custom style for buttons
style = ttk.Style()
style.configure("Custom.TButton", borderwidth=1, relief="solid", bordercolor="black", focusthickness=3, focuscolor="none")
style.map("Custom.TButton", background=[("active", "linear-gradient(to bottom, #00f, #0ff)")])

# Draw the main menu
draw_menu()

# Run the application
root.mainloop()