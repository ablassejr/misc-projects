"""Determinant algorithms — Chapter 3.

Cofactor expansion, elimination-based, adjoint, Cramer's Rule.
Functions are added progressively as notebooks are completed.
"""

from linalg_core.matrix import Matrix
from linalg_core import EPSILON


# --- Notebook 3.1: Cofactor expansion ---

def minor(A, i, j):
    """Return the (i,j) minor: determinant of A with row i and column j deleted."""
    if A.rows != A.cols:
        raise ValueError("Minors are defined for square matrices")
    n = A.rows
    sub_data = []
    for r in range(n):
        if r == i:
            continue
        for c in range(n):
            if c == j:
                continue
            sub_data.append(A[r, c])
    sub = Matrix(n - 1, n - 1, sub_data)
    return det_cofactor(sub)


def cofactor(A, i, j):
    """Return the (i,j) cofactor: (-1)^(i+j) * minor(A, i, j)."""
    sign = (-1) ** (i + j)
    return sign * minor(A, i, j)


def det_cofactor(A):
    """Compute determinant by cofactor expansion along row 0.

    Recursive. Base case: 1×1 matrix.
    """
    if A.rows != A.cols:
        raise ValueError("Determinant requires a square matrix")
    n = A.rows
    if n == 1:
        return A[0, 0]
    if n == 2:
        return A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]

    result = 0.0
    for j in range(n):
        result += A[0, j] * cofactor(A, 0, j)
    return result


# --- Notebook 3.2: Elimination-based determinant ---

def det_elimination(A):
    """Compute determinant using elimination to upper triangular form.

    O(n³) instead of O(n!) for cofactor expansion.
    """
    from linalg_core.elimination import swap_rows

    if A.rows != A.cols:
        raise ValueError("Determinant requires a square matrix")
    n = A.rows
    m = A.copy()
    sign = 1

    for col in range(n):
        best = col
        for r in range(col + 1, n):
            if abs(m[r, col]) > abs(m[best, col]):
                best = r

        if abs(m[best, col]) < EPSILON:
            return 0.0

        if best != col:
            swap_rows(m, col, best)
            sign *= -1

        for r in range(col + 1, n):
            if abs(m[r, col]) > EPSILON:
                factor = m[r, col] / m[col, col]
                for k in range(col, n):
                    m[r, k] -= factor * m[col, k]

    det = float(sign)
    for i in range(n):
        det *= m[i, i]
    return det


# --- Notebook 3.4: Applications of determinants ---

def cofactor_matrix(A):
    """Return the matrix of cofactors."""
    if A.rows != A.cols:
        raise ValueError("Cofactor matrix requires a square matrix")
    n = A.rows
    C = Matrix(n, n)
    for i in range(n):
        for j in range(n):
            C[i, j] = cofactor(A, i, j)
    return C


def adjoint(A):
    """Return the adjoint (transpose of cofactor matrix)."""
    from linalg_core.ops import transpose
    return transpose(cofactor_matrix(A))


def inverse_adjoint(A):
    """Compute A⁻¹ = (1/det(A)) * adj(A)."""
    from linalg_core.ops import scalar_mul
    d = det_cofactor(A)
    if abs(d) < EPSILON:
        raise ValueError("Matrix is singular — no inverse exists")
    adj = adjoint(A)
    return scalar_mul(adj, 1.0 / d)


def cramers_rule(A, b):
    """Solve Ax = b using Cramer's Rule.

    A is an n×n Matrix, b is a list of n floats.
    Returns solution as a list.
    """
    if A.rows != A.cols:
        raise ValueError("Cramer's Rule requires a square coefficient matrix")
    n = A.rows
    det_A = det_elimination(A)
    if abs(det_A) < EPSILON:
        raise ValueError("System has no unique solution (det = 0)")

    solution = []
    for i in range(n):
        Ai = A.copy()
        for r in range(n):
            Ai[r, i] = b[r]
        solution.append(det_elimination(Ai) / det_A)
    return solution
