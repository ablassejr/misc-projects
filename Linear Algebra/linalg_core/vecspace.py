"""Vector space algorithms — Chapter 4.

Rank, nullity, null space, column space, row space, change of basis.
Functions are added progressively as notebooks are completed.
"""

from linalg_core.matrix import Matrix
from linalg_core import EPSILON


# --- Notebook 4.4: Linear independence and span ---

def is_independent(vectors):
    """Test if a list of column vectors (each a list of floats) is linearly independent.

    Stacks vectors as columns, reduces to RREF, checks if every column is a pivot column.
    Returns (independent: bool, dependency: list or None).
    """
    from linalg_core.elimination import to_rref

    if not vectors:
        return True, None

    n = len(vectors[0])
    k = len(vectors)

    A = Matrix(n, k)
    for j, v in enumerate(vectors):
        for i in range(n):
            A[i, j] = v[i]

    m = A.copy()
    pivot_positions = to_rref(m)
    pivot_cols = {col for _, col in pivot_positions}

    if len(pivot_cols) == k:
        return True, None

    free_cols = [j for j in range(k) if j not in pivot_cols]
    first_free = free_cols[0]
    dep = [0.0] * k
    dep[first_free] = 1.0
    for row, col in pivot_positions:
        dep[col] = -m[row, first_free]
    return False, dep


def is_in_span(v, vectors):
    """Test if vector v is in the span of the given vectors.

    Returns (in_span: bool, coefficients: list or None).
    """
    from linalg_core.elimination import solve

    if not vectors:
        return all(abs(x) < EPSILON for x in v), None

    n = len(v)
    k = len(vectors)

    aug = Matrix(n, k + 1)
    for j, vec in enumerate(vectors):
        for i in range(n):
            aug[i, j] = vec[i]
    for i in range(n):
        aug[i, k] = v[i]

    sol_type, result = solve(aug)
    if sol_type == "inconsistent":
        return False, None
    if sol_type == "unique":
        return True, result
    return True, result["particular"]


# --- Notebook 4.6: Rank, nullity, fundamental subspaces ---

def rank(A):
    """Return the rank of A (number of pivot positions in RREF)."""
    from linalg_core.elimination import to_rref

    m = A.copy()
    pivot_positions = to_rref(m)
    return len(pivot_positions)


def nullity(A):
    """Return the nullity of A (number of free variables = cols - rank)."""
    return A.cols - rank(A)


def null_space(A):
    """Return a basis for the null space of A as a list of vectors (lists).

    Each basis vector corresponds to one free variable.
    """
    from linalg_core.elimination import to_rref

    m = A.copy()
    pivot_positions = to_rref(m)
    pivot_cols = {col for _, col in pivot_positions}
    n_vars = A.cols
    free_vars = [j for j in range(n_vars) if j not in pivot_cols]

    basis = []
    for fv in free_vars:
        vec = [0.0] * n_vars
        vec[fv] = 1.0
        for row, col in pivot_positions:
            vec[col] = -m[row, fv]
        basis.append(vec)
    return basis


def column_space(A):
    """Return a basis for the column space of A.

    Returns the original columns of A corresponding to pivot positions.
    """
    from linalg_core.elimination import to_rref

    m = A.copy()
    pivot_positions = to_rref(m)
    pivot_cols = sorted(col for _, col in pivot_positions)

    basis = []
    for col in pivot_cols:
        basis.append(A.get_col(col))
    return basis


def row_space(A):
    """Return a basis for the row space of A.

    Returns the nonzero rows of the RREF.
    """
    from linalg_core.elimination import to_rref

    m = A.copy()
    pivot_positions = to_rref(m)

    basis = []
    for row, _ in pivot_positions:
        basis.append(m.get_row(row))
    return basis


# --- Notebook 4.7: Coordinates and change of basis ---

def coordinate_vector(x, basis):
    """Find the coordinate vector [x]_B of x relative to basis B.

    x is a list, basis is a list of lists. Returns coordinate list.
    """
    from linalg_core.elimination import solve

    n = len(x)
    k = len(basis)

    aug = Matrix(n, k + 1)
    for j, bvec in enumerate(basis):
        for i in range(n):
            aug[i, j] = bvec[i]
    for i in range(n):
        aug[i, k] = x[i]

    sol_type, result = solve(aug)
    if sol_type != "unique":
        raise ValueError("Vector cannot be uniquely represented in this basis")
    return result


def change_of_basis(old_basis, new_basis):
    """Compute the transition matrix from old_basis to new_basis.

    Both are lists of lists. Returns a Matrix P such that [x]_new = P @ [x]_old.
    """
    n = len(old_basis)
    cols = []
    for bvec in old_basis:
        coords = coordinate_vector(bvec, new_basis)
        cols.append(coords)

    P = Matrix(n, n)
    for j, col in enumerate(cols):
        for i in range(n):
            P[i, j] = col[i]
    return P
