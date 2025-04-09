import tkinter as tk
from tkinter import ttk

class ResultsFrame:
    """Frame for displaying calculation results with improved UI"""
    
    def __init__(self, parent):
        """
        Initialize the results frame.
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and place widgets with improved layout"""
        # summary info
        self.info_frame = ttk.LabelFrame(self.frame, text="Результати")
        self.info_frame.grid(column=0, row=0, padx=5, pady=5, sticky="ew")
        
        info_grid = ttk.Frame(self.info_frame)
        info_grid.pack(fill="x", padx=10, pady=10)
        
        # method name
        ttk.Label(info_grid, text="Метод:", font=("Helvetica", 9, "bold")).grid(column=0, row=0, padx=(0, 10), pady=5, sticky="w")
        self.method_name_var = tk.StringVar()
        ttk.Label(info_grid, textvariable=self.method_name_var).grid(column=1, row=0, padx=0, pady=5, sticky="w")
        
        # found root
        ttk.Label(info_grid, text="Знайдений корінь:", font=("Helvetica", 9, "bold")).grid(column=0, row=1, padx=(0, 10), pady=5, sticky="w")
        self.root_var = tk.StringVar()
        ttk.Label(info_grid, textvariable=self.root_var).grid(column=1, row=1, padx=0, pady=5, sticky="w")
        
        # func val
        ttk.Label(info_grid, text="Значення функції:", font=("Helvetica", 9, "bold")).grid(column=0, row=2, padx=(0, 10), pady=5, sticky="w")
        self.fx_var = tk.StringVar()
        ttk.Label(info_grid, textvariable=self.fx_var).grid(column=1, row=2, padx=0, pady=5, sticky="w")
        
        # iters
        ttk.Label(info_grid, text="Кількість ітерацій:", font=("Helvetica", 9, "bold")).grid(column=0, row=3, padx=(0, 10), pady=5, sticky="w")
        self.iter_var = tk.StringVar()
        ttk.Label(info_grid, textvariable=self.iter_var).grid(column=1, row=3, padx=0, pady=5, sticky="w")
        
        # accuracy
        ttk.Label(info_grid, text="Досягнута точність:", font=("Helvetica", 9, "bold")).grid(column=0, row=4, padx=(0, 10), pady=5, sticky="w")
        self.accuracy_var = tk.StringVar()
        ttk.Label(info_grid, textvariable=self.accuracy_var).grid(column=1, row=4, padx=0, pady=5, sticky="w")
        
        # table with iters
        self.table_frame = ttk.LabelFrame(self.frame, text="Таблиця ітерацій")
        self.table_frame.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")
        
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=1)
  
        self.tree = ttk.Treeview(self.table_frame)

        h_scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=h_scrollbar.set)
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        v_scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=v_scrollbar.set)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
    
        self.tree.grid(row=0, column=0, sticky="nsew")
    
    def display_results(self, results, method_type):
        """
        Display calculation results with improved formatting.
        
        Args:
            results: Dictionary with calculation results
            method_type: Type of method used (bisection or chord)
        """
        self.method_name_var.set(results['method_name'])
        self.root_var.set(f"{results['root']:.10f}")
        self.iter_var.set(str(results['iterations']))
        self.fx_var.set(f"{results['f_value']:.10f}")
        self.accuracy_var.set(f"{results['tolerance']:.10f}")
        
        self.tree.delete(*self.tree.get_children())
        
        if method_type == "bisection":
            self._setup_bisection_tree()
            self._populate_bisection_tree(results['history'])
        else:  # chord
            self._setup_chord_tree()
            self._populate_chord_tree(results['history'])
    
    def _setup_bisection_tree(self):
        """Set up tree for bisection method with better column configuration"""
        for col in self.tree['columns']:
            self.tree.column(col, width=0)
            self.tree.heading(col, text="")
        
        # config columns
        columns = ('iteration', 'a', 'b', 'c', 'f(a)', 'f(b)', 'f(c)', 'b-a')
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'

        self.tree.heading('iteration', text='Ітерація (k)')
        self.tree.heading('a', text='a')
        self.tree.heading('b', text='b')
        self.tree.heading('c', text='c')
        self.tree.heading('f(a)', text='f(a)')
        self.tree.heading('f(b)', text='f(b)')
        self.tree.heading('f(c)', text='f(c)')
        self.tree.heading('b-a', text='|b-a|')

        self.tree.column('iteration', width=80, anchor='center')
        self.tree.column('a', width=100, anchor='center')
        self.tree.column('b', width=100, anchor='center')
        self.tree.column('c', width=100, anchor='center')
        self.tree.column('f(a)', width=100, anchor='center')
        self.tree.column('f(b)', width=100, anchor='center')
        self.tree.column('f(c)', width=100, anchor='center')
        self.tree.column('b-a', width=100, anchor='center')
    
    def _setup_chord_tree(self):
        """Set up tree for chord method with better column configuration"""
        for col in self.tree['columns']:
            self.tree.column(col, width=0)
            self.tree.heading(col, text="")
        
        # config columns
        columns = ('iteration', 'a', 'b', 'x', 'f(a)', 'f(b)', 'f(x)', 'delta')
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        self.tree.heading('iteration', text='Ітерація (k)')
        self.tree.heading('a', text='a')
        self.tree.heading('b', text='b')
        self.tree.heading('x', text='x')
        self.tree.heading('f(a)', text='f(a)')
        self.tree.heading('f(b)', text='f(b)')
        self.tree.heading('f(x)', text='f(x)')
        self.tree.heading('delta', text='|x_k - x_(k-1)|')
        
        # Set optimal column widths
        self.tree.column('iteration', width=80, anchor='center')
        self.tree.column('a', width=100, anchor='center')
        self.tree.column('b', width=100, anchor='center')
        self.tree.column('x', width=100, anchor='center')
        self.tree.column('f(a)', width=100, anchor='center')
        self.tree.column('f(b)', width=100, anchor='center')
        self.tree.column('f(x)', width=100, anchor='center')
        self.tree.column('delta', width=120, anchor='center')
    
    def _populate_bisection_tree(self, history):
        """
        Populate tree with bisection method data.
        
        Args:
            history: List of iteration data
        """
        self.tree.tag_configure('oddrow', background='#f0f0f0')
        self.tree.tag_configure('evenrow', background='#ffffff')
        
        for i, entry in enumerate(history):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(
                entry['iter'],
                f"{entry['a']:.8f}",
                f"{entry['b']:.8f}",
                f"{entry['c']:.8f}",
                f"{entry['fa']:.8f}",
                f"{entry['fb']:.8f}",
                f"{entry['fc']:.8f}",
                f"{entry['interval']:.8f}"
            ), tags=(tag,))
    
    def _populate_chord_tree(self, history):
        """
        Populate tree with chord method data.
        
        Args:
            history: List of iteration data
        """
        self.tree.tag_configure('oddrow', background='#f0f0f0')
        self.tree.tag_configure('evenrow', background='#ffffff')
        
        for i, entry in enumerate(history):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(
                entry['iter'],
                f"{entry['a']:.8f}",
                f"{entry['b']:.8f}",
                f"{entry['x']:.8f}",
                f"{entry['fa']:.8f}",
                f"{entry['fb']:.8f}",
                f"{entry['fx']:.8f}",
                f"{entry['delta']:.8f}"
            ), tags=(tag,))