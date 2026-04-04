"""Polynomial Regression — least squares fitting degrees 1-5 via C engine."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bindings'))

import ctypes
import math
from linalgcore import CMatrix, _lib, _LAMatrix

_lib.la_least_squares.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
_lib.la_least_squares.restype = ctypes.c_int


def poly_regression(x_data, y_data, degree):
    m = len(x_data)
    n = degree + 1

    A_data = []
    for xi in x_data:
        for d in range(n):
            A_data.append(xi ** d)

    A = CMatrix(m, n, A_data)
    b = (ctypes.c_double * m)(*y_data)
    result = (ctypes.c_double * n)()

    rc = _lib.la_least_squares(A.ptr, b, result)
    if rc != 0:
        return None
    return list(result)


def evaluate_poly(coeffs, x):
    return sum(c * x**i for i, c in enumerate(coeffs))


def rmse(x_data, y_data, coeffs):
    n = len(x_data)
    ss = sum((y_data[i] - evaluate_poly(coeffs, x_data[i]))**2 for i in range(n))
    return math.sqrt(ss / n)


if __name__ == '__main__':
    print("=== Polynomial Regression via Least Squares ===\n")

    x = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    y = [1.0, 1.8, 3.2, 4.5, 3.9, 3.1, 2.0, 1.5, 1.2]

    print(f"Data points: {len(x)}")
    print(f"x = {x}")
    print(f"y = {y}")

    for deg in range(1, 6):
        coeffs = poly_regression(x, y, deg)
        if coeffs is None:
            print(f"\n  Degree {deg}: Failed (singular normal equations)")
            continue

        err = rmse(x, y, coeffs)
        terms = []
        for i, c in enumerate(coeffs):
            if i == 0:
                terms.append(f"{c:.4f}")
            elif i == 1:
                terms.append(f"{c:+.4f}x")
            else:
                terms.append(f"{c:+.4f}x^{i}")
        poly_str = " ".join(terms)

        print(f"\n  Degree {deg}: y = {poly_str}")
        print(f"  RMSE = {err:.6f}")

    deg3 = poly_regression(x, y, 3)
    if deg3:
        print(f"\nBest fit (degree 3) predictions:")
        for xi in [0.25, 1.75, 3.25]:
            yi = evaluate_poly(deg3, xi)
            print(f"  f({xi}) = {yi:.4f}")

    print("\nRegression complete!")
