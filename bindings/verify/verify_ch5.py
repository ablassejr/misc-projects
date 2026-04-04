"""Verify Ch.5 inner product spaces against NumPy."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import ctypes
from linalgcore import CMatrix, _lib, _LAMatrix

_lib.la_dot.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]
_lib.la_dot.restype = ctypes.c_double
_lib.la_norm.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
_lib.la_norm.restype = ctypes.c_double
_lib.la_cross_product.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
_lib.la_cross_product.restype = None
_lib.la_gram_schmidt.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
_lib.la_gram_schmidt.restype = None
_lib.la_least_squares.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
_lib.la_least_squares.restype = ctypes.c_int

passed = 0
failed = 0

def check(name, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name}")

print("=== Chapter 5: Inner Product Spaces ===\n")

u = (ctypes.c_double * 3)(1, 2, 3)
v = (ctypes.c_double * 3)(4, 5, 6)
c_dot = _lib.la_dot(u, v, 3)
np_dot = np.dot([1,2,3], [4,5,6])
check("Dot product matches NumPy", abs(c_dot - np_dot) < 1e-9)

c_norm = _lib.la_norm(u, 3)
np_norm = np.linalg.norm([1,2,3])
check("Norm matches NumPy", abs(c_norm - np_norm) < 1e-9)

a = (ctypes.c_double * 3)(1, 0, 0)
b = (ctypes.c_double * 3)(0, 1, 0)
cross = (ctypes.c_double * 3)()
_lib.la_cross_product(a, b, cross)
np_cross = np.cross([1,0,0], [0,1,0])
check("Cross product matches NumPy", all(abs(cross[i] - np_cross[i]) < 1e-9 for i in range(3)))

vecs = (ctypes.c_double * 9)(1,1,0, 1,0,1, 0,1,1)
result = (ctypes.c_double * 9)()
_lib.la_gram_schmidt(vecs, result, 3, 3)
orth_vecs = [np.array([result[i*3+j] for j in range(3)]) for i in range(3)]
for i in range(3):
    check(f"GS vector {i} unit norm", abs(np.linalg.norm(orth_vecs[i]) - 1.0) < 1e-6)
for i in range(3):
    for j in range(i+1, 3):
        check(f"GS vectors {i},{j} orthogonal", abs(np.dot(orth_vecs[i], orth_vecs[j])) < 1e-6)

A = CMatrix(4, 2, [1,1, 1,2, 1,3, 1,4])
b_ls = (ctypes.c_double * 4)(1, 2, 1.5, 3.5)
x_ls = (ctypes.c_double * 2)()
rc = _lib.la_least_squares(A.ptr, b_ls, x_ls)
check("Least squares succeeds", rc == 0)

A_np = np.array([[1,1],[1,2],[1,3],[1,4]], dtype=float)
b_np = np.array([1, 2, 1.5, 3.5])
x_np, _, _, _ = np.linalg.lstsq(A_np, b_np, rcond=None)
check("Least squares matches NumPy", all(abs(x_ls[i] - x_np[i]) < 1e-6 for i in range(2)))

residual = A_np @ np.array([x_ls[0], x_ls[1]]) - b_np
check("Residual orthogonal to column space", abs(A_np.T @ residual).max() < 1e-6)

print(f"\n{passed}/{passed+failed} passed")
sys.exit(0 if failed == 0 else 1)
