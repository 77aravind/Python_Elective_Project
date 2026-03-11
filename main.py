import tkinter as tk
from gui import SecurePassProGUI
import sys

def main():
    try:
        import zxcvbn
        import matplotlib
    except ImportError:
        print("Error: Missing dependencies. Please run 'pip install -r requirements.txt'")
        sys.exit(1)

    import customtkinter as ctk
    from gui import SplashScreen, SecurePassProGUI

    # Initialize single root
    root = ctk.CTk()
    root.withdraw() # Hide initially

    # Show Splash Screen on the same root
    splash = SplashScreen(root)
    
    # After splash duration, initialize main GUI
    def start_app():
        for widget in root.winfo_children():
            widget.destroy()
        
        root.overrideredirect(False) # Restore title bar
        root.deiconify() # Show main window
        app = SecurePassProGUI(root)

    root.after(3000, start_app)
    root.mainloop()

if __name__ == "__main__":
    main()
