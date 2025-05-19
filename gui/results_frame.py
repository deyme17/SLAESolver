import tkinter as tk
from tkinter import ttk

class ResultsFrame:
    """Frame for displaying calculation results"""

    def __init__(self, parent):
        self.parent = parent

        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self._create_widgets()

    def _create_widgets(self):
        # results label
        self.info_frame = ttk.LabelFrame(self.frame, text="Розв'язок")
        self.info_frame.grid(column=0, row=0, padx=5, pady=5, sticky="ew")

        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(self.info_frame, textvariable=self.result_var, font=("Courier New", 10))
        self.result_label.pack(anchor="w", padx=10, pady=5)

        # table for iterations
        self.table_frame = ttk.LabelFrame(self.frame, text="Ітерації (лише для ітераційних методів)")
        self.table_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self.table_frame)

        h_scroll = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        v_scroll = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(xscroll=h_scroll.set, yscroll=v_scroll.set)

        h_scroll.grid(row=1, column=0, sticky="ew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.grid(row=0, column=0, sticky="nsew")

    def display_results(self, x, history, method_name):
        self.result_var.set("\n".join([f"x{i+1} = {val:.6f}" for i, val in enumerate(x)]))

        self.tree.delete(*self.tree.get_children())

        if history:
            self._setup_iteration_table(len(x))
            for i, x_iter in enumerate(history):
                row = [f"{val:.6f}" for val in x_iter]
                self.tree.insert("", "end", values=[i + 1] + row)

    def _setup_iteration_table(self, var_count):
        columns = ["iter"] + [f"x{i+1}" for i in range(var_count)]
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'

        self.tree.heading('iter', text='Ітерація')
        self.tree.column('iter', width=80, anchor='center')

        for i in range(var_count):
            key = f"x{i+1}"
            self.tree.heading(key, text=key)
            self.tree.column(key, width=100, anchor='center')