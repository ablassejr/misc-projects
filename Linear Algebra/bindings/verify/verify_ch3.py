"""Verify Ch.3 determinants against NumPy."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import ctypes
from linalgcore import CMatrix, _lib, _LAMatrix

_lib.la_det_cofactor.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_det_cofactor.restype = ctypes.c_double
_lib.la_det_elimination.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_det_elimination.restype = ctypes.c_double
_lib.la_adjoint.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_adjoint.restype = ctypes.POINTER(_LAMatrix)
_lib.la_inverse_adjoint.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_inverse_adjoint.restype = ctypes.POINTER(_LAMatrix)
_lib.la_matrix_inverse.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_inverse.restype = ctypes.POINTER(_LAMatrix)
_lib.la_cramers_rule.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
_lib.la_cramers_rule.restype = ctypes.c_int

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

print("=== Chapter 3: Determinants ===\n")

A = CMatrix(3, 3, [2,1,1,4,3,3,8,7,9])
A_np = np.array([[2,1,1],[4,3,3],[8,7,9]], dtype=float)

det_cof = _lib.la_det_cofactor(A.ptr)
det_elim = _lib.la_det_elimination(A.ptr)
det_np = np.linalg.det(A_np)
check("Cofactor det matches NumPy", abs(det_cof - det_np) < 1e-6)
check("Elimination det matches NumPy", abs(det_elim - det_np) < 1e-6)
check("Both methods agree", abs(det_cof - det_elim) < 1e-9)

inv_adj_ptr = _lib.la_inverse_adjoint(A.ptr)
inv_gj_ptr = _lib.la_matrix_inverse(A.ptr)
inv_adj = ptr_to_np(inv_adj_ptr, 3, 3)
inv_gj = ptr_to_np(inv_gj_ptr, 3, 3)
check("Adjoint inverse matches Gauss-Jordan", np.allclose(inv_adj, inv_gj, atol=1e-6))
_lib.la_matrix_free(inv_adj_ptr)
_lib.la_matrix_free(inv_gj_ptr)

b = (ctypes.c_double * 3)(9.0, 1.0, 0.0)
result = (ctypes.c_double * 3)()
A2 = CMatrix(3, 3, [1,1,2,2,4,-3,3,6,-5])
rc = _lib.la_cramers_rule(A2.ptr, b, result)
np_sol = np.linalg.solve(np.array([[1,1,2],[2,4,-3],[3,6,-5]], dtype=float), [9,1,0])
check("Cramer's rule succeeds", rc == 0)
check("Cramer's matches NumPy solve", all(abs(result[i] - np_sol[i]) < 1e-6 for i in range(3)))

S = CMatrix(3, 3, [1,2,3,4,5,6,7,8,9])
det_s = _lib.la_det_elimination(S.ptr)
check("Singular det ≈ 0", abs(det_s) < 1e-6)

print(f"\n{passed}/{passed+failed} passed")
sys.exit(0 if failed == 0 else 1)
