"""Verify Ch.4 vector spaces against NumPy."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import ctypes
from linalgcore import CMatrix, _lib, _LAMatrix

_lib.la_rank.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_rank.restype = ctypes.c_int
_lib.la_nullity.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_nullity.restype = ctypes.c_int
_lib.la_null_space.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(ctypes.POINTER(_LAMatrix))]
_lib.la_null_space.restype = ctypes.c_int
_lib.la_is_independent.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
_lib.la_is_independent.restype = ctypes.c_int

def ptr_to_np(ptr, rows, cols):
    return np.array([[_lib.la_matrix_get(ptr, i, j) for j in range(cols)] for i in range(rows)])

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

print("=== Chapter 4: Vector Spaces ===\n")

A = CMatrix(3, 4, [1,2,0,1, 0,0,1,1, 1,2,1,2])
A_np = np.array([[1,2,0,1],[0,0,1,1],[1,2,1,2]], dtype=float)

c_rank = _lib.la_rank(A.ptr)
np_rank = np.linalg.matrix_rank(A_np)
check("Rank matches NumPy", c_rank == np_rank)

c_nullity = _lib.la_nullity(A.ptr)
check("Rank-nullity theorem", c_rank + c_nullity == 4)

ns_ptr = ctypes.POINTER(_LAMatrix)()
ns_dim = _lib.la_null_space(A.ptr, ctypes.byref(ns_ptr))
check("Null space dimension = nullity", ns_dim == c_nullity)

if ns_dim > 0:
    ns = ptr_to_np(ns_ptr, 4, ns_dim)
    residuals = A_np @ ns
    check("Null space vectors satisfy Ax=0", np.allclose(residuals, 0, atol=1e-6))
    _lib.la_matrix_free(ns_ptr)

I3 = CMatrix(3, 3, [1,0,0, 0,1,0, 0,0,1])
check("Full rank identity", _lib.la_rank(I3.ptr) == 3)

S = CMatrix(3, 3, [1,2,3, 4,5,6, 7,8,9])
check("Rank-deficient 3x3", _lib.la_rank(S.ptr) == 2)

vecs_indep = (ctypes.c_double * 9)(1,0,0, 0,1,0, 0,0,1)
check("Standard basis independent", _lib.la_is_independent(vecs_indep, 3, 3) == 1)

vecs_dep = (ctypes.c_double * 9)(1,2,3, 4,5,6, 5,7,9)
check("Dependent vectors detected", _lib.la_is_independent(vecs_dep, 3, 3) == 0)

print(f"\n{passed}/{passed+failed} passed")
sys.exit(0 if failed == 0 else 1)
