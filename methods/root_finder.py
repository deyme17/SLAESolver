from abc import ABC, abstractmethod
import numpy as np

class RootFinder(ABC):
    """Abstract base class for root finding methods"""
    
    def __init__(self, function, tol=1e-6, max_iter=100):
        """
        Initialize the root finder.
        
        Args:
            function: The function for which to find roots
            tol: Tolerance (accuracy) of the solution
            max_iter: Maximum number of iterations
        """
        self.function = function
        self.tolerance = tol
        self.max_iter = max_iter
        self.history = []
        
    @abstractmethod
    def find_root(self, a, b):
        """
        Find the root of the function in interval [a, b].
        
        Args:
            a: Left boundary of interval
            b: Right boundary of interval
            
        Returns:
            Dictionary containing root, iterations, function value, tolerance, and history
        """
        pass
    
    def check_interval(self, a, b):
        """
        Check if the function changes sign in the interval [a, b].
        
        Args:
            a: Left boundary of interval
            b: Right boundary of interval
            
        Returns:
            True if function changes sign, False otherwise
        """
        fa = self.function(a)
        fb = self.function(b)
        return fa * fb < 0
