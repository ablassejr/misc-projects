"""Matrix operations — Chapter 2.

Addition, multiplication, transpose, inverse, LU factorization.
Functions are added progressively as notebooks are completed.
"""

from linalg_core.matrix import Matrix
from linalg_core import EPSILON


# --- Notebook 2.1: Basic operations ---

def add(A, B):
    """Return A + B."""
    if A.rows != B.rows or A.cols != B.cols:
        raise ValueError(f"Dimension mismatch: {A.rows}x{A.cols} vs {B.rows}x{B.cols}")
    data = [a + b for a, b in zip(A.data, B.data)]
    return Matrix(A.rows, A.cols, data)


def scalar_mul(A, s):
    """Return s * A."""
    data = [s * x for x in A.data]
    return Matrix(A.rows, A.cols, data)


def multiply(A, B):
    """Return A * B using row-column dot products."""
    if A.cols != B.rows:
        raise ValueError(f"Cannot multiply {A.rows}x{A.cols} by {B.rows}x{B.cols}")
    result = Matrix(A.rows, B.cols)
    for i in range(A.rows):
        for j in range(B.cols):
            s = 0.0
            for k in range(A.cols):
                s += A[i, k] * B[k, j]
            result[i, j] = s
    return result


def transpose(A):
    """Return A^T."""
    result = Matrix(A.cols, A.rows)
    for i in range(A.rows):
        for j in range(A.cols):
            result[j, i] = A[i, j]
    return result


# --- Notebook 2.3: Inverse ---

def inverse(A):
    """Compute A⁻¹ using Gauss-Jordan elimination on [A | I].

    Raises ValueError if A is singular.
    """
    from linalg_core.elimination import to_rref

    if A.rows != A.cols:
        raise ValueError("Only square matrices can be inverted")
    n = A.rows

    aug = Matrix(n, 2 * n)
    for i in range(n):
        for j in range(n):
            aug[i, j] = A[i, j]
        aug[i, n + i] = 1.0

    to_rref(aug)

    for i in range(n):
        if abs(aug[i, i] - 1.0) > EPSILON:
            raise ValueError("Matrix is singular — no inverse exists")

    result = Matrix(n, n)
    for i in range(n):
        for j in range(n):
            result[i, j] = aug[i, n + j]
    return result


# --- Notebook 2.4: Elementary matrices and LU factorization ---

def elementary_swap(n, i, j):
    """Return the n×n elementary matrix that swaps rows i and j."""
    E = Matrix.identity(n)
    E[i, i] = 0.0
    E[j, j] = 0.0
    E[i, j] = 1.0
    E[j, i] = 1.0
    return E


def elementary_scale(n, i, c):
    """Return the n×n elementary matrix that scales row i by c."""
    E = Matrix.identity(n)
    E[i, i] = c
    return E


def elementary_add(n, target, source, c):
    """Return the n×n elementary matrix that adds c * row[source] to row[target]."""
    E = Matrix.identity(n)
    E[target, source] = c
    return E


def lu_factorize(A):
    """LU factorization without pivoting (Doolittle's method).

    Returns (L, U) where A = L * U, L is lower triangular with 1s on diagonal,
    U is upper triangular.
    Raises ValueError if a zero pivot is encountered.
    """
    if A.rows != A.cols:
        raise ValueError("LU factorization requires a square matrix")
    n = A.rows
    L = Matrix.identity(n)
    U = A.copy()

    for col in range(n):
        if abs(U[col, col]) < EPSILON:
            raise ValueError(f"Zero pivot at position ({col},{col}) — LU without pivoting fails")
        for row in range(col + 1, n):
            factor = U[row, col] / U[col, col]
            L[row, col] = factor
            for k in range(col, n):
                U[row, k] = U[row, k] - factor * U[col, k]

    return L, U


def forward_sub(L, b):
    """Solve Ly = b by forward substitution where L is lower triangular.

    b is a list of floats. Returns y as a list.
    """
    n = L.rows
    y = [0.0] * n
    for i in range(n):
        s = b[i]
        for j in range(i):
            s -= L[i, j] * y[j]
        y[i] = s / L[i, i]
    return y


def back_sub(U, y):
    """Solve Ux = y by back substitution where U is upper triangular.

    y is a list of floats. Returns x as a list.
    """
    n = U.rows
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = y[i]
        for j in range(i + 1, n):
            s -= U[i, j] * x[j]
        x[i] = s / U[i, i]
    return x
