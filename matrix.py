from collections import Counter
from threading import Lock
import random


class Matrix:
    N = 10

    @staticmethod
    def __flatten(matrix):
        return [x for row in matrix for x in row]

    @staticmethod
    def __deflatten(matrix):
        ret = []
        for i in range(Matrix.N):
            row = []
            for j in range(Matrix.N):
                row.append(matrix[i * Matrix.N + j])

            ret.append(row)

        return ret

    def __init__(self):
        self.lock = Lock()
        self.matrix = []
        for _ in range(Matrix.N * Matrix.N):
            self.matrix.append(random.randint(1, 10))

        self.matrix = Matrix.__deflatten(self.matrix)

    def __repr__(self):
        with self.lock:
            return "\n".join([" ".join([f"{x:3}" for x in row]) for row in self.matrix])

    def sort(self):
        with self.lock:
            self.matrix = Matrix.__flatten(self.matrix)
            self.matrix.sort()
            self.matrix = Matrix.__deflatten(self.matrix)

        return True

    def transpose(self):
        with self.lock:
            self.matrix = [list(x) for x in zip(*self.matrix)]

        return True

    def sum(self):
        with self.lock:
            return sum(sum(x for x in row) for row in self.matrix)

    def max(self):
        with self.lock:
            return max(Matrix.__flatten(self.matrix))

    def count(self):
        with self.lock:
            cnt = Counter(Matrix.__flatten(self.matrix))
            return cnt
