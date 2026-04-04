"""Inner product space algorithms — Chapter 5.

Dot product, norm, Gram-Schmidt, least squares, cross product.
Functions are added progressively as notebooks are completed.
"""

import math

from linalg_core.matrix import Matrix
from linalg_core import EPSILON


# --- Notebook 5.1: Dot product and norm ---

def dot(u, v):
    """Dot product of two vectors (lists of floats)."""
    if len(u) != len(v):
        raise ValueError(f"Dimension mismatch: {len(u)} vs {len(v)}")
    return sum(a * b for a, b in zip(u, v))


def norm(v):
    """Euclidean norm of a vector (list of floats)."""
    return math.sqrt(dot(v, v))


def normalize(v):
    """Return unit vector in the direction of v."""
    n = norm(v)
    if n < EPSILON:
        raise ValueError("Cannot normalize the zero vector")
    return [x / n for x in v]


def distance(u, v):
    """Euclidean distance between two vectors."""
    diff = [a - b for a, b in zip(u, v)]
    return norm(diff)


def angle(u, v):
    """Angle between two vectors in radians."""
    cos_theta = dot(u, v) / (norm(u) * norm(v))
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.acos(cos_theta)


def are_orthogonal(u, v):
    """Test if two vectors are orthogonal."""
    return abs(dot(u, v)) < EPSILON


# --- Notebook 5.3: Gram-Schmidt and projection ---

def orthogonal_projection(v, u):
    """Project v onto u: proj_u(v) = (<v,u>/<u,u>) * u."""
    scale = dot(v, u) / dot(u, u)
    return [scale * x for x in u]


def gram_schmidt(vectors):
    """Gram-Schmidt orthonormalization.

    Takes a list of linearly independent vectors (lists of floats).
    Returns an orthonormal set spanning the same space.
    """
    orthogonal = []

    for v in vectors:
        u = list(v)
        for q in orthogonal:
            proj = orthogonal_projection(u, q)
            u = [a - b for a, b in zip(u, proj)]

        if norm(u) < EPSILON:
            continue
        orthogonal.append(u)

    return [normalize(u) for u in orthogonal]


# --- Notebook 5.4: Least squares ---

def least_squares(A, b):
    """Solve the least-squares problem min ||Ax - b||².

    Solves the normal equations A^T A x = A^T b.
    A is a Matrix, b is a list. Returns x as a list.
    """
    from linalg_core.ops import multiply, transpose as mat_transpose
    from linalg_core.ops import lu_factorize, forward_sub, back_sub

    At = mat_transpose(A)
    AtA = multiply(At, A)

    b_mat = Matrix.from_vector(b)
    Atb_mat = multiply(At, b_mat)
    Atb = [Atb_mat[i, 0] for i in range(Atb_mat.rows)]

    L, U = lu_factorize(AtA)
    y = forward_sub(L, Atb)
    x = back_sub(U, y)
    return x


# --- Notebook 5.5: Cross product ---

def cross_product(u, v):
    """Cross product of two 3D vectors."""
    if len(u) != 3 or len(v) != 3:
        raise ValueError("Cross product is defined for 3D vectors only")
    return [
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    ]
