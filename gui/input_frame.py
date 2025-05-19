import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class InputFrame:
    """Frame for input data"""
    def __init__(self, parent, calculate_callback, method_choices):
        self.parent = parent
        self.calculate_callback = calculate_callback
        self.method_choices = method_choices

        self.n = 3 # Default size of the matrix

        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.frame.columnconfigure(0, weight=1)
        self._create_widgets()

    def _create_widgets(self):
        header = ttk.Label(self.frame, text="Введення системи лінійних рівнянь", style="Header.TLabel")
        header.grid(column=0, row=0, pady=(0, 15), sticky="w")

        # matrix table
        self.entries = []
        table_frame = ttk.Frame(self.frame)
        table_frame.grid(column=0, row=1, pady=5, sticky="n")

        for i in range(self.n):
            row_entries = []
            for j in range(self.n):
                e = ttk.Entry(table_frame, width=5)
                e.grid(row=i, column=j, padx=3, pady=2)
                e.insert(0, "1" if i == j else "0")
                row_entries.append(e)

            rhs = ttk.Entry(table_frame, width=5)
            rhs.grid(row=i, column=self.n + 1, padx=(10, 3))
            rhs.insert(0, "1")
            row_entries.append(rhs)
            self.entries.append(row_entries)

        # method selection
        method_frame = ttk.LabelFrame(self.frame, text="Метод")
        method_frame.grid(column=0, row=2, pady=10, sticky="ew")
        self.method_var = tk.StringVar(value=self.method_choices[0][0])

        for i, (method_id, label) in enumerate(self.method_choices):
            ttk.Radiobutton(method_frame, text=label, variable=self.method_var, value=method_id).grid(row=0, column=i, padx=10, pady=5)

        # parameters
        params_frame = ttk.Frame(self.frame)
        params_frame.grid(column=0, row=3, pady=10, sticky="w")

        ttk.Label(params_frame, text="Точність ε:").grid(row=0, column=0, sticky="w")
        self.tol_var = tk.StringVar(value="0.001")
        ttk.Entry(params_frame, width=10, textvariable=self.tol_var).grid(row=0, column=1, padx=5)

        ttk.Label(params_frame, text="Макс. ітерацій:").grid(row=0, column=2, padx=(10, 0), sticky="w")
        self.iter_var = tk.IntVar(value=50)
        ttk.Entry(params_frame, width=10, textvariable=self.iter_var).grid(row=0, column=3, padx=5)

        # buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(column=0, row=4, pady=(15, 0), sticky="ew")
        button_frame.columnconfigure(1, weight=1)

        ttk.Button(button_frame, text="Обчислити", command=self.calculate_callback, width=15).grid(column=0, row=0, padx=(0, 10))
        ttk.Button(button_frame, text="Очистити", command=self.clear, width=15).grid(column=1, row=0, padx=10)

    def get_matrix(self):
        """Read matrix A and vector b"""
        A = np.zeros((self.n, self.n))
        b = np.zeros(self.n)

        for i in range(self.n):
            for j in range(self.n):
                A[i, j] = float(self.entries[i][j].get())
            b[i] = float(self.entries[i][self.n].get())

        return A, b

    def get_method(self):
        return self.method_var.get()

    def get_tolerance(self):
        return float(self.tol_var.get())

    def get_max_iter(self):
        return int(self.iter_var.get())

    def clear(self):
        for i in range(self.n):
            for j in range(self.n + 1):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, "1" if i == j else "0")
