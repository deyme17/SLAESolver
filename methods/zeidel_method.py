import numpy as np
from methods.slae_solver import SLAESolver

class ZeidelMethod(SLAESolver):
    display_name = "Метод Зейделя"

    def solve(self):
        A, b = self.A, self.b
        n = len(b)
        x = np.zeros(n)
        for k in range(self.max_iter):
            x_old = x.copy()
            for i in range(n):
                s1 = sum(A[i][j] * x[j] for j in range(i))
                s2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
                x[i] = (b[i] - s1 - s2) / A[i][i]
            self.history.append(x.copy())
            if np.linalg.norm(x - x_old, ord=np.inf) < self.tol:
                break
        return x
