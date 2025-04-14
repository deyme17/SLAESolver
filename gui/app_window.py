import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from gui.input_frame import InputFrame
from gui.results_frame import ResultsFrame
from gui.graph_frame import GraphFrame
from methods.bisection_method import BisectionMethod
from methods.chord_method import ChordMethod

class RootFindingApp:
    """Main application class with improved UI"""
    
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Уточнення коренів рівняння")
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
        self.tab3 = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab1, text='Вхідні дані')
        self.tab_control.add(self.tab2, text='Розрахунки')
        self.tab_control.add(self.tab3, text='Графіки')
        
        # conf tab frames
        for tab in (self.tab1, self.tab2, self.tab3):
            tab.columnconfigure(0, weight=1)
            tab.rowconfigure(0, weight=1)
        
        # frames
        self.input_frame = InputFrame(self.tab1, self.calculate)
        self.results_frame = ResultsFrame(self.tab2)
        self.graph_frame = GraphFrame(self.tab3)
        
        # status bar
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
        
        self.results = None
    
        self.root.bind("<Configure>", self._on_window_resize)
    
    def _configure_style(self):
        """Configure the application style"""
        style = ttk.Style()
        
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'vista' in available_themes:
            style.theme_use('vista')
        
        # styles
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TNotebook', background='#f0f0f0', tabmargins=[2, 5, 2, 0])
        style.configure('TNotebook.Tab', padding=[10, 2], background='#e0e0e0', font=('Helvetica', 9))
        style.map('TNotebook.Tab', 
                  background=[('selected', '#f0f0f0'), ('active', '#e8e8e8')],
                  foreground=[('selected', '#000000')])
        
        style.configure('TLabel', background='#f5f5f5', font=('Helvetica', 9))
        style.configure('TEntry', padding=5)
        style.configure('TButton', padding=5, font=('Helvetica', 9))
        
        style.configure('Header.TLabel', font=('Helvetica', 11, 'bold'))
        style.configure('Results.TFrame', background='#ffffff')
        
    def _on_window_resize(self, event):
        """Handle window resize event"""
        if event.widget == self.root:
            self.graph_frame.update_canvas_size()
            
    def calculate(self):
        """Calculate the root using the selected method"""
        try:
            equation_str = self.input_frame.get_equation()
            a = self.input_frame.get_a()
            b = self.input_frame.get_b()
            tolerance = self.input_frame.get_tolerance()
            max_iter = self.input_frame.get_max_iter()
            method_type = self.input_frame.get_method()
     
            def f(x):
                eq = equation_str.replace("^", "**")

                locals_dict = {
                    'sin': np.sin,
                    'cos': np.cos,
                    'tan': np.tan,
                    'exp': np.exp,
                    'log': np.log,
                    'sqrt': np.sqrt,
                    'pi': np.pi,
                    'e': np.e
                }
                return eval(eq, {"__builtins__": {}}, {**locals_dict, 'x': x})
            
            # change sigh?
            fa = f(a)
            fb = f(b)
            
            if fa * fb > 0:
                messagebox.showerror("Помилка", f"Функція не змінює знак на інтервалі [{a}, {b}].\nf({a}) = {fa:.6f}, f({b}) = {fb:.6f}")
                return
            
            self.status_var.set("Обчислення...")
            self.root.update_idletasks()
            
            # create appropriate root finder
            if method_type == "bisection":
                finder = BisectionMethod(f, tolerance, max_iter)
                method_name = "Метод половинного ділення"
            else:  # chord
                finder = ChordMethod(f, tolerance, max_iter)
                method_name = "Метод хорд"
            
            # calc root
            self.results = finder.find_root(a, b)
            self.results['method_name'] = method_name
            self.results['function'] = f
            self.results['a'] = a
            self.results['b'] = b
            
            # display
            self.results_frame.display_results(self.results, method_type)
            self.graph_frame.create_function_plot(f, self.results, a, b)
            self.graph_frame.create_convergence_plot(self.results, method_type)
            
            self.status_var.set("Обчислення завершено")
            self.tab_control.select(1)
            
        except Exception as e:
            messagebox.showerror("Помилка", str(e))
            self.status_var.set("Помилка обчислень")