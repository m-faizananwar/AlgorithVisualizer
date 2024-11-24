from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import os

root = Tk()
# Corrected the file path separator and ensured it handles single or double slashes.
image = PhotoImage(file='nel.png')

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
welcome_label.place(x=130, y=25)

# Adding the background image
bg_label = Label(root, image=image, bg='#2F6C60')
bg_label.place(x=130, y=65)

# Adding the progress label
progres_label = Label(root, text='Loading...', bg='#2F6C60', font=("Trebuchet Ms", 10, "bold"), fg='#FFFFFF')
progres_label.place(x=190, y=330)

# Configuring the progress bar style
progress = ttk.Style()
progress.theme_use('clam')  # Changed from 'clan' to 'clam', which is a valid theme
progress.configure("red.Horizontal.TProgressbar", troughcolor='red', background='#108CFF')

# Adding the progress bar
progress_bar = Progressbar(root, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=400, mode='determinate')
progress_bar.place(x=70, y=370)

# Define a function to open the main script
def def_top():
    root.withdraw()
    os.system('python main.py')
    root.destroy()

i = 0  # Initialize the global variable

# Define the loading function
def load():
    global i
    if i <= 10:
        txt = f'Loading {10 * i}%'
        progres_label.config(text=txt)
        progres_label.after(600, load)
        progress_bar['value'] = 10 * i
        i += 1
    else:
        def_top()

load()

# Set the window to be non-resizable
root.resizable(False, False)
root.mainloop()
