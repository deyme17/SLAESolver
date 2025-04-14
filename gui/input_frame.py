import tkinter as tk
from tkinter import ttk, messagebox

class InputFrame:
    """Frame for input data with improved UI"""
    
    def __init__(self, parent, calculate_callback):
        """
        Initialize the input frame.
        
        Args:
            parent: Parent widget
            calculate_callback: Function to call when calculate button is clicked
        """
        self.parent = parent
        self.calculate_callback = calculate_callback
    
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.frame.columnconfigure(0, weight=1)

        self._create_widgets()
        
    def _create_widgets(self):
        """Create and place widgets with improved layout"""
        header = ttk.Label(
            self.frame, 
            text="Знаходження коренів нелінійних рівнянь",
            style="Header.TLabel"
        )
        header.grid(column=0, row=0, columnspan=2, pady=(0, 15), sticky="w")
        
        # method selection
        method_frame = ttk.LabelFrame(self.frame, text="Метод розв'язання")
        method_frame.grid(column=0, row=1, padx=5, pady=5, sticky="ew")
        method_frame.columnconfigure(0, weight=1)
        
        self.method_var = tk.StringVar(value="bisection")
        
        method_inner_frame = ttk.Frame(method_frame)
        method_inner_frame.grid(column=0, row=0, padx=10, pady=10, sticky="w")
        
        self.bisection_radio = ttk.Radiobutton(
            method_inner_frame, 
            text="Метод половинного ділення", 
            variable=self.method_var, 
            value="bisection"
        )
        self.chord_radio = ttk.Radiobutton(
            method_inner_frame, 
            text="Метод хорд", 
            variable=self.method_var, 
            value="chord"
        )
        
        self.bisection_radio.grid(column=0, row=0, padx=(0, 20), pady=5, sticky="w")
        self.chord_radio.grid(column=1, row=0, padx=0, pady=5, sticky="w")
        
        # equation input
        equation_frame = ttk.LabelFrame(self.frame, text="Рівняння")
        equation_frame.grid(column=0, row=2, padx=5, pady=5, sticky="ew")
        equation_frame.columnconfigure(0, weight=1)
        
        equation_inner_frame = ttk.Frame(equation_frame)
        equation_inner_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew")
        equation_inner_frame.columnconfigure(1, weight=1)
        
        ttk.Label(equation_inner_frame, text="f(x) =").grid(column=0, row=0, padx=(0, 10), pady=5, sticky="w")
        self.equation_var = tk.StringVar(value="x^3 - 3*x^2 + x + 5")
        self.equation_entry = ttk.Entry(equation_inner_frame, width=40, textvariable=self.equation_var)
        self.equation_entry.grid(column=1, row=0, padx=0, pady=5, sticky="ew")
        ttk.Label(equation_inner_frame, text="= 0").grid(column=2, row=0, padx=(10, 0), pady=5, sticky="w")
        
        # params
        params_frame = ttk.LabelFrame(self.frame, text="Параметри")
        params_frame.grid(column=0, row=3, padx=5, pady=5, sticky="ew")
        params_frame.columnconfigure(0, weight=1)
        params_frame.columnconfigure(2, weight=1)
        
        # interval
        interval_frame = ttk.Frame(params_frame)
        interval_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew")
        
        ttk.Label(interval_frame, text="Інтервал пошуку:").grid(column=0, row=0, padx=0, pady=5, sticky="w")
        
        interval_input_frame = ttk.Frame(interval_frame)
        interval_input_frame.grid(column=0, row=1, padx=0, pady=0, sticky="w")
        
        ttk.Label(interval_input_frame, text="a =").grid(column=0, row=0, padx=(0, 5), pady=5, sticky="w")
        self.a_var = tk.DoubleVar(value=-4.0)
        self.a_entry = ttk.Entry(interval_input_frame, width=8, textvariable=self.a_var)
        self.a_entry.grid(column=1, row=0, padx=0, pady=5, sticky="w")
        
        ttk.Label(interval_input_frame, text="b =").grid(column=2, row=0, padx=(15, 5), pady=5, sticky="w")
        self.b_var = tk.DoubleVar(value=4.0)
        self.b_entry = ttk.Entry(interval_input_frame, width=8, textvariable=self.b_var)
        self.b_entry.grid(column=3, row=0, padx=0, pady=5, sticky="w")
        
        toliter_frame = ttk.Frame(params_frame)
        toliter_frame.grid(column=0, row=1, padx=10, pady=(0, 10), sticky="ew")
        
        # tolerance
        ttk.Label(toliter_frame, text="Точність (ε) =").grid(column=0, row=0, padx=(0, 5), pady=5, sticky="w")
        self.tolerance_var = tk.StringVar(value="0.001")
        self.tolerance_entry = ttk.Entry(toliter_frame, width=8, textvariable=self.tolerance_var)
        self.tolerance_entry.grid(column=1, row=0, padx=0, pady=5, sticky="w")
        
        # max iter
        ttk.Label(toliter_frame, text="Макс. ітерацій =").grid(column=2, row=0, padx=(15, 5), pady=5, sticky="w")
        self.max_iter_var = tk.IntVar(value=100)
        self.max_iter_entry = ttk.Entry(toliter_frame, width=8, textvariable=self.max_iter_var)
        self.max_iter_entry.grid(column=3, row=0, padx=0, pady=5, sticky="w")
        
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(column=0, row=4, pady=(15, 0), sticky="ew")
        button_frame.columnconfigure(1, weight=1) 
        
        self.calculate_button = ttk.Button(
            button_frame, 
            text="Обчислити", 
            command=self.calculate_callback,
            width=15
        )
        self.calculate_button.grid(column=0, row=0, padx=(0, 10))
        
        self.clear_button = ttk.Button(
            button_frame, 
            text="Очистити", 
            command=self.clear,
            width=15
        )
        self.clear_button.grid(column=1, row=0, padx=10)
        
        self.help_button = ttk.Button(
            button_frame, 
            text="Довідка", 
            command=self.show_help,
            width=15
        )
        self.help_button.grid(column=2, row=0, padx=(10, 0))
        
        self.equation_entry.focus_set()
        
    def get_equation(self):
        """Get the entered equation"""
        return self.equation_var.get()
    
    def get_a(self):
        """Get the left interval boundary"""
        return self.a_var.get()
    
    def get_b(self):
        """Get the right interval boundary"""
        return self.b_var.get()
    
    def get_tolerance(self):
        """Get the tolerance value"""
        return float(self.tolerance_var.get())
    
    def get_max_iter(self):
        """Get the maximum iterations value"""
        return self.max_iter_var.get()
    
    def get_method(self):
        """Get the selected method"""
        return self.method_var.get()
    
    def clear(self):
        """Clear all input fields"""
        self.equation_var.set("x^3 - 3*x^2 + x + 5")
        self.a_var.set(-4.0)
        self.b_var.set(4.0)
        self.tolerance_var.set("0.001")
        self.max_iter_var.set(100)
        self.equation_entry.focus_set()
    
    def show_help(self):
        """Show help information with improved formatting"""
        help_text = """
Знаходження коренів нелінійних рівнянь

Доступні методи:
• Метод половинного ділення - послідовне ділення інтервалу навпіл для знаходження кореня
• Метод хорд - використовує апроксимацію функції прямою лінією (хордою)

Як користуватись:
1. Введіть рівняння у форматі f(x)
2. Задайте інтервал пошуку кореня [a, b]
3. Встановіть бажану точність ε
4. Виберіть метод розв'язання
5. Натисніть "Обчислити"

Примітки:
• Функція повинна змінювати знак на інтервалі [a, b]
• У рівнянні можна використовувати:
  - Базові операції: +, -, *, /, ^
  - Функції: sin, cos, tan, exp, log, sqrt
  - Константи: pi, e
        """
        
        messagebox.showinfo("Довідка", help_text)