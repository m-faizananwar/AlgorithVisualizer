import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def on_button_click(size):
    """Handles button click events."""
    for widget in root.winfo_children():
        widget.destroy()
    label = ttk.Label(root, text=f"You selected: {size}", font=("Helvetica", 24, "bold"), bootstyle="info", background='#2F6C60')
    
    label.pack(pady=50, anchor='center')

    close_button = ttk.Button(
        root,
        text="Close",
        command=root.destroy,
        bootstyle="dark-outline",
        style="Custom.TButton"
    )
    close_button.pack(pady=20)

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

# Draw the main menu
draw_menu()

# Run the application
root.mainloop()