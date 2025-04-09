import tkinter as tk
from gui.app_window import RootFindingApp

def main():
    root = tk.Tk()
    app = RootFindingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()