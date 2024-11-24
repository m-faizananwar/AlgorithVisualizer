from tkinter import Tk
from splashscreen import SplashScreen

def main():
    # Your main application logic here
    print("Main application started!")

if __name__ == "__main__":
    root = Tk()
    splash = SplashScreen(root, "nel.png")
    splash.start_loading()
    root.mainloop()

    # Start your main application after the splash screen
    main()
