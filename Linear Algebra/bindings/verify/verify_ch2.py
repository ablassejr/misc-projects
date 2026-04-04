"""Verify Ch.2 matrix operations against NumPy."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import ctypes
from linalgcore import CMatrix, _lib, _LAMatrix

_lib.la_matrix_add.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_add.restype = ctypes.POINTER(_LAMatrix)
_lib.la_matrix_mul.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_mul.restype = ctypes.POINTER(_LAMatrix)
_lib.la_matrix_transpose.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_transpose.restype = ctypes.POINTER(_LAMatrix)
_lib.la_matrix_inverse.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_inverse.restype = ctypes.POINTER(_LAMatrix)
_lib.la_matrix_scalar_mul.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.c_double]
_lib.la_matrix_scalar_mul.restype = ctypes.POINTER(_LAMatrix)
_lib.la_lu_factorize.argtypes = [
    ctypes.POINTER(_LAMatrix),
    ctypes.POINTER(ctypes.POINTER(_LAMatrix)),
    ctypes.POINTER(ctypes.POINTER(_LAMatrix))
]
_lib.la_lu_factorize.restype = ctypes.c_int

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

print("=== Chapter 2: Matrix Operations ===\n")

A = CMatrix(2, 3, [1,2,3,4,5,6])
B = CMatrix(2, 3, [7,8,9,10,11,12])
C_ptr = _lib.la_matrix_add(A.ptr, B.ptr)
C_np = np.array([[1,2,3],[4,5,6]]) + np.array([[7,8,9],[10,11,12]])
C_c = ptr_to_np(C_ptr, 2, 3)
check("Addition matches NumPy", np.allclose(C_c, C_np))
_lib.la_matrix_free(C_ptr)

A2 = CMatrix(2, 2, [1,2,3,4])
S_ptr = _lib.la_matrix_scalar_mul(A2.ptr, 3.0)
S_c = ptr_to_np(S_ptr, 2, 2)
check("Scalar mul matches NumPy", np.allclose(S_c, np.array([[3,6],[9,12]])))
_lib.la_matrix_free(S_ptr)

A3 = CMatrix(2, 3, [1,2,3,4,5,6])
B3 = CMatrix(3, 2, [7,8,9,10,11,12])
P_ptr = _lib.la_matrix_mul(A3.ptr, B3.ptr)
P_c = ptr_to_np(P_ptr, 2, 2)
P_np = np.array([[1,2,3],[4,5,6]]) @ np.array([[7,8],[9,10],[11,12]])
check("Multiplication matches NumPy", np.allclose(P_c, P_np))
_lib.la_matrix_free(P_ptr)

T_ptr = _lib.la_matrix_transpose(A3.ptr)
T_c = ptr_to_np(T_ptr, 3, 2)
T_np = np.array([[1,2,3],[4,5,6]]).T
check("Transpose matches NumPy", np.allclose(T_c, T_np))
_lib.la_matrix_free(T_ptr)

M = CMatrix(3, 3, [2,1,1,4,3,3,8,7,9])
Inv_ptr = _lib.la_matrix_inverse(M.ptr)
Inv_c = ptr_to_np(Inv_ptr, 3, 3)
Inv_np = np.linalg.inv(np.array([[2,1,1],[4,3,3],[8,7,9]], dtype=float))
check("Inverse matches NumPy", np.allclose(Inv_c, Inv_np, atol=1e-6))

Prod_ptr = _lib.la_matrix_mul(M.ptr, Inv_ptr)
Prod_c = ptr_to_np(Prod_ptr, 3, 3)
check("A * inv(A) = I", np.allclose(Prod_c, np.eye(3), atol=1e-6))
_lib.la_matrix_free(Inv_ptr)
_lib.la_matrix_free(Prod_ptr)

L_ptr = ctypes.POINTER(_LAMatrix)()
U_ptr = ctypes.POINTER(_LAMatrix)()
rc = _lib.la_lu_factorize(M.ptr, ctypes.byref(L_ptr), ctypes.byref(U_ptr))
check("LU factorization succeeds", rc == 0)
L_c = ptr_to_np(L_ptr, 3, 3)
U_c = ptr_to_np(U_ptr, 3, 3)
LU_product = L_c @ U_c
M_np = np.array([[2,1,1],[4,3,3],[8,7,9]], dtype=float)
check("LU = A", np.allclose(LU_product, M_np, atol=1e-9))
_lib.la_matrix_free(L_ptr)
_lib.la_matrix_free(U_ptr)

AB_ptr = _lib.la_matrix_mul(A3.ptr, B3.ptr)
AB_T_ptr = _lib.la_matrix_transpose(AB_ptr)
BT_ptr = _lib.la_matrix_transpose(B3.ptr)
AT_ptr = _lib.la_matrix_transpose(A3.ptr)
BT_AT_ptr = _lib.la_matrix_mul(BT_ptr, AT_ptr)
AB_T_c = ptr_to_np(AB_T_ptr, 2, 2)
BT_AT_c = ptr_to_np(BT_AT_ptr, 2, 2)
check("(AB)^T = B^T A^T", np.allclose(AB_T_c, BT_AT_c))
_lib.la_matrix_free(AB_ptr)
_lib.la_matrix_free(AB_T_ptr)
_lib.la_matrix_free(BT_ptr)
_lib.la_matrix_free(AT_ptr)
_lib.la_matrix_free(BT_AT_ptr)

print(f"\n{passed}/{passed+failed} passed")
sys.exit(0 if failed == 0 else 1)
