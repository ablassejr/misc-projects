"""Verify Ch.1 elimination against NumPy."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import ctypes
from linalgcore import CMatrix, _lib, _LAMatrix

_lib.la_solve.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(ctypes.c_double)]
_lib.la_solve.restype = ctypes.c_int

def c_solve(A_lists, b_list):
    rows = len(A_lists)
    cols = len(A_lists[0])
    aug_data = []
    for i, row in enumerate(A_lists):
        aug_data.extend(row)
        aug_data.append(b_list[i])
    m = CMatrix(rows, cols + 1, aug_data)
    result = (ctypes.c_double * cols)()
    sol_type = _lib.la_solve(m.ptr, result)
    if sol_type == 0:
        return 0, list(result)
    return sol_type, None

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

print("=== Chapter 1: Systems of Linear Equations ===\n")

A = [[1,1,2],[2,4,-3],[3,6,-5]]
b = [9,1,0]
sol_type, sol = c_solve(A, b)
np_sol = np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float))
check("Unique 3x3 type", sol_type == 0)
check("Unique 3x3 matches NumPy", all(abs(s - n) < 1e-6 for s, n in zip(sol, np_sol)))
residual = np.array(A) @ np.array(sol) - np.array(b)
check("Unique 3x3 residual < epsilon", np.linalg.norm(residual) < 1e-6)

sol_type2, _ = c_solve([[1,1,1],[0,1,1],[0,0,0]], [2,1,3])
check("Inconsistent detected", sol_type2 == -1)

sol_type3, _ = c_solve([[1,2],[2,4]], [3,6])
check("Infinite detected", sol_type3 == 1)

sol_type4, _ = c_solve([[1,2,3],[4,5,6],[7,8,9]], [0,0,0])
check("Homogeneous infinite", sol_type4 == 1)

print(f"\n{passed}/{passed+failed} passed")
sys.exit(0 if failed == 0 else 1)
