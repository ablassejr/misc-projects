"""Elimination algorithms — Chapter 1.

Row operations, Gaussian elimination, Gauss-Jordan, system solving.
Functions are added progressively as notebooks are completed.
"""

from linalg_core.matrix import Matrix
from linalg_core import EPSILON


# --- Notebook 1.1: Row operations and forward elimination ---

def swap_rows(m, i, j):
    """Swap rows i and j in-place."""
    for k in range(m.cols):
        m[i, k], m[j, k] = m[j, k], m[i, k]


def scale_row(m, i, scalar):
    """Multiply row i by scalar in-place."""
    for k in range(m.cols):
        m[i, k] = m[i, k] * scalar


def add_scaled_row(m, target, source, scalar):
    """Add scalar * row[source] to row[target] in-place."""
    for k in range(m.cols):
        m[target, k] = m[target, k] + scalar * m[source, k]


def forward_eliminate(m, verbose=False):
    """Reduce matrix to row-echelon form (REF) using forward elimination.

    Uses partial pivoting. Operates in-place. Returns the number of row swaps.
    """
    swaps = 0
    pivot_row = 0
    for col in range(m.cols):
        if pivot_row >= m.rows:
            break

        best = pivot_row
        for r in range(pivot_row + 1, m.rows):
            if abs(m[r, col]) > abs(m[best, col]):
                best = r

        if abs(m[best, col]) < EPSILON:
            continue

        if best != pivot_row:
            swap_rows(m, pivot_row, best)
            swaps += 1
            if verbose:
                print(f"Swap R{pivot_row+1} <-> R{best+1}")
                print(m)

        pivot_val = m[pivot_row, col]
        scale_row(m, pivot_row, 1.0 / pivot_val)
        if verbose:
            print(f"Scale R{pivot_row+1} by 1/{pivot_val:.4f}")
            print(m)

        for r in range(pivot_row + 1, m.rows):
            if abs(m[r, col]) > EPSILON:
                factor = -m[r, col]
                add_scaled_row(m, r, pivot_row, factor)
                if verbose:
                    print(f"R{r+1} += {factor:.4f} * R{pivot_row+1}")
                    print(m)

        pivot_row += 1

    return swaps


def back_substitute(ref_matrix):
    """Back-substitute from a row-echelon form augmented matrix.

    Returns (solution_type, result) where:
    - ("unique", [values]) for a unique solution
    - ("infinite", {free_vars, parametric}) for infinitely many solutions
    - ("inconsistent", None) if no solution exists
    """
    m = ref_matrix.copy()
    rows, cols = m.rows, m.cols
    n_vars = cols - 1

    pivots = {}
    for i in range(rows):
        for j in range(n_vars):
            if abs(m[i, j]) > EPSILON:
                pivots[i] = j
                break
        else:
            if abs(m[i, cols - 1]) > EPSILON:
                return ("inconsistent", None)

    pivot_cols = set(pivots.values())
    free_vars = [j for j in range(n_vars) if j not in pivot_cols]

    if not free_vars:
        solution = [0.0] * n_vars
        pivot_rows = sorted(pivots.keys(), reverse=True)
        for i in pivot_rows:
            j = pivots[i]
            val = m[i, cols - 1]
            for k in range(j + 1, n_vars):
                val -= m[i, k] * solution[k]
            solution[j] = val
        return ("unique", solution)

    parametric = {}
    for fv in free_vars:
        parametric[fv] = f"t{free_vars.index(fv) + 1}"

    particular = [0.0] * n_vars
    coefficients = {fv: [0.0] * n_vars for fv in free_vars}

    for fv in free_vars:
        coefficients[fv][fv] = 1.0

    pivot_rows = sorted(pivots.keys(), reverse=True)
    for i in pivot_rows:
        j = pivots[i]
        particular[j] = m[i, cols - 1]
        for k in range(j + 1, n_vars):
            if k in free_vars:
                for fv in free_vars:
                    if k == fv:
                        coefficients[fv][j] -= m[i, k]
            else:
                particular[j] -= m[i, k] * particular[k]
                for fv in free_vars:
                    coefficients[fv][j] -= m[i, k] * coefficients[fv][k]

    return ("infinite", {
        "free_vars": free_vars,
        "parametric_names": parametric,
        "particular": particular,
        "coefficients": coefficients,
    })


