import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from gui.input_frame import InputFrame
from gui.results_frame import ResultsFrame
from utils.method_register import SLAEMethodRegistry

class SLAESolverApp:
    """Main application class"""

    def __init__(self, root):
        self.root = root
        self.root.title("Розв'язання СЛАР")
        self.root.geometry("900x600")

        self._configure_style()

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # tabs
        self.tab_control = ttk.Notebook(main_frame)
        self.tab_control.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Вхідні дані')
        self.tab_control.add(self.tab2, text='Результати')

        for tab in (self.tab1, self.tab2):
            tab.columnconfigure(0, weight=1)
            tab.rowconfigure(0, weight=1)

        self.input_frame = InputFrame(self.tab1, self.calculate, SLAEMethodRegistry.get_method_choices())
        self.results_frame = ResultsFrame(self.tab2)

        self.status_var = tk.StringVar()
        self.status_var.set("Готовий до роботи")
        self.status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2)
        )
        self.status_bar.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))

    def _configure_style(self):
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Helvetica', 9))
        style.configure('TButton', padding=5, font=('Helvetica', 9))
        style.configure('Header.TLabel', font=('Helvetica', 11, 'bold'))

    def calculate(self):
        try:
            A, b = self.input_frame.get_matrix()
            method_id = self.input_frame.get_method()
            tol = self.input_frame.get_tolerance()
            max_iter = self.input_frame.get_max_iter()

            method_class = SLAEMethodRegistry.get_method(method_id)
            if not method_class:
                raise ValueError(f"Метод '{method_id}' не знайдено в реєстрі")

            solver = method_class(A, b, tol, max_iter)
            x = solver.solve()

            self.results_frame.display_results(x, solver.history, method_class.display_name)
            self.status_var.set("Обчислення завершено")
            self.tab_control.select(1)

        except Exception as e:
            messagebox.showerror("Помилка", str(e))
            self.status_var.set("Помилка обчислень")