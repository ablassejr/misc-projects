"""Markov Chain — iterate transition matrix P^k via C engine, show convergence."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bindings'))

import ctypes
from linalgcore import CMatrix, _lib, _LAMatrix

_lib.la_matrix_mul.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_mul.restype = ctypes.POINTER(_LAMatrix)


def matrix_power(mat, k):
    n = mat.rows
    result_data = []
    for i in range(n):
        for j in range(n):
            result_data.append(1.0 if i == j else 0.0)
    result = CMatrix(n, n, result_data)

    base = CMatrix(n, n, [_lib.la_matrix_get(mat.ptr, i, j)
                           for i in range(n) for j in range(n)])

    for _ in range(k):
        new_ptr = _lib.la_matrix_mul(result.ptr, base.ptr)
        new_data = [_lib.la_matrix_get(new_ptr, i, j)
                    for i in range(n) for j in range(n)]
        _lib.la_matrix_free(new_ptr)
        result = CMatrix(n, n, new_data)

    return result


def print_matrix(mat, label=""):
    if label:
        print(f"\n{label}:")
    for i in range(mat.rows):
        row = [f"{mat[i, j]:8.4f}" for j in range(mat.cols)]
        print("  [" + ", ".join(row) + "]")


if __name__ == '__main__':
    P = CMatrix(3, 3, [
        0.7, 0.2, 0.1,
        0.3, 0.4, 0.3,
        0.2, 0.3, 0.5,
    ])

    print("Weather Markov Chain (Sunny/Cloudy/Rainy)")
    print("==========================================")
    print_matrix(P, "Transition matrix P")

    for k in [1, 2, 5, 10, 50]:
        Pk = matrix_power(P, k)
        print_matrix(Pk, f"P^{k}")

    P50 = matrix_power(P, 50)
    steady = [P50[0, j] for j in range(3)]
    print(f"\nSteady state: Sunny={steady[0]:.4f}, Cloudy={steady[1]:.4f}, Rainy={steady[2]:.4f}")

    for j in range(3):
        col_vals = [P50[i, j] for i in range(3)]
        assert max(col_vals) - min(col_vals) < 1e-6, "Rows should converge"
    print("Convergence verified!")
