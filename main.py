from tkinter import Tk
from gui.app_window import SLAESolverApp

from methods.gauss_method import GaussMethod
from methods.zeidel_method import ZeidelMethod
from utils.method_register import SLAEMethodRegistry

SLAEMethodRegistry.register(GaussMethod)
SLAEMethodRegistry.register(ZeidelMethod)

if __name__ == '__main__':
    root = Tk()
    app = SLAESolverApp(root)
    root.mainloop()
