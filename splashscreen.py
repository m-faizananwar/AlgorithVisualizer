from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk  # For image resizing

class SplashScreen:
    def __init__(self, root, image_path, width=530, height=430):
        self.root = root
        self.image_path = image_path
        self.width = width
        self.height = height
        self.i = 0  # Initialize the progress counter
        
        # Configure root window
        self.root.overrideredirect(True)
        self.root.config(background="#2F6C60")
        self.center_window()
        
        # Load and resize image
        self.load_image()
        
        # Add UI components
        self.create_widgets()
        
    def center_window(self):
        """Centers the window on the screen."""
        x = (self.root.winfo_screenwidth() // 2) - (self.width // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.height // 2)
        self.root.geometry(f'{self.width}x{self.height}+{x}+{y}')
    
    def load_image(self):
        """Loads and resizes the splash screen image."""
        original_image = Image.open(self.image_path)
        resized_image = original_image.resize((250, 250), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)
    
    def create_widgets(self):
        """Creates and places the widgets on the splash screen."""
        # Welcome label
        self.welcome_label = Label(self.root, text='Algorithm Visualizer', 
                                   bg='#2F6C60', font=("Trebuchet Ms", 15, "bold"), fg='#FFFFFF')
        self.welcome_label.place(x=160, y=25)

        # Background image
        self.bg_label = Label(self.root, image=self.image, bg='#2F6C60')
        self.bg_label.place(x=130, y=65)
        
        # Progress label
        self.progres_label = Label(self.root, text='Loading...', bg='#2F6C60', 
                                   font=("Trebuchet Ms", 10, "bold"), fg='#FFFFFF')
        self.progres_label.place(x=190, y=330)

        # Configure progress bar style
        self.progress_style = ttk.Style()
        self.progress_style.theme_use('clam')
        self.progress_style.configure("blue.Horizontal.TProgressbar", troughcolor='gray', background='cyan')

        # Add progress bar
        self.progress_bar = Progressbar(self.root, style="blue.Horizontal.TProgressbar", 
                                        orient=HORIZONTAL, length=400, mode='determinate')
        self.progress_bar.place(x=70, y=370)

        # Footer label
        self.footer_label = Label(self.root, text="Developed by: M Faizan and Mahad © 2024", 
                                  bg='#2F6C60', font=("Arial", 9, "italic"), fg='#FFFFFF')
        self.footer_label.place(x=140, y=405)  # Positioned at the bottom of the window
    
    def start_loading(self):
        """Starts the loading animation."""
        if self.i <= 100:
            txt = f'Loading {self.i}%'
            self.progres_label.config(text=txt)
            self.progress_bar['value'] = self.i
            self.i += 1
            self.root.after(50, self.start_loading)
        else:
            self.finish()
    
    def finish(self):
        """Closes the splash screen and allows the main window to open."""
        self.root.destroy()


# Example usage
if __name__ == "__main__":
    root = Tk()
    splash = SplashScreen(root, "nel.png")
    splash.start_loading()
    root.mainloop()
