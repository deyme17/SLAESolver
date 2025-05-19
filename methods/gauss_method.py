import numpy as np
from methods.slae_solver import SLAESolver

class GaussMethod(SLAESolver):
    display_name = "Метод Гауса"

    def solve(self):
        A, b = self.A.copy(), self.b.copy()
        n = len(b)
        for i in range(n):
            max_row = np.argmax(abs(A[i:, i])) + i
            A[[i, max_row]] = A[[max_row, i]]
            b[[i, max_row]] = b[[max_row, i]]

            for j in range(i + 1, n):
                ratio = A[j][i] / A[i][i]
                A[j, i:] -= ratio * A[i, i:]
                b[j] -= ratio * b[i]

        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i][i]
        return x
