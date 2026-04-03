"""Matrix class — the foundation for everything else.

Stores data as a flat list in row-major order.
All indexing is explicit: element (i,j) = data[i * cols + j].
"""

from linalg_core import EPSILON


class Matrix:
    """A matrix stored as a flat row-major list of floats."""

    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        if data is not None:
            if len(data) != rows * cols:
                raise ValueError(f"Expected {rows*cols} elements, got {len(data)}")
            self.data = [float(x) for x in data]
        else:
            self.data = [0.0] * (rows * cols)

    @classmethod
    def from_lists(cls, lists):
        rows = len(lists)
        cols = len(lists[0])
        data = []
        for row in lists:
            if len(row) != cols:
                raise ValueError("All rows must have the same length")
            data.extend(row)
        return cls(rows, cols, data)

    @classmethod
    def identity(cls, n):
        m = cls(n, n)
        for i in range(n):
            m[i, i] = 1.0
        return m

    @classmethod
    def from_vector(cls, vec):
        return cls(len(vec), 1, vec)

    def __getitem__(self, key):
        i, j = key
        return self.data[i * self.cols + j]

    def __setitem__(self, key, value):
        i, j = key
        self.data[i * self.cols + j] = float(value)

    def get_row(self, i):
        start = i * self.cols
        return self.data[start:start + self.cols]

    def get_col(self, j):
        return [self.data[i * self.cols + j] for i in range(self.rows)]

    def copy(self):
        return Matrix(self.rows, self.cols, list(self.data))

    def to_lists(self):
        return [self.get_row(i) for i in range(self.rows)]

    def to_flat(self):
        return list(self.data)

    def __repr__(self):
        rows_str = []
        for i in range(self.rows):
            row = self.get_row(i)
            rows_str.append("  [" + ", ".join(f"{x:8.4f}" for x in row) + "]")
        return f"Matrix({self.rows}x{self.cols}):\n" + "\n".join(rows_str)

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        return all(
            abs(a - b) < EPSILON
            for a, b in zip(self.data, other.data)
        )
