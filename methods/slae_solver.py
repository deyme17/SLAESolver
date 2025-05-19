from abc import ABC, abstractmethod

class SLAESolver(ABC):
    def __init__(self, A, b, tol=1e-6, max_iter=100):
        self.A = A
        self.b = b
        self.tol = tol
        self.max_iter = max_iter
        self.history = []

    @abstractmethod
    def solve(self):
        pass