from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk  # For image resizing
import os

root = Tk()

# Resize the image using PIL
original_image = Image.open('nel.png')
resized_image = original_image.resize((250, 250), Image.Resampling.LANCZOS)  # Updated resizing method
image = ImageTk.PhotoImage(resized_image)

# Set the dimensions of the application window
height = 430
width = 530
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
root.overrideredirect(True)

# Background color updated to a proper hex code with '#' prefix
root.config(background="#2F6C60")

# Adding the welcome label
welcome_label = Label(root, text='Algorithm Visualizer', bg='#2F6C60', font=("Trebuchet Ms", 15, "bold"), fg='#FFFFFF')
welcome_label.place(x=160, y=25)

# Adding the resized background image
bg_label = Label(root, image=image, bg='#2F6C60')
bg_label.place(x=130, y=65)  # Centered horizontally

# Adding the progress label
progres_label = Label(root, text='Loading...', bg='#2F6C60', font=("Trebuchet Ms", 10, "bold"), fg='#FFFFFF')
progres_label.place(x=190, y=330)

# Configuring the progress bar style
progress = ttk.Style()
progress.theme_use('clam')
progress.configure("blue.Horizontal.TProgressbar", troughcolor='gray', background='cyan')

# Adding the smoother progress bar
progress_bar = Progressbar(root, style="blue.Horizontal.TProgressbar", orient=HORIZONTAL, length=400, mode='determinate')
progress_bar.place(x=70, y=370)

# Define a function to open the main script
def def_top():
    root.withdraw()
    os.system('python main.py')
    root.destroy()

i = 0  # Initialize the global variable

def load():
    global i
    if i <= 100:
        txt = f'Loading {i}%'
        progres_label.config(text=txt)
        progress_bar['value'] = i
        i += 1
        root.after(50, load)  # Adjust the speed for smoother animation
    else:
        def_top()

load()

# Set the window to be non-resizable
root.resizable(False, False)
root.mainloop()
