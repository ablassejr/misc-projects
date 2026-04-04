"""Rank Explorer — interactive demonstration of rank, nullity, and fundamental subspaces."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bindings'))

import ctypes
from linalgcore import CMatrix, _lib, _LAMatrix

_lib.la_rank.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_rank.restype = ctypes.c_int
_lib.la_nullity.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_nullity.restype = ctypes.c_int
_lib.la_null_space.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(ctypes.POINTER(_LAMatrix))]
_lib.la_null_space.restype = ctypes.c_int
_lib.la_column_space.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(ctypes.POINTER(_LAMatrix))]
_lib.la_column_space.restype = ctypes.c_int
_lib.la_row_space.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(ctypes.POINTER(_LAMatrix))]
_lib.la_row_space.restype = ctypes.c_int


def print_basis(name, ptr, rows, cols):
    if not ptr or cols == 0:
        print(f"  {name}: (empty)")
        return
    print(f"  {name} ({cols} vector{'s' if cols > 1 else ''}):")
    for c in range(cols):
        vec = [_lib.la_matrix_get(ptr, r, c) for r in range(rows)]
        print(f"    [{', '.join(f'{v:6.2f}' for v in vec)}]")


def print_row_basis(name, ptr, rows, cols):
    if not ptr or rows == 0:
        print(f"  {name}: (empty)")
        return
    print(f"  {name} ({rows} vector{'s' if rows > 1 else ''}):")
    for r in range(rows):
        vec = [_lib.la_matrix_get(ptr, r, c) for c in range(cols)]
        print(f"    [{', '.join(f'{v:6.2f}' for v in vec)}]")


def analyze(name, data, rows, cols):
    A = CMatrix(rows, cols, data)
    r = _lib.la_rank(A.ptr)
    n = _lib.la_nullity(A.ptr)

    print(f"\n{'='*50}")
    print(f"Matrix: {name} ({rows}x{cols})")
    for i in range(rows):
        row = [A[i, j] for j in range(cols)]
        print(f"  [{', '.join(f'{v:6.2f}' for v in row)}]")
    print(f"\n  rank = {r}, nullity = {n}, rank + nullity = {r+n} = cols({cols})")

    cs_ptr = ctypes.POINTER(_LAMatrix)()
    cs_dim = _lib.la_column_space(A.ptr, ctypes.byref(cs_ptr))
    print_basis("Column space", cs_ptr, rows, cs_dim)
    if cs_ptr:
        _lib.la_matrix_free(cs_ptr)

    rs_ptr = ctypes.POINTER(_LAMatrix)()
    rs_dim = _lib.la_row_space(A.ptr, ctypes.byref(rs_ptr))
    if rs_ptr:
        print_row_basis("Row space", rs_ptr, rs_dim, cols)
        _lib.la_matrix_free(rs_ptr)

    ns_ptr = ctypes.POINTER(_LAMatrix)()
    ns_dim = _lib.la_null_space(A.ptr, ctypes.byref(ns_ptr))
    print_basis("Null space", ns_ptr, cols, ns_dim)
    if ns_ptr and ns_dim > 0:
        _lib.la_matrix_free(ns_ptr)


if __name__ == '__main__':
    print("=== Rank Explorer ===")

    analyze("Full rank 3x3", [2,1,1, 4,3,3, 8,7,9], 3, 3)
    analyze("Rank-deficient 3x3", [1,2,3, 4,5,6, 7,8,9], 3, 3)
    analyze("Wide 2x4", [1,2,0,1, 0,0,1,1], 2, 4)
    analyze("Tall 4x2", [1,0, 0,1, 1,1, 2,1], 4, 2)

    print(f"\n{'='*50}")
    print("All demonstrations complete!")
