import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GraphFrame:
    """Frame for displaying graphs with improved UI"""
    
    def __init__(self, parent):
        """
        Initialize the graph frame.
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        self.function_frame = ttk.Frame(self.notebook)
        self.convergence_frame = ttk.Frame(self.notebook)
        
        self.function_frame.columnconfigure(0, weight=1)
        self.function_frame.rowconfigure(0, weight=1)
        self.convergence_frame.columnconfigure(0, weight=1)
        self.convergence_frame.rowconfigure(0, weight=1)
        
        self.notebook.add(self.function_frame, text='Графік функції')
        self.notebook.add(self.convergence_frame, text='Збіжність методу')
  
        self.function_canvas = None
        self.convergence_canvas = None

        self._create_empty_plots()
    
    def _create_empty_plots(self):
        """Create initial empty plots"""
        # func plot
        fig1 = Figure(figsize=(5, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.set_title('Графік функції')
        ax1.set_xlabel('x')
        ax1.set_ylabel('f(x)')
        ax1.grid(True, linestyle='--', alpha=0.7)
        fig1.tight_layout()
        
        self.function_canvas = FigureCanvasTkAgg(fig1, master=self.function_frame)
        self.function_canvas.draw()
        self.function_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # plot
        fig2 = Figure(figsize=(5, 4), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.set_title('Збіжність методу')
        ax2.set_xlabel('Ітерація')
        ax2.set_ylabel('Похибка')
        ax2.grid(True, linestyle='--', alpha=0.7)
        fig2.tight_layout()
        
        self.convergence_canvas = FigureCanvasTkAgg(fig2, master=self.convergence_frame)
        self.convergence_canvas.draw()
        self.convergence_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def update_canvas_size(self):
        """Update canvas sizes when window is resized"""
        if self.function_canvas:
            self.function_canvas.figure.tight_layout()
            self.function_canvas.draw()
        
        if self.convergence_canvas:
            self.convergence_canvas.figure.tight_layout()
            self.convergence_canvas.draw()
    
    def create_function_plot(self, func, results, a, b):
        """
        Create plot of the function with root.
        
        Args:
            func: Function to plot
            results: Calculation results
            a, b: Interval boundaries
        """
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        root = results['root']
    
        margin = (b - a) * 0.1
        x_min = a - margin
        x_max = b + margin
        
        x = np.linspace(x_min, x_max, 1000)
        y = [func(xi) for xi in x]
        
        y_values = np.array(y)
        y_filtered = y_values[np.isfinite(y_values)]
        if len(y_filtered) > 0:
            y_range = np.max(y_filtered) - np.min(y_filtered)
            y_min = np.min(y_filtered) - 0.1 * y_range
            y_max = np.max(y_filtered) + 0.1 * y_range
            ax.set_ylim(y_min, y_max)

        ax.plot(x, y, 'b-', linewidth=2, label='f(x)')
    
        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
        ax.axvline(x=0, color='gray', linestyle='-', alpha=0.5)

        ax.plot(root, func(root), 'ro', markersize=8, label=f'Корінь: x = {root:.6f}')

        ax.axvspan(a, b, alpha=0.1, color='green', label=f'Інтервал [{a}, {b}]')

        ax.set_title('Графік функції з знайденим коренем', fontsize=12, fontweight='bold')
        ax.set_xlabel('x', fontsize=10)
        ax.set_ylabel('f(x)', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        ax.legend(loc='best', framealpha=0.9, fontsize=9)

        ax.tick_params(direction='out', length=4, width=1, colors='black')

        fig.tight_layout()
  
        if self.function_canvas:
            self.function_canvas.get_tk_widget().grid_forget()
        
        self.function_canvas = FigureCanvasTkAgg(fig, master=self.function_frame)
        self.function_canvas.draw()
        self.function_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def create_convergence_plot(self, results, method_type):
        """
        Create plot showing convergence of the method.
        
        Args:
            results: Calculation results
            method_type: Type of method used (bisection or chord)
        """
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        iterations = [entry['iter'] for entry in results['history']]
        
        if method_type == "bisection":
            errors = [entry['interval'] for entry in results['history']]
            method_name = "Метод половинного ділення"
            y_label = "Інтервал (b-a)"
        else:  # chord
            errors = [entry['delta'] for entry in results['history']]
            method_name = "Метод хорд"
            y_label = "Зміна наближення |x_k - x_(k-1)|"

        ax.semilogy(iterations, errors, 'ro-', linewidth=2, markersize=6, label=method_name)

        if len(iterations) > 1:
            try:
                # Make sure errors are positive
                valid_errors = [max(err, 1e-15) for err in errors[-min(3, len(iterations)):]]
                x_trend = np.linspace(0, max(iterations) * 1.1, 100)
                p = np.polyfit(iterations[-min(3, len(iterations)):], np.log(valid_errors), 1)
                y_trend = np.exp(p[0] * x_trend + p[1])
                ax.semilogy(x_trend, y_trend, 'b--', alpha=0.5, linewidth=1.5, label='Тренд збіжності')
            except Exception as e:
                print(f"Помилка побудови тренду збіржності: {e}")
        
        ax.set_title('Збіжність методу', fontsize=12, fontweight='bold')
        ax.set_xlabel('Ітерація', fontsize=10)
        ax.set_ylabel(y_label, fontsize=10)
        ax.grid(True, which='both', linestyle='--', alpha=0.7)

        ax.legend(loc='upper right', framealpha=0.9, fontsize=9)
       
        ax.tick_params(direction='out', length=4, width=1, colors='black')
     
        if 'tolerance' in results:
            tolerance = results['tolerance']
            ax.axhline(y=tolerance, color='green', linestyle='-.', alpha=0.8, 
                       label=f'Досягнута точність: {tolerance:.6f}')
  
        if len(iterations) > 2:
            if method_type == "bisection":
                rate_text = "Швидкість збіжності ≈ O(1/2^n)"
            else:
                rate_text = "Швидкість збіжності ≈ O(1/n)"
            
            ax.text(0.05, 0.05, rate_text, transform=ax.transAxes, 
                   fontsize=9, bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
        
        fig.tight_layout()
        
        if self.convergence_canvas:
            self.convergence_canvas.get_tk_widget().grid_forget()
        
        self.convergence_canvas = FigureCanvasTkAgg(fig, master=self.convergence_frame)
        self.convergence_canvas.draw()
        self.convergence_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)