# Design: Google Colab Notebooks for Elementary Linear Algebra

**Date:** 2026-04-03
**Textbook:** Elementary Linear Algebra, 8th Edition, Ron Larson (Cengage, 2017)
**Scope:** Chapters 1-5 (28 sections)

---

## Summary

28 Google Colab notebooks (one per textbook section) that teach linear algebra theory through a code-first approach. Each notebook poses a motivating problem, builds the algorithm from scratch in pure Python step-by-step, extracts definitions and theorems as they emerge, verifies against NumPy, and ends with auto-graded exercises.

A shared `linalg_core/` Python package in the repo grows progressively as notebooks are completed — each section adds implementations to the corresponding module. NumPy is used exclusively for verification, never for computation.

---

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Platform | Google Colab | Accessible, no local setup, Python-native |
| Granularity | One notebook per section | Focused, digestible sessions |
| Philosophy | From-scratch first, NumPy to verify | Friction is the learning mechanism |
| Teaching flow | Code-first | Motivating problem drives theory extraction |
| Exercises | Auto-graded stubs | Immediate feedback via assert + NumPy cross-check |
| Cross-notebook code | GitHub-backed `linalg_core/` package | Standalone notebooks + growing reference library |
| Relationship to engine | Notebooks = learning; C/C++/TS engine = proof project | Separate concerns |

---

## Notebook Inventory

```
notebooks/
├── ch1_systems/
│   ├── 1.1_intro_to_systems.ipynb
│   ├── 1.2_gaussian_elimination.ipynb
│   └── 1.3_applications_of_systems.ipynb
├── ch2_matrices/
│   ├── 2.1_operations_with_matrices.ipynb
│   ├── 2.2_properties_of_matrix_operations.ipynb
│   ├── 2.3_inverse_of_a_matrix.ipynb
│   ├── 2.4_elementary_matrices.ipynb
│   ├── 2.5_markov_chains.ipynb
│   └── 2.6_applications_of_matrix_operations.ipynb
├── ch3_determinants/
│   ├── 3.1_determinant_of_a_matrix.ipynb
│   ├── 3.2_determinants_and_elementary_operations.ipynb
│   ├── 3.3_properties_of_determinants.ipynb
│   └── 3.4_applications_of_determinants.ipynb
├── ch4_vector_spaces/
│   ├── 4.1_vectors_in_rn.ipynb
│   ├── 4.2_vector_spaces.ipynb
│   ├── 4.3_subspaces.ipynb
│   ├── 4.4_spanning_sets_and_linear_independence.ipynb
│   ├── 4.5_basis_and_dimension.ipynb
│   ├── 4.6_rank_and_systems.ipynb
│   ├── 4.7_coordinates_and_change_of_basis.ipynb
│   └── 4.8_applications_of_vector_spaces.ipynb
├── ch5_inner_product_spaces/
│   ├── 5.1_length_and_dot_product.ipynb
│   ├── 5.2_inner_product_spaces.ipynb
│   ├── 5.3_gram_schmidt_process.ipynb
│   ├── 5.4_least_squares_analysis.ipynb
│   └── 5.5_applications_of_inner_product_spaces.ipynb
```

---

## Shared Package Structure

```
linalg_core/
├── __init__.py
├── matrix.py          # Matrix class, creation, printing, element access
├── elimination.py     # Ch.1: REF, RREF, solve, row operations
├── ops.py             # Ch.2: add, multiply, transpose, inverse, LU
├── determinant.py     # Ch.3: cofactor, elimination-based, adjoint, Cramer's
├── vecspace.py        # Ch.4: rank, nullity, null space, col space, change of basis
└── inner.py           # Ch.5: dot, norm, Gram-Schmidt, least squares, cross product
```

Each notebook starts with:

```python
!git clone https://github.com/<your-repo>/linear-algebra.git 2>/dev/null || true
!pip install -e linear-algebra/ -q

from linalg_core.matrix import Matrix
import numpy as np  # verification only
```

**Rule:** `linalg_core` does the computation. `numpy` only appears in cells labeled `# VERIFY`.

---

## Notebook Internal Flow

Every notebook follows this 7-section template:

### 1. Setup (1-2 cells)
Clone repo, install `linalg_core`, imports.

### 2. Motivation (1-3 cells)
A concrete problem that can't be solved yet. Show why brute force fails or gets tedious.

### 3. Build (5-15 cells, the core)
Step-by-step algorithm construction. Each cycle:
- Small code block implementing one step
- Markdown cell extracting the definition/theorem that justifies the step
- Immediate demo on the motivating problem

### 4. Full Implementation (1-2 cells)
Assemble steps into a complete function. Solve the motivating problem end-to-end.

### 5. Verify (2-4 cells)
Compare against NumPy on the same problem. Assert mathematical invariants (residual < epsilon, A*A^-1 = I, etc.). Test edge cases.

### 6. Visualize (1-3 cells, where applicable)
matplotlib plots for geometric intuition. Skipped for purely algebraic sections.

### 7. Exercises (3-5 cells)
Stub functions with docstrings, followed by assert-based test cells. Difficulty: easy, medium, challenge. Each test checks both NumPy output and a mathematical invariant.

---

## Exercise Design

```python
# Stub
def exercise_1_back_substitution(upper_triangular, b):
    """Solve Ux = b using back-substitution."""
    # YOUR CODE HERE
    raise NotImplementedError
```

```python
# Auto-grade
import numpy as np
U = [[2, 1, -1], [0, 3, 2], [0, 0, 5]]
b = [8, 13, 15]
result = exercise_1_back_substitution(U, b)
expected = np.linalg.solve(np.array(U, dtype=float), np.array(b, dtype=float))
np.testing.assert_allclose(result, expected, atol=1e-9)
residual = np.array(U) @ np.array(result) - np.array(b)
assert np.linalg.norm(residual) < 1e-9
print("Exercise 1 passed!")
```

---

## Visualization Map

| Notebook | Visualization |
|----------|--------------|
| 1.1 Intro to Systems | 2D/3D line/plane intersection — consistent vs inconsistent |
| 1.2 Gaussian Elimination | Augmented matrix heatmap showing pivot progression |
| 1.3 Applications | Polynomial curve fitting, network flow diagram |
| 2.1 Operations | 2D shape before/after matrix transformation |
| 2.3 Inverse | Transform then inverse-transform roundtrip |
| 2.5 Markov Chains | State probability convergence (line chart) |
| 3.4 Applications | Triangle area, collinearity, parallelogram via determinant |
| 4.1 Vectors in R^n | Vector addition, scalar multiplication in 2D/3D |
| 4.3 Subspaces | Subspaces of R^2/R^3 — lines/planes through origin |
| 4.6 Rank & Systems | Column space / null space basis vectors in R^3 |
| 4.7 Change of Basis | Overlaid coordinate grids — standard vs custom |
| 5.1 Length and Dot Product | Angle between vectors, orthogonal projection |
| 5.3 Gram-Schmidt | Before/after orthogonalization in 3D |
| 5.4 Least Squares | Data + fitted curves + residual bars |
| 5.5 Applications | Cross product: parallelogram area, parallelepiped volume |

~15 of 28 notebooks include visualizations. The rest skip section 6.
