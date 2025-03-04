from database import init_db
from gui import ManicuristApp
import ttkbootstrap as ttk

if __name__ == "__main__":
    # Initialize the database (create tables if they don't exist)
    init_db()
    
    # Start the application
    root = ttk.Window(themename="cosmo")
    app = ManicuristApp(root)
    root.mainloop()