def solve_system(augmented):
    """Solve a system given its augmented matrix [A|b].

    Returns (solution_type, result).
    """
    m = augmented.copy()
    forward_eliminate(m)
    return back_substitute(m)


# --- Notebook 1.2: Gaussian and Gauss-Jordan elimination ---

def find_pivot(m, col, start_row):
    """Find the row with the largest absolute value in column col, from start_row down.

    Returns the row index, or -1 if the column is all zeros below start_row.
    """
    best = -1
    best_val = EPSILON
    for r in range(start_row, m.rows):
        if abs(m[r, col]) > best_val:
            best_val = abs(m[r, col])
            best = r
    return best


def to_ref(m, verbose=False):
    """Reduce matrix to row-echelon form (REF) with partial pivoting.

    Operates in-place. Returns (pivot_positions, num_swaps) where
    pivot_positions is a list of (row, col) tuples.
    """
    swaps = 0
    pivot_positions = []
    pivot_row = 0

    for col in range(m.cols):
        if pivot_row >= m.rows:
            break

        best = find_pivot(m, col, pivot_row)
        if best == -1:
            continue

        if best != pivot_row:
            swap_rows(m, pivot_row, best)
            swaps += 1
            if verbose:
                print(f"Swap R{pivot_row+1} <-> R{best+1}")
                print(m)

        pivot_val = m[pivot_row, col]
        scale_row(m, pivot_row, 1.0 / pivot_val)
        if verbose:
            print(f"Scale R{pivot_row+1} by 1/{pivot_val:.4f}")
            print(m)

        for r in range(pivot_row + 1, m.rows):
            if abs(m[r, col]) > EPSILON:
                factor = -m[r, col]
                add_scaled_row(m, r, pivot_row, factor)
                if verbose:
                    print(f"R{r+1} += {factor:.4f} * R{pivot_row+1}")
                    print(m)

        pivot_positions.append((pivot_row, col))
        pivot_row += 1

    return pivot_positions, swaps


def to_rref(m, verbose=False):
    """Reduce matrix to reduced row-echelon form (RREF).

    Operates in-place. Returns pivot_positions.
    """
    pivot_positions, swaps = to_ref(m, verbose=verbose)

    for pivot_row, pivot_col in reversed(pivot_positions):
        for r in range(pivot_row - 1, -1, -1):
            if abs(m[r, pivot_col]) > EPSILON:
                factor = -m[r, pivot_col]
                add_scaled_row(m, r, pivot_row, factor)
                if verbose:
                    print(f"R{r+1} += {factor:.4f} * R{pivot_row+1}")
                    print(m)

    return pivot_positions


def solve(augmented, verbose=False):
    """Solve a linear system using RREF.

    Takes an augmented matrix [A|b]. Returns (solution_type, result) where:
    - ("unique", [values]) for a unique solution
    - ("infinite", {free_vars, particular, directions}) for infinitely many
    - ("inconsistent", None) if no solution exists
    """
    m = augmented.copy()
    pivot_positions = to_rref(m, verbose=verbose)
    n_vars = m.cols - 1

    pivot_cols = {col for _, col in pivot_positions}

    for row, col in pivot_positions:
        if col >= n_vars:
            return ("inconsistent", None)

    for i in range(m.rows):
        is_zero_row = all(abs(m[i, j]) < EPSILON for j in range(n_vars))
        if is_zero_row and abs(m[i, n_vars]) > EPSILON:
            return ("inconsistent", None)

    free_vars = [j for j in range(n_vars) if j not in pivot_cols]

    if not free_vars:
        solution = [0.0] * n_vars
        for row, col in pivot_positions:
            solution[col] = m[row, n_vars]
        return ("unique", solution)

    particular = [0.0] * n_vars
    directions = {fv: [0.0] * n_vars for fv in free_vars}

    for fv in free_vars:
        directions[fv][fv] = 1.0

    for row, col in pivot_positions:
        particular[col] = m[row, n_vars]
        for fv in free_vars:
            directions[fv][col] = -m[row, fv]

    return ("infinite", {
        "free_vars": free_vars,
        "particular": particular,
        "directions": directions,
    })
