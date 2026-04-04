"""Geometry Engine — triangle area, collinearity, tetrahedron volume via determinants."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bindings'))

import ctypes
from linalgcore import CMatrix, _lib, _LAMatrix

_lib.la_det_cofactor.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_det_cofactor.restype = ctypes.c_double


def triangle_area(p1, p2, p3):
    mat = CMatrix(3, 3, [
        p1[0], p1[1], 1,
        p2[0], p2[1], 1,
        p3[0], p3[1], 1,
    ])
    return abs(_lib.la_det_cofactor(mat.ptr)) / 2.0


def are_collinear(p1, p2, p3, tol=1e-9):
    return triangle_area(p1, p2, p3) < tol


def tetrahedron_volume(p1, p2, p3, p4):
    mat = CMatrix(4, 4, [
        p1[0], p1[1], p1[2], 1,
        p2[0], p2[1], p2[2], 1,
        p3[0], p3[1], p3[2], 1,
        p4[0], p4[1], p4[2], 1,
    ])
    return abs(_lib.la_det_cofactor(mat.ptr)) / 6.0


if __name__ == '__main__':
    print("=== Geometry Engine (Determinant Applications) ===\n")

    A, B, C = (0, 0), (4, 0), (0, 3)
    area = triangle_area(A, B, C)
    print(f"Triangle ({A}, {B}, {C})")
    print(f"  Area = {area:.4f} (expected 6.0)")
    assert abs(area - 6.0) < 1e-9

    P1, P2, P3 = (1, 2), (3, 6), (5, 10)
    print(f"\nPoints {P1}, {P2}, {P3}")
    print(f"  Collinear? {are_collinear(P1, P2, P3)} (expected True)")
    assert are_collinear(P1, P2, P3)

    P4, P5, P6 = (1, 2), (3, 6), (5, 11)
    print(f"\nPoints {P4}, {P5}, {P6}")
    print(f"  Collinear? {are_collinear(P4, P5, P6)} (expected False)")
    assert not are_collinear(P4, P5, P6)

    T1, T2, T3, T4 = (0,0,0), (1,0,0), (0,1,0), (0,0,1)
    vol = tetrahedron_volume(T1, T2, T3, T4)
    print(f"\nTetrahedron ({T1}, {T2}, {T3}, {T4})")
    print(f"  Volume = {vol:.4f} (expected {1/6:.4f})")
    assert abs(vol - 1.0/6.0) < 1e-9

    print("\nAll geometry checks passed!")
