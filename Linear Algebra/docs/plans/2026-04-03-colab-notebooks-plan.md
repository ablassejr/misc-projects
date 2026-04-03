# Colab Notebooks Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create 28 Google Colab notebooks teaching Elementary Linear Algebra (Larson 8e, Chapters 1-5) through code-first pedagogy, backed by a shared `linalg_core` Python package.

**Architecture:** Each notebook follows a 7-section template (Setup, Motivation, Build, Implementation, Verify, Visualize, Exercises). A `linalg_core/` Python package grows progressively — each notebook adds implementations to the corresponding module. NumPy is used exclusively for verification.

**Tech Stack:** Python 3.10+ (Colab default), NumPy (verification only), matplotlib (visualization), `linalg_core` (from-scratch implementations)

---

## Task 0: Scaffold Repository Structure

**Files:**
- Create: `linalg_core/__init__.py`
- Create: `linalg_core/matrix.py`
- Create: `linalg_core/elimination.py`
- Create: `linalg_core/ops.py`
- Create: `linalg_core/determinant.py`
- Create: `linalg_core/vecspace.py`
- Create: `linalg_core/inner.py`
- Create: `pyproject.toml`
- Create: `notebooks/ch1_systems/.gitkeep`
- Create: `notebooks/ch2_matrices/.gitkeep`
- Create: `notebooks/ch3_determinants/.gitkeep`
- Create: `notebooks/ch4_vector_spaces/.gitkeep`
- Create: `notebooks/ch5_inner_product_spaces/.gitkeep`

**Step 1: Create `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "linalg-core"
version = "0.1.0"
description = "From-scratch linear algebra implementations for learning"
requires-python = ">=3.10"

[project.optional-dependencies]
verify = ["numpy>=1.24", "matplotlib>=3.7"]
```

**Step 2: Create `linalg_core/__init__.py`**

```python
"""From-scratch linear algebra library.

Rule: This package does the computation. NumPy is for verification only.
"""

EPSILON = 1e-9
```

**Step 3: Create `linalg_core/matrix.py` with the foundational Matrix class**

```python
"""Matrix class — the foundation for everything else.

Stores data as a flat list in row-major order.
All indexing is explicit: element (i,j) = data[i * cols + j].
"""

from linalg_core import EPSILON


class Matrix:
    """A matrix stored as a flat row-major list of floats."""

    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        if data is not None:
            if len(data) != rows * cols:
                raise ValueError(f"Expected {rows*cols} elements, got {len(data)}")
            self.data = [float(x) for x in data]
        else:
            self.data = [0.0] * (rows * cols)

    @classmethod
    def from_lists(cls, lists):
        rows = len(lists)
        cols = len(lists[0])
        data = []
        for row in lists:
            if len(row) != cols:
                raise ValueError("All rows must have the same length")
            data.extend(row)
        return cls(rows, cols, data)

    @classmethod
    def identity(cls, n):
        m = cls(n, n)
        for i in range(n):
            m[i, i] = 1.0
        return m

    @classmethod
    def from_vector(cls, vec):
        return cls(len(vec), 1, vec)

    def __getitem__(self, key):
        i, j = key
        return self.data[i * self.cols + j]

    def __setitem__(self, key, value):
        i, j = key
        self.data[i * self.cols + j] = float(value)

    def get_row(self, i):
        start = i * self.cols
        return self.data[start:start + self.cols]

    def get_col(self, j):
        return [self.data[i * self.cols + j] for i in range(self.rows)]

    def copy(self):
        return Matrix(self.rows, self.cols, list(self.data))

    def to_lists(self):
        return [self.get_row(i) for i in range(self.rows)]

    def to_flat(self):
        return list(self.data)

    def __repr__(self):
        rows_str = []
        for i in range(self.rows):
            row = self.get_row(i)
            rows_str.append("  [" + ", ".join(f"{x:8.4f}" for x in row) + "]")
        return f"Matrix({self.rows}x{self.cols}):\n" + "\n".join(rows_str)

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        return all(
            abs(a - b) < EPSILON
            for a, b in zip(self.data, other.data)
        )
```

**Step 4: Create stub modules for chapters 1-5**

Each module file (`elimination.py`, `ops.py`, `determinant.py`, `vecspace.py`, `inner.py`) starts as:

```python
"""<Module description>

Functions are added progressively as notebooks are completed.
"""

from linalg_core.matrix import Matrix
from linalg_core import EPSILON
```

**Step 5: Create directory structure and commit**

```bash
mkdir -p notebooks/ch1_systems notebooks/ch2_matrices notebooks/ch3_determinants notebooks/ch4_vector_spaces notebooks/ch5_inner_product_spaces
touch notebooks/ch1_systems/.gitkeep notebooks/ch2_matrices/.gitkeep notebooks/ch3_determinants/.gitkeep notebooks/ch4_vector_spaces/.gitkeep notebooks/ch5_inner_product_spaces/.gitkeep
git add linalg_core/ pyproject.toml notebooks/
git commit -m "scaffold: linalg_core package and notebook directory structure"
```

---

## Task 1: Notebook 1.1 — Introduction to Systems of Linear Equations

**Files:**
- Create: `notebooks/ch1_systems/1_1_intro_to_systems.ipynb`
- Modify: `linalg_core/elimination.py` (add row operations + back-substitution)

**Motivation Problem:**
A chemistry lab needs to balance the equation: `x₁C₃H₈ + x₂O₂ → x₃CO₂ + x₄H₂O`. This gives the system:
- Carbon: 3x₁ = x₃
- Hydrogen: 8x₁ = 2x₄  
- Oxygen: 2x₂ = 2x₃ + x₄

"Can we find x₁, x₂, x₃, x₄ systematically?"

**Build Section — cells in order:**

1. **Representing a system as a list of lists** — encode the 3×4 augmented matrix `[[3,0,-1,0,0],[8,0,0,-2,0],[0,2,-2,-1,0]]`
2. **Definition: Linear equation in n variables** — `a₁x₁ + a₂x₂ + ... + aₙxₙ = b`. Coefficients are real numbers. No products of variables, no powers > 1.
3. **Swap rows** — implement `swap_rows(matrix, i, j)`. Demo on the augmented matrix.
4. **Scale a row** — implement `scale_row(matrix, i, scalar)`. Demo dividing row 1 by 3.
5. **Add a scaled row to another** — implement `add_scaled_row(matrix, target, source, scalar)`. Demo eliminating below the first pivot.
6. **Definition: Row-echelon form** — leading 1 in each row, each leading 1 is to the right of the one above, zero rows at bottom.
7. **Forward elimination** — implement `forward_eliminate(matrix)` using the three row operations. Reduce the chemical equation system step by step, printing after each operation.
8. **Back-substitution** — implement `back_substitute(ref_matrix)`. Solve from the bottom row up.
9. **Definition: Consistent vs Inconsistent** — a system is consistent if it has at least one solution. Three possibilities: unique, infinitely many, no solution.
10. **Parametric solutions** — when free variables exist, express solutions in terms of parameters. Demo with the chemical equation (which has a free variable — set x₁ = t).

**Full Implementation:**
Assemble into `solve_system(augmented_matrix)` that returns `(solution_type, solution)` where solution_type is "unique", "infinite", or "inconsistent".

**Verify:**
- Solve 3×3 system `[[1,1,2,9],[2,4,-3,1],[3,6,-5,0]]` — compare against `np.linalg.solve`
- Plug solution back into original system, assert residual < epsilon
- Test an inconsistent system: `[[1,1,1,2],[0,1,1,1],[0,0,0,3]]` → detect "inconsistent"
- Test underdetermined: `[[1,2,3],[2,4,6]]` → detect "infinite" with parametric form

**Visualize:**
- 2D: Plot two lines that intersect (unique), are parallel (inconsistent), are the same (infinite)
- 3D: Plot three planes meeting at a point vs along a line vs no common point

**Exercises:**

*Easy:* Solve `2x + y = 5, x - y = 1` by building the augmented matrix and calling your solver.

*Medium:* Given the system `x + 2y + 3z = 6, 2x + 5y + 2z = 4, 6x + 15y + z = -2`, determine if it's consistent. If so, find all solutions.

*Challenge:* Write a function `classify_system(A, b)` that takes a coefficient matrix and RHS vector and returns "unique", "infinite", or "inconsistent" without computing the actual solution — only by examining the REF.

**Update `linalg_core/elimination.py`:**
Add `swap_rows`, `scale_row`, `add_scaled_row`, `forward_eliminate`, `back_substitute` as module-level functions operating on `Matrix` objects.

---

## Task 2: Notebook 1.2 — Gaussian Elimination and Gauss-Jordan Elimination

**Files:**
- Create: `notebooks/ch1_systems/1_2_gaussian_elimination.ipynb`
- Modify: `linalg_core/elimination.py` (add `to_ref`, `to_rref`, `solve`)

**Motivation Problem:**
A nutrition problem: a dietitian must mix three foods to meet exact vitamin/mineral targets. Food A has [10, 6, 8] units of vitamins [C, B₁, B₂] per serving, Food B has [4, 2, 0], Food C has [6, 4, 2]. Target: [32, 20, 16] units. How many servings of each?

System: `10x + 4y + 6z = 32, 6x + 2y + 4z = 20, 8x + 0y + 2z = 16`

**Build Section — cells in order:**

1. **Augmented matrix** — construct the 3×4 augmented matrix from the nutrition problem
2. **Definition: Elementary row operations** — three types: swap, scale, add-scaled. These produce *row-equivalent* matrices.
3. **Partial pivoting** — before eliminating in column k, find the row with the largest absolute value in that column (from row k down) and swap it into the pivot position. Implement `find_pivot(matrix, col, start_row)`.
4. **Definition: Row-echelon form (REF)** — all zero rows at bottom, leading entry of each nonzero row is to the right of the one above, all entries below a leading entry are zero.
5. **Gaussian elimination with partial pivoting** — implement `to_ref(matrix)`. Apply to the nutrition problem step by step, showing each row operation and the resulting matrix.
6. **Back-substitution with REF** — solve the nutrition problem from REF.
7. **Definition: Reduced row-echelon form (RREF)** — additionally: leading entry in each row is 1, and it's the only nonzero entry in its column.
8. **Gauss-Jordan elimination** — implement `to_rref(matrix)`. Start from REF, work upward to eliminate above each pivot, then scale pivots to 1.
9. **Definition: Homogeneous system** — `Ax = 0`. Always consistent (trivial solution x = 0). Nontrivial solutions exist when there are free variables.
10. **Solving homogeneous systems** — demo with a 3×4 coefficient matrix (more unknowns than equations), showing the guaranteed nontrivial solution.

**Full Implementation:**
`solve(augmented)` — returns `(solution_type, result)`. Uses `to_rref` internally, then reads off the solution. Handles all three cases: unique (return vector), infinite (return parametric form as dict), inconsistent (return None).

**Verify:**
- REF: verify each row's leading entry is to the right of the one above
- RREF: verify additional properties (leading 1s, only nonzero in their column)
- Solve `[[2,-1,0,3],[4,0,-1,5],[6,-2,1,4]]` — compare against NumPy
- Residual check: `A @ x - b` < epsilon for every test
- Homogeneous: solve `[[1,2,3,0],[4,5,6,0],[7,8,9,0]]` — verify Ax = 0 for the nontrivial solution

**Visualize:**
Augmented matrix heatmap: show the matrix at each elimination step. Color cells by value (blue for negative, white for zero, red for positive). Highlight the current pivot and the row being modified.

**Exercises:**

*Easy:* Use `to_rref` to solve: `x + y + z = 6, 2x + 3y + z = 10, x + 2y - z = 2`.

*Medium:* Find all solutions to the homogeneous system `x₁ + 2x₂ - x₃ + x₄ = 0, 2x₁ + 4x₂ + x₃ - 2x₄ = 0`. Express the solution set in parametric vector form.

*Challenge:* Implement `num_solutions(A)` that determines the number of free variables by counting non-pivot columns in the RREF. Test on 5 different matrices of varying sizes.

**Update `linalg_core/elimination.py`:**
Add `find_pivot`, `to_ref`, `to_rref`, `solve` as module-level functions.

---

## Task 3: Notebook 1.3 — Applications of Systems of Linear Equations

**Files:**
- Create: `notebooks/ch1_systems/1_3_applications_of_systems.ipynb`

**Motivation Problem:**
You have 4 data points: `(-2, 15), (-1, 4), (1, 2), (3, 28)`. You want a polynomial `p(x) = a₀ + a₁x + a₂x² + a₃x³` passing through all of them. This gives a 4×4 linear system (Vandermonde system).

**Build Section:**

1. **Vandermonde matrix construction** — given x-values, build the matrix where row i is `[1, xᵢ, xᵢ², ..., xᵢⁿ⁻¹]`
2. **Polynomial curve fitting** — plug the 4 data points into the polynomial equation, get a system, solve with `linalg_core.elimination.solve`
3. **Evaluate and plot** — compute `p(x)` for a fine grid, plot alongside data points
4. **Network analysis** — model a simple 4-intersection traffic network. Each intersection gives a flow conservation equation: flow in = flow out. Set up and solve the system. Interpret free variables as adjustable flows.
5. **Underdetermined network** — add a 5th intersection that makes the system underdetermined. Show the parametric solution and discuss what the free variable means physically.

**Verify:**
- Polynomial: evaluate `p(xᵢ)` for each data point, verify it matches `yᵢ` within epsilon
- Cross-check polynomial coefficients against `np.polyfit`
- Network: verify all flow conservation equations are satisfied

**Visualize:**
- Scatter plot of data points + smooth polynomial curve
- Network diagram (matplotlib arrows between nodes with flow labels)

**Exercises:**

*Easy:* Find the parabola `y = a + bx + cx²` through the points `(1, 5), (2, 11), (3, 19)`.

*Medium:* A traffic network has 3 intersections with known external flows. Set up and solve the system. If underdetermined, express the solution in terms of a free variable and determine what range of values makes physical sense (all flows ≥ 0).

*Challenge:* Write `fit_polynomial(points, degree)` that builds the Vandermonde system and solves it. Test with degree < n-1 (underdetermined) and degree = n-1 (exact interpolation). What happens when degree > n-1?

---

## Task 4: Notebook 2.1 — Operations with Matrices

**Files:**
- Create: `notebooks/ch2_matrices/2_1_operations_with_matrices.ipynb`
- Modify: `linalg_core/ops.py` (add `add`, `scalar_mul`, `multiply`, `transpose`)

**Motivation Problem:**
A company has two factories. Factory output for 3 products over 2 months is stored in matrices A (Jan) and B (Feb). A cost vector gives price per unit. "How do we compute total revenue per factory per month?"

Matrix A: `[[120, 80, 40], [100, 60, 50]]` (2 factories × 3 products)  
Cost vector c: `[[25], [30], [15]]` (3 products × 1)  
Total revenue = A × c

**Build Section:**

1. **Matrix addition** — implement `add(A, B)`. Demo: total production A + B.
2. **Scalar multiplication** — implement `scalar_mul(A, s)`. Demo: if production doubles next quarter.
3. **Definition: Matrix multiplication** — entry (i,j) of AB is the dot product of row i of A with column j of B. Dimensions must be compatible: (m×n)(n×p) = (m×p).
4. **Matrix multiplication** — implement `multiply(A, B)` with the row-column rule. Demo: compute revenue A × c.
5. **Non-commutativity** — find matrices where AB ≠ BA. Demo with 2×2 examples.
6. **Identity matrix** — `Matrix.identity(n)`. Show AI = IA = A.
7. **Transpose** — implement `transpose(A)`. Row i becomes column i.
8. **Transpose properties** — `(A^T)^T = A`, `(A+B)^T = A^T + B^T`, `(cA)^T = cA^T`, `(AB)^T = B^T A^T`.

**Verify:**
- `add(A, B)` matches element-wise against NumPy
- `multiply(A, B)` matches `np.matmul`
- `transpose(transpose(A))` == A
- `transpose(multiply(A, B))` == `multiply(transpose(B), transpose(A))`
- Find A, B where `multiply(A,B) != multiply(B,A)` — verify non-commutativity

**Visualize:**
2D transformation: apply a 2×2 matrix to the unit square vertices `[(0,0), (1,0), (1,1), (0,1)]`. Plot original and transformed shapes side by side. Try rotation, scaling, shearing matrices.

**Exercises:**

*Easy:* Given `A = [[1,2],[3,4]]` and `B = [[5,6],[7,8]]`, compute AB and BA. Verify AB ≠ BA.

*Medium:* Implement a `power(A, n)` function that computes `A^n` by repeated multiplication. Test with the rotation matrix `R = [[cos θ, -sin θ], [sin θ, cos θ]]` for θ = π/4. Verify `R^8 = I`.

*Challenge:* Two loop orders for matrix multiplication: `i-j-k` and `i-k-j`. Implement both and time them on 200×200 matrices. Which is faster and why? (Hint: cache locality and row-major storage.)

**Update `linalg_core/ops.py`:**
Add `add`, `scalar_mul`, `multiply`, `transpose`.

---

## Task 5: Notebook 2.2 — Properties of Matrix Operations

**Files:**
- Create: `notebooks/ch2_matrices/2_2_properties_of_matrix_operations.ipynb`

**Motivation Problem:**
"Matrix algebra looks like regular algebra — addition is commutative, multiplication is associative. But some familiar rules break. Can we still factor? Can we cancel? Let's stress-test the algebra."

**Build Section:**

1. **Additive properties** — verify with random matrices: A+B = B+A, (A+B)+C = A+(B+C), A+0 = A, A+(-A) = 0
2. **Multiplicative properties** — A(BC) = (AB)C, A(B+C) = AB+AC, (A+B)C = AC+BC, cA·B = c(AB) = A·cB
3. **The zero matrix trap** — find A ≠ 0, B ≠ 0 where AB = 0. Example: `A = [[1,2],[2,4]]`, `B = [[2,-1],[-1,0.5]]`... actually `B = [[-2,2],[1,-1]]` gives AB = 0.
4. **Cancellation failure** — find A, B, C where AB = AC but B ≠ C. This happens when A is singular.
5. **Why these break** — connect to determinant = 0 (preview of Ch.3). The zero-product property and cancellation both require invertibility.

**Verify:**
- Associativity: `multiply(A, multiply(B, C))` == `multiply(multiply(A, B), C)` for random 3×3 matrices
- Distributivity: `multiply(A, add(B, C))` == `add(multiply(A, B), multiply(A, C))`
- Zero product: verify AB = 0 with the specific non-zero A, B

**Exercises:**

*Easy:* Verify all four additive properties for `A = [[1,2],[3,4]]`, `B = [[5,6],[7,8]]`.

*Medium:* Find a 3×3 nonzero matrix A such that A² = 0 (a nilpotent matrix). Verify your answer.

*Challenge:* Write `test_cancellation(A, B, C)` that checks if AB = AC and B ≠ C. Generate 1000 random singular 3×3 matrices and find a triple (A, B, C) demonstrating cancellation failure.

---

## Task 6: Notebook 2.3 — The Inverse of a Matrix

**Files:**
- Create: `notebooks/ch2_matrices/2_3_inverse_of_a_matrix.ipynb`
- Modify: `linalg_core/ops.py` (add `inverse`)

**Motivation Problem:**
An encryption system encodes a message as `y = Ax` where A is a secret key matrix. To decode: `x = A⁻¹y`. If A = `[[1,2],[3,7]]` and the encoded message is `y = [11, 31]`, what's the original message?

**Build Section:**

1. **Definition: Invertible matrix** — A is invertible (nonsingular) if there exists B such that AB = BA = I. B is unique and denoted A⁻¹.
2. **2×2 formula** — for `A = [[a,b],[c,d]]`, `A⁻¹ = (1/det) * [[d,-b],[-c,a]]` where det = ad - bc. Implement `inverse_2x2(A)`.
3. **Decode the message** — compute A⁻¹ and multiply by y. Verify A·A⁻¹ = I.
4. **Gauss-Jordan method for larger matrices** — augment [A | I], reduce to RREF. If left side becomes I, right side is A⁻¹. If left side has a zero row, A is singular.
5. **Implement `inverse(A)`** — use `to_rref` on the augmented matrix. Return the inverse or raise an error if singular.
6. **Solving systems via inverse** — Ax = b ⟹ x = A⁻¹b. Compare to direct RREF solution.
7. **When inverse doesn't exist** — demo with a singular matrix. Show the augmented [A|I] reduction produces a zero row on the left.

**Verify:**
- `multiply(A, inverse(A))` == Identity within epsilon
- `multiply(inverse(A), A)` == Identity
- `inverse(inverse(A))` == A
- `inverse(multiply(A, B))` == `multiply(inverse(B), inverse(A))`
- Inverse-based solve matches RREF-based solve for same system
- Compare against `np.linalg.inv`

**Visualize:**
Apply a 2×2 matrix A to the unit square. Then apply A⁻¹. Show the roundtrip: original → transformed → back to original.

**Exercises:**

*Easy:* Find the inverse of `[[2, 1], [5, 3]]` using the 2×2 formula. Verify by multiplication.

*Medium:* Find the inverse of `[[1, 0, 2], [2, -1, 3], [4, 1, 8]]` using Gauss-Jordan. If it's singular, explain why.

*Challenge:* The Hilbert matrix `H_n` has entries `H[i,j] = 1/(i+j+1)`. Compute inverses for n = 2, 3, 4, 5. At what size does `multiply(H, inverse(H))` start visibly deviating from identity? This demonstrates ill-conditioning.

**Update `linalg_core/ops.py`:**
Add `inverse`.

---

## Task 7: Notebook 2.4 — Elementary Matrices

**Files:**
- Create: `notebooks/ch2_matrices/2_4_elementary_matrices.ipynb`
- Modify: `linalg_core/ops.py` (add `lu_factorize`, `forward_sub`, `back_sub`)

**Motivation Problem:**
"Every row operation we've been doing is secretly a matrix multiplication. If we can decompose A into simpler pieces (L and U), we can solve Ax = b with two easy passes instead of full elimination every time."

**Build Section:**

1. **Elementary matrices** — each elementary row operation corresponds to multiplying by an elementary matrix. Build `elementary_swap(n, i, j)`, `elementary_scale(n, i, c)`, `elementary_add(n, i, j, c)`.
2. **Demo: row operation = matrix multiply** — show that `E × A` produces the same result as applying the row operation directly to A.
3. **Invertibility condition** — A is invertible iff it's row-equivalent to I. Equivalently: A = E₁E₂...Eₖ (product of elementary matrices).
4. **LU-factorization concept** — A = LU where L is lower triangular (multipliers from elimination) and U is upper triangular (the REF form). 
5. **Doolittle's method** — implement `lu_factorize(A)`. Track multipliers during forward elimination, store them in L. No row swaps (if a zero pivot is encountered, factorization fails without pivoting).
6. **Forward substitution** — implement `forward_sub(L, b)` to solve Ly = b.
7. **Back substitution** — implement `back_sub(U, y)` to solve Ux = y.
8. **LU solve** — solve Ax = b in two passes: forward sub (Ly = b) then back sub (Ux = y). Demo on the same system solved earlier via RREF.

**Verify:**
- `multiply(L, U)` == A within epsilon
- L is lower triangular with 1s on diagonal
- U is upper triangular
- LU-based solve matches RREF solve for same system
- Compare L, U against `scipy.linalg.lu` (with permutation)

**Exercises:**

*Easy:* Construct the 3×3 elementary matrix that adds 3× row 1 to row 2. Verify by multiplying it with a test matrix.

*Medium:* Find the LU factorization of `A = [[2, -1, 1], [4, 1, -1], [-2, 3, 1]]`. Verify L×U = A. Then solve Ax = [1, 5, -1] using forward/back substitution.

*Challenge:* Solve the same system Ax = b for 3 different right-hand sides `b₁, b₂, b₃` using (a) RREF three times and (b) LU once + three forward/back sub passes. Count the total floating-point operations for each approach.

**Update `linalg_core/ops.py`:**
Add `elementary_swap`, `elementary_scale`, `elementary_add`, `lu_factorize`, `forward_sub`, `back_sub`.

---

## Task 8: Notebook 2.5 — Markov Chains

**Files:**
- Create: `notebooks/ch2_matrices/2_5_markov_chains.ipynb`

**Motivation Problem:**
Weather in a city follows a pattern: if today is sunny, there's a 70% chance tomorrow is sunny and 30% chance of rain. If today is rainy, there's a 40% chance tomorrow is sunny and 60% chance of rain. Given it's sunny today, what's the weather probability distribution after 7 days? After 100 days?

**Build Section:**

1. **Stochastic matrix** — a square matrix where every column sums to 1 and all entries are non-negative. Implement `is_stochastic(P)`.
2. **State vector** — a column vector whose entries sum to 1. `x₀ = [1, 0]` (sunny today with certainty).
3. **One step** — `x₁ = P × x₀`. Compute the day-1 probability.
4. **Iterating** — `xₖ = P^k × x₀`. Loop and compute x₁ through x₇.
5. **Convergence** — keep iterating until `‖xₖ₊₁ - xₖ‖ < epsilon`. The limit is the steady-state vector.
6. **Algebraic steady state** — solve `(P - I)x = 0` with the constraint that entries sum to 1. Use `linalg_core.elimination.solve` on the augmented system. Compare to the iterative result.
7. **Regular Markov chains** — a Markov chain is regular if some power of P has all positive entries. Regular chains always converge to a unique steady state regardless of x₀.

**Verify:**
- P is stochastic: all columns sum to 1
- State vector at each step: entries sum to 1, all non-negative
- Iterative steady state matches algebraic steady state within epsilon
- Compare against `np.linalg.matrix_power` for P^100

**Visualize:**
Line chart: x-axis is time step (0 to 50), y-axis is probability. Two lines (sunny, rainy) converging to steady-state values. Mark the algebraic steady state with horizontal dashed lines.

**Exercises:**

*Easy:* A consumer switches between brands A and B. Transition matrix: `P = [[0.8, 0.3], [0.2, 0.7]]`. Starting with 60% market share for A, find the distribution after 5 steps.

*Medium:* Extend to 3 states (sunny, cloudy, rainy) with transition matrix `P = [[0.6, 0.3, 0.1], [0.2, 0.5, 0.3], [0.2, 0.2, 0.6]]`. Find the steady-state vector both iteratively and algebraically.

*Challenge:* Investigate what happens with an absorbing Markov chain: `P = [[1, 0, 0.2], [0, 1, 0.3], [0, 0, 0.5]]`. States 1 and 2 are absorbing (once entered, never left). Starting from state 3, what's the probability of eventually being absorbed into state 1 vs state 2?

---

## Task 9: Notebook 2.6 — Applications of Matrix Operations

**Files:**
- Create: `notebooks/ch2_matrices/2_6_applications_of_matrix_operations.ipynb`

**Motivation Problem:**
You intercept the encoded message `[8, 21, 5, 10, 21, 5]`. You know it was encrypted using a Hill cipher with key matrix `K = [[1, 0, 1], [2, 1, 0], [0, 1, 2]]`. Decode it.

**Build Section:**

1. **Hill cipher: encoding** — map letters to numbers (A=0, ..., Z=25). Split plaintext into blocks of size n. Multiply each block by key matrix K (mod 26).
2. **Hill cipher: decoding** — multiply ciphertext blocks by K⁻¹ (mod 26). Need modular inverse.
3. **Modular inverse** — implement `mod_inverse_matrix(K, mod)`. Use the adjoint formula: `K⁻¹ = (1/det(K)) × adj(K)` all mod 26. Need modular multiplicative inverse of det(K).
4. **Encode/decode demo** — encode "HELP" with K, decode back, verify roundtrip.
5. **Leontief input-output model** — an economy has n sectors. The consumption matrix C describes how much each sector consumes from others. The production equation: `x = Cx + d` → `(I - C)x = d` → `x = (I - C)⁻¹d`.
6. **Demo Leontief** — 3-sector economy with consumption matrix and demand vector. Solve for required output.

**Verify:**
- Encode then decode recovers the original message
- `K × K_inv mod 26` == Identity mod 26
- Leontief: `(I-C) × x - d` < epsilon

**Exercises:**

*Easy:* Encode "CODE" using key matrix `K = [[3, 2], [5, 3]]` with the Hill cipher (mod 26). Then decode your ciphertext to recover "CODE".

*Medium:* A 3-sector economy has consumption matrix `C = [[0.2, 0.3, 0.1], [0.1, 0.2, 0.3], [0.3, 0.1, 0.2]]` and external demand `d = [100, 150, 200]`. Find the required production for each sector.

*Challenge:* The Hill cipher with a 2×2 key is breakable by known-plaintext attack. Given that "TH" encrypts to "PO" and "AT" encrypts to "LS", recover the key matrix K. Verify by encoding "MATH" with your recovered key.

---

## Task 10: Notebook 3.1 — The Determinant of a Matrix

**Files:**
- Create: `notebooks/ch3_determinants/3_1_determinant_of_a_matrix.ipynb`
- Modify: `linalg_core/determinant.py` (add `det_cofactor`, `minor`, `cofactor`)

**Motivation Problem:**
"We've been saying a matrix is 'singular' when it has no inverse and 'nonsingular' when it does. Is there a single number that tells us which? The determinant is that number."

**Build Section:**

1. **2×2 determinant** — `det([[a,b],[c,d]]) = ad - bc`. Implement and demo. Show det = 0 means singular (try `[[1,2],[2,4]]`).
2. **Minors** — `M_ij` is the determinant of the matrix with row i and column j deleted. Implement `minor(A, i, j)`.
3. **Cofactors** — `C_ij = (-1)^(i+j) × M_ij`. The sign alternates in a checkerboard pattern.
4. **Cofactor expansion along row 1** — `det(A) = Σ a₁ⱼ × C₁ⱼ`. Implement `det_cofactor(A)` recursively. Base case: 1×1 matrix.
5. **Demo on 3×3** — compute determinant of `[[1, 2, 3], [4, 5, 6], [7, 8, 0]]` step by step.
6. **Expansion along any row or column** — the result is the same regardless of which row/column you expand along. Verify with the 3×3 example.
7. **Triangular matrix shortcut** — det of a triangular matrix is the product of diagonal entries. Verify: reduce to REF, multiply diagonal.

**Verify:**
- `det_cofactor(A)` matches `np.linalg.det(A)` for multiple test matrices
- Triangular matrix: det = product of diagonal
- 2×2 formula matches cofactor expansion

**Exercises:**

*Easy:* Compute the determinant of `[[3, -2], [6, -4]]` using the 2×2 formula. Is this matrix invertible?

*Medium:* Compute the determinant of `[[2, -1, 3], [1, 0, -2], [3, 5, 1]]` by cofactor expansion along row 1, then verify by expanding along column 2.

*Challenge:* Time `det_cofactor` on matrices from 2×2 to 10×10. Plot the timing curve. At what size does it become painfully slow? Why? (Hint: count the number of recursive calls.)

**Update `linalg_core/determinant.py`:**
Add `minor`, `cofactor`, `det_cofactor`.

---

## Task 11: Notebook 3.2 — Determinants and Elementary Operations

**Files:**
- Create: `notebooks/ch3_determinants/3_2_determinants_and_elementary_operations.ipynb`
- Modify: `linalg_core/determinant.py` (add `det_elimination`)

**Motivation Problem:**
"Cofactor expansion is O(n!). For a 20×20 matrix, that's 2.4 × 10¹⁸ operations. We need a faster way. Can we use the elimination we already have?"

**Build Section:**

1. **Effect of row swap** — swapping two rows negates the determinant. Demo: compute det before and after a swap.
2. **Effect of scaling** — multiplying a row by c multiplies det by c. Demo.
3. **Effect of row addition** — adding a multiple of one row to another doesn't change det. Demo.
4. **Elimination-based determinant** — reduce to upper triangular using row operations. Track sign flips (from swaps) and scale factors. Final det = (product of diagonal) × (-1)^(number of swaps) / (product of scale factors). Implement `det_elimination(A)`.
5. **Speed comparison** — time cofactor vs elimination on 8×8 matrix. Elimination should be nearly instant.
6. **det(AB) = det(A) × det(B)** — verify with random matrices.
7. **det(A^T) = det(A)** — verify.
8. **det(A⁻¹) = 1/det(A)** — verify.

**Verify:**
- `det_elimination(A)` matches `det_cofactor(A)` for multiple matrices
- `det_elimination(multiply(A, B))` ≈ `det_elimination(A) * det_elimination(B)`
- `det_elimination(transpose(A))` ≈ `det_elimination(A)`
- Compare both against `np.linalg.det`

**Exercises:**

*Easy:* Compute the determinant of `[[4, 2, 1], [0, 3, -1], [0, 0, 5]]` using the triangular shortcut (no expansion needed).

*Medium:* Use `det_elimination` to determine which of these matrices are invertible: `A = [[1,2,3],[4,5,6],[7,8,9]]`, `B = [[1,2,3],[4,5,6],[7,8,10]]`. Explain the geometric intuition for why one is singular.

*Challenge:* Benchmark both determinant methods on matrix sizes 2 through 12. Plot execution time vs n for both. Fit an exponential to cofactor times and a polynomial to elimination times.

**Update `linalg_core/determinant.py`:**
Add `det_elimination`.

---

## Task 12: Notebook 3.3 — Properties of Determinants

**Files:**
- Create: `notebooks/ch3_determinants/3_3_properties_of_determinants.ipynb`

**Motivation Problem:**
"We've built two ways to compute determinants. Now let's understand what the determinant *means* — what properties does it satisfy, and what does det = 0 really tell us about a matrix?"

**Build Section:**

1. **det(cA) = cⁿ det(A)** for n×n matrix A. Demo: scale A by 2, check det. Common mistake: thinking det(2A) = 2·det(A).
2. **det(A) ≠ 0 ⟺ A is invertible** — the master equivalence. Test with singular and nonsingular matrices.
3. **The Invertible Matrix Theorem (growing list)** — collect all equivalent conditions seen so far: A invertible ⟺ det(A) ≠ 0 ⟺ RREF of A is I ⟺ Ax = 0 has only trivial solution ⟺ A is a product of elementary matrices.
4. **Conditions for det = 0** — zero row, two equal rows, proportional rows. Demo each.
5. **det and linear independence preview** — columns of A are linearly independent iff det(A) ≠ 0. (Full treatment in Ch.4.)

**Verify:**
- `det(scalar_mul(A, c))` ≈ `c**n * det(A)` for n×n A
- Matrices with zero/duplicate/proportional rows have det ≈ 0
- Invertible matrices have det ≠ 0; verify inverse exists

**Exercises:**

*Easy:* Without computing, determine if `det(3A)` = 3·det(A) when A is 4×4. What is the correct relationship?

*Medium:* Write a function `is_invertible(A)` that checks invertibility using the determinant. Test it on 10 random 5×5 matrices and compare against trying to compute the inverse.

*Challenge:* For a random 5×5 matrix A, verify all 5 conditions of the Invertible Matrix Theorem computationally: (1) det ≠ 0, (2) RREF = I, (3) Ax=0 has only trivial solution, (4) inverse exists, (5) rank = 5 (use your Ch.1 tools to check rank via RREF).

---

## Task 13: Notebook 3.4 — Applications of Determinants

**Files:**
- Create: `notebooks/ch3_determinants/3_4_applications_of_determinants.ipynb`
- Modify: `linalg_core/determinant.py` (add `cofactor_matrix`, `adjoint`, `inverse_adjoint`, `cramers_rule`)

**Motivation Problem:**
Three surveyors mark points on a map: (1, 2), (4, 6), (7, 10). Are these points on the same line? If they place a fourth point at (2, 5), what's the area of the triangle formed by any three of them?

**Build Section:**

1. **Cramer's Rule** — for Ax = b with det(A) ≠ 0: xᵢ = det(Aᵢ)/det(A) where Aᵢ replaces column i with b. Implement `cramers_rule(A, b)`.
2. **Adjoint matrix** — `adj(A)` is the transpose of the cofactor matrix. Implement `cofactor_matrix(A)` and `adjoint(A)`.
3. **Inverse via adjoint** — `A⁻¹ = (1/det(A)) × adj(A)`. Implement `inverse_adjoint(A)`. Compare against Gauss-Jordan inverse.
4. **Area of a triangle** — area = `½|det([[x₁,y₁,1],[x₂,y₂,1],[x₃,y₃,1]])|`. Demo with the surveyor points.
5. **Collinearity test** — points are collinear iff the above determinant = 0. Test the three surveyor points.
6. **Equation of a line** — two-point form via determinant: `det([[x,y,1],[x₁,y₁,1],[x₂,y₂,1]]) = 0`.
7. **Volume of a tetrahedron** — `V = (1/6)|det([[x₂-x₁,y₂-y₁,z₂-z₁],[x₃-x₁,y₃-y₁,z₃-z₁],[x₄-x₁,y₄-y₁,z₄-z₁]])|`.

**Verify:**
- Cramer's Rule solution matches RREF solution and NumPy
- Inverse via adjoint matches Gauss-Jordan inverse
- Triangle area matches the shoelace formula
- Collinear points give area ≈ 0

**Visualize:**
- Plot triangle with area shaded and labeled
- Plot collinear points on a line
- 3D tetrahedron with volume labeled

**Exercises:**

*Easy:* Use Cramer's Rule to solve `2x + y = 5, 3x - 2y = 4`.

*Medium:* Determine if the points (1, 1), (2, 3), (4, 7) are collinear. Then find the area of the triangle formed by (0, 0), (3, 0), (1, 4).

*Challenge:* Write `equation_of_plane(p1, p2, p3)` that returns coefficients (a, b, c, d) for the plane ax + by + cz = d passing through three 3D points. Test with (1,0,0), (0,1,0), (0,0,1) — should give x + y + z = 1.

**Update `linalg_core/determinant.py`:**
Add `cofactor_matrix`, `adjoint`, `inverse_adjoint`, `cramers_rule`.

---

## Task 14: Notebook 4.1 — Vectors in R^n

**Files:**
- Create: `notebooks/ch4_vector_spaces/4_1_vectors_in_rn.ipynb`

**Motivation Problem:**
"A robot arm in 3D space applies forces from 3 different actuators. Each force is a vector. The net force is a linear combination of these. Can any desired force be achieved?"

Force vectors: `f₁ = [1, 0, 2]`, `f₂ = [0, 1, -1]`, `f₃ = [3, 1, 5]`. Target: `t = [4, 2, 6]`. Find scalars c₁, c₂, c₃ such that `c₁f₁ + c₂f₂ + c₃f₃ = t`.

**Build Section:**

1. **Vectors in Rⁿ** — n-tuples of real numbers. Implement as column matrices (n×1).
2. **Vector addition and scalar multiplication** — reuse `ops.add` and `ops.scalar_mul`. Demo with force vectors.
3. **Linear combination** — `c₁v₁ + c₂v₂ + ... + cₖvₖ`. Implement `linear_combination(vectors, scalars)`.
4. **Standard unit vectors** — `e₁ = [1,0,...,0]`, `e₂ = [0,1,...,0]`, etc. Every vector is a linear combination of the standard unit vectors.
5. **The robot arm problem** — set up as a system `[f₁ | f₂ | f₃ | t]` and solve. The coefficients are the actuator settings.
6. **When it fails** — change f₃ to `[2, 1, 1]` (a linear combination of f₁ and f₂). Now some targets can't be reached. (Preview of linear dependence.)

**Visualize:**
- 2D: draw vectors as arrows, show a linear combination graphically (parallelogram rule)
- 3D: three force vectors and their linear combination reaching the target

**Exercises:**

*Easy:* Express `v = [3, 7]` as a linear combination of `e₁ = [1, 0]` and `e₂ = [0, 1]`.

*Medium:* Determine if `w = [1, 2, 3]` is a linear combination of `v₁ = [1, 0, 1]` and `v₂ = [0, 1, 1]`. Set up and solve the system.

*Challenge:* Write a function `is_linear_combination(w, vectors)` that returns True/False and the coefficients if True. Test with vectors in R⁴.

---

## Task 15: Notebook 4.2 — Vector Spaces

**Files:**
- Create: `notebooks/ch4_vector_spaces/4_2_vector_spaces.ipynb`

**Motivation Problem:**
"Rⁿ with its addition and scalar multiplication satisfies 10 specific axioms. Surprisingly, matrices, polynomials, and even continuous functions satisfy the same 10 axioms. What structure do they all share?"

**Build Section:**

1. **The 10 axioms** — list all 10 vector space axioms (closure under addition, closure under scalar multiplication, commutativity, associativity, additive identity, additive inverse, scalar associativity, scalar distributivity over vector addition, scalar distributivity over scalar addition, scalar identity).
2. **Verify Rⁿ** — computationally check all 10 axioms for R³ with random vectors.
3. **Verify M₂ₓ₂** — represent 2×2 matrices as vectors, check axioms.
4. **Verify P₂ (polynomials of degree ≤ 2)** — represent `a + bx + cx²` as `[a, b, c]`. Check axioms.
5. **A non-example** — the set of all 2×2 matrices with det = 1. Show it fails closure under addition: det(A) = 1 and det(B) = 1 does not imply det(A+B) = 1.
6. **Properties that follow from the axioms** — 0·v = 0, c·0 = 0, (-1)·v = -v. Verify computationally.

**Exercises:**

*Easy:* Verify the 10 axioms for R² using `v = [1, 2]`, `w = [3, -1]`, scalars c = 3, d = -2.

*Medium:* Show that the set `{(x, y) : x ≥ 0, y ≥ 0}` (first quadrant) is NOT a vector space. Which axiom(s) fail?

*Challenge:* The set of 2×2 symmetric matrices (A = A^T) forms a vector space. Verify all 10 axioms computationally. What is its dimension? (Hint: how many free entries does a 2×2 symmetric matrix have?)

---

## Task 16: Notebook 4.3 — Subspaces of Vector Spaces

**Files:**
- Create: `notebooks/ch4_vector_spaces/4_3_subspaces.ipynb`

**Motivation Problem:**
"Not every subset of a vector space is a vector space. But some are — and they show up everywhere: the set of solutions to Ax = 0, the set of all vectors reachable by combining given vectors. How do we test if a subset qualifies?"

**Build Section:**

1. **Subspace test** — three conditions: (a) contains zero vector, (b) closed under addition, (c) closed under scalar multiplication. Implement `is_subspace_candidate(vectors, zero_vec)` that tests (b) and (c) on given sample vectors.
2. **Trivial subspaces** — {0} and V itself are always subspaces.
3. **Subspaces of R²** — only {0}, lines through the origin, and R² itself. Demo: the line `y = 2x` is a subspace; the line `y = 2x + 1` is not (doesn't contain zero).
4. **Subspaces of R³** — {0}, lines through origin, planes through origin, R³.
5. **Span** — `span(S)` is the set of all linear combinations of vectors in S. It's always a subspace. Implement `is_in_span(v, S)` using the system-solving from Ch.1.
6. **Null space preview** — the set of solutions to Ax = 0 is a subspace of Rⁿ. Verify the three conditions.

**Visualize:**
- R²: plot a line through origin (subspace) vs a shifted line (not a subspace)
- R³: plot a plane through origin (subspace) defined by a normal vector

**Exercises:**

*Easy:* Is the set `{(x, y, z) : x + y + z = 0}` a subspace of R³? Verify the three conditions.

*Medium:* Given `S = {[1, 2, 1], [0, 1, -1]}`, determine if `v = [3, 5, 4]` is in span(S). What about `w = [1, 1, 1]`?

*Challenge:* Write `span_dimension(vectors)` that determines the dimension of span(S) by finding how many of the vectors are linearly independent (using RREF). Test with sets of 2, 3, 4 vectors in R³.

---

## Task 17: Notebook 4.4 — Spanning Sets and Linear Independence

**Files:**
- Create: `notebooks/ch4_vector_spaces/4_4_spanning_sets_and_linear_independence.ipynb`
- Modify: `linalg_core/vecspace.py` (add `is_independent`, `is_in_span`)

**Motivation Problem:**
"An engineer has 4 sensor measurements in R³. Are any of them redundant? If so, which can be removed without losing information?"

Sensors: `s₁ = [1, 0, 2]`, `s₂ = [0, 1, -1]`, `s₃ = [2, 1, 3]`, `s₄ = [1, 1, 1]`. One of these must be a linear combination of the others (pigeonhole: 4 vectors in R³).

**Build Section:**

1. **Linear independence definition** — {v₁, ..., vₖ} is linearly independent if `c₁v₁ + ... + cₖvₖ = 0` implies all cᵢ = 0. Otherwise linearly dependent.
2. **Testing via homogeneous system** — stack vectors as columns, solve `Ax = 0`. If only trivial solution → independent. If nontrivial → dependent, and the coefficients tell you the dependency.
3. **Implement `is_independent(vectors)`** — uses RREF on the matrix with vectors as columns.
4. **The sensor problem** — test independence of s₁, s₂, s₃, s₄. Find the dependency relation. Remove the redundant sensor.
5. **Key fact: more vectors than dimension ⟹ dependent** — if you have k vectors in Rⁿ and k > n, they must be dependent.
6. **Spanning set** — S spans V if every vector in V is a linear combination of vectors in S. Implement `is_spanning_set(vectors, n)` — vectors span Rⁿ iff the matrix has rank n.
7. **Wronskian for functions** — (brief mention) for function spaces, the Wronskian determinant tests independence. Demo with `{1, x, x²}`.

**Verify:**
- Independent sets: the only solution to the homogeneous system is trivial
- Dependent sets: nontrivial solution exists, and the linear combination actually equals zero
- Compare rank computation against `np.linalg.matrix_rank`

**Exercises:**

*Easy:* Are `v₁ = [1, 2]` and `v₂ = [3, 6]` linearly independent? Explain geometrically.

*Medium:* Find the largest linearly independent subset of `{[1,0,1,0], [0,1,0,1], [1,1,1,1], [2,1,2,1]}`. Express the dependent vectors as linear combinations of the independent ones.

*Challenge:* Write `remove_dependent(vectors)` that returns a maximal linearly independent subset. Use RREF to identify pivot columns. Test on sets of 5-6 vectors in R⁴.

**Update `linalg_core/vecspace.py`:**
Add `is_independent`, `is_in_span`.

---

## Task 18: Notebook 4.5 — Basis and Dimension

**Files:**
- Create: `notebooks/ch4_vector_spaces/4_5_basis_and_dimension.ipynb`

**Motivation Problem:**
"A basis is the Goldilocks set — linearly independent (no redundancy) AND spanning (complete coverage). How many vectors does a basis for Rⁿ need? Exactly n. This number is the *dimension*."

**Build Section:**

1. **Definition: Basis** — a set B is a basis for V if (a) B is linearly independent, (b) B spans V. Every vector in V has a *unique* representation as a linear combination of basis vectors.
2. **Standard basis for Rⁿ** — {e₁, ..., eₙ}. Verify it's a basis.
3. **Non-standard basis** — B = {[1,1], [1,-1]} is a basis for R². Express [3, 5] in this basis: find c₁, c₂ such that c₁[1,1] + c₂[1,-1] = [3,5]. Solution: c₁ = 4, c₂ = -1.
4. **Dimension** — the number of vectors in any basis for V. All bases have the same size. dim(Rⁿ) = n.
5. **Finding a basis from a spanning set** — RREF the matrix, take columns corresponding to pivots.
6. **Extending to a basis** — if you have a linearly independent set that doesn't span, you can add vectors to make it a basis.
7. **Theorems connecting count, independence, spanning** — if dim(V) = n: (a) more than n vectors → dependent, (b) fewer than n vectors → don't span, (c) exactly n independent vectors → must be a basis.

**Exercises:**

*Easy:* Verify that `{[1, 0, 0], [0, 1, 0], [0, 0, 1]}` is a basis for R³ by checking independence and spanning.

*Medium:* Find a basis for the subspace spanned by `{[1,2,3], [4,5,6], [7,8,9], [2,1,0]}`. What is its dimension?

*Challenge:* Write `find_basis(vectors)` that extracts a basis from a spanning set. Then write `extend_to_basis(independent_set, n)` that extends a linearly independent set to a basis for Rⁿ. Test: extend {[1,1,0]} to a basis for R³.

---

## Task 19: Notebook 4.6 — Rank of a Matrix and Systems of Linear Equations

**Files:**
- Create: `notebooks/ch4_vector_spaces/4_6_rank_and_systems.ipynb`
- Modify: `linalg_core/vecspace.py` (add `rank`, `nullity`, `null_space`, `column_space`, `row_space`)

**Motivation Problem:**
"We've been solving Ax = b and sometimes getting unique solutions, sometimes infinite, sometimes none. The rank of A is the single number that explains all three cases."

**Build Section:**

1. **Row space** — the subspace spanned by the rows of A. Implement `row_space(A)` — nonzero rows of RREF.
2. **Column space** — the subspace spanned by the columns of A. Implement `column_space(A)` — columns of A corresponding to pivot positions in RREF.
3. **Null space** — the solution set of Ax = 0. Implement `null_space(A)` — identify free variables from RREF, construct basis vectors by setting each free variable to 1 and the rest to 0.
4. **Rank** — `rank(A)` = dim(row space) = dim(column space) = number of pivots. Implement `rank(A)`.
5. **Nullity** — `nullity(A)` = dim(null space) = number of free variables. Implement `nullity(A)`.
6. **Rank-Nullity Theorem** — `rank(A) + nullity(A) = n` (number of columns). Verify on multiple matrices.
7. **Rank and solution types** — unique solution iff rank(A) = rank([A|b]) = n. Infinite iff rank(A) = rank([A|b]) < n. Inconsistent iff rank(A) < rank([A|b]).

**Verify:**
- rank(A) + nullity(A) = n for every test matrix
- Every null space basis vector satisfies Ax = 0
- Column space basis vectors are actual columns of A
- Row space basis vectors span the same space as the original rows
- Compare rank against `np.linalg.matrix_rank`

**Visualize:**
For a 3×3 matrix: plot column space basis vectors (a plane or line through origin in R³) and null space basis vectors. Show they are complementary.

**Exercises:**

*Easy:* Find the rank and nullity of `A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`. Verify the Rank-Nullity Theorem.

*Medium:* Find bases for the row space, column space, and null space of `A = [[1, 2, -1, 3], [2, 4, 1, -2], [3, 6, 0, 1]]`. Verify: every null space vector satisfies Ax = 0, and column space vectors are columns of A.

*Challenge:* Write `solution_analysis(A, b)` that uses rank to predict the solution type before solving. Returns a dict with rank(A), rank([A|b]), nullity, solution_type, and (if consistent) the solution. Test on 5 different systems.

**Update `linalg_core/vecspace.py`:**
Add `rank`, `nullity`, `null_space`, `column_space`, `row_space`.

---

## Task 20: Notebook 4.7 — Coordinates and Change of Basis

**Files:**
- Create: `notebooks/ch4_vector_spaces/4_7_coordinates_and_change_of_basis.ipynb`
- Modify: `linalg_core/vecspace.py` (add `change_of_basis`, `coordinate_vector`)

**Motivation Problem:**
"A graphics engine stores a 3D model in world coordinates. The camera has its own coordinate system. To render the scene, every point must be converted from world coordinates to camera coordinates. This is a change of basis."

**Build Section:**

1. **Coordinate vector** — given a basis B = {v₁, ..., vₙ} and a vector x, the coordinate vector [x]_B = [c₁, ..., cₙ] satisfies `x = c₁v₁ + ... + cₙvₙ`. Implement `coordinate_vector(x, basis)` — solve the system.
2. **Demo** — B = {[1,1], [1,-1]}. Find [x]_B for x = [3, 5]. Answer: [4, -1].
3. **Transition matrix** — P converts coordinates from basis B' to basis B. To find P: form `[B | B']`, reduce to `[I | P]`. Implement `change_of_basis(old_basis, new_basis)`.
4. **Roundtrip** — convert x from standard to B', then back to standard. Verify recovery.
5. **Inverse transition** — P⁻¹ converts the other direction. Verify P × P⁻¹ = I.
6. **The camera analogy** — set up a 2D "world basis" and "camera basis". Convert a set of points from world to camera coordinates.

**Visualize:**
Two overlaid coordinate grids in R²: the standard grid (gray) and the custom basis grid (blue). A point is shown with its coordinates in both systems. Move the point and watch both coordinate readouts change.

**Exercises:**

*Easy:* Find the coordinate vector of `x = [5, 3]` relative to the basis `B = {[2, 1], [1, 3]}`.

*Medium:* Find the transition matrix from `B = {[1, 0], [0, 1]}` to `B' = {[1, 1], [1, -1]}`. Use it to convert [3, 5] from B-coordinates to B'-coordinates.

*Challenge:* In R³, define two non-standard bases B and B'. Find the transition matrix from B to B' directly (without going through the standard basis as an intermediary). Verify with a round-trip.

**Update `linalg_core/vecspace.py`:**
Add `change_of_basis`, `coordinate_vector`.

---

## Task 21: Notebook 4.8 — Applications of Vector Spaces

**Files:**
- Create: `notebooks/ch4_vector_spaces/4_8_applications_of_vector_spaces.ipynb`

**Motivation Problem:**
"Differential equations have solution spaces that are vector spaces. The Wronskian determinant — which we built in Ch.3 — tests whether solutions are linearly independent. Let's see vector space theory applied outside Rⁿ."

**Build Section:**

1. **Solution space of a linear ODE** — `y'' + y = 0` has solutions `sin(t)` and `cos(t)`. The general solution `c₁sin(t) + c₂cos(t)` is a 2-dimensional vector space.
2. **Wronskian** — for functions f₁, f₂: `W = det([[f₁, f₂], [f₁', f₂']])`. If W ≠ 0 at any point, the functions are linearly independent. Implement `wronskian(functions, derivatives, t)` numerically.
3. **Demo** — verify sin(t) and cos(t) are independent via Wronskian.
4. **Higher order** — `y''' - y = 0` has solutions `eᵗ`, `e^(-t/2)cos(√3t/2)`, `e^(-t/2)sin(√3t/2)`. Compute the 3×3 Wronskian.
5. **Connection to matrices** — the Wronskian is just a determinant of a matrix whose entries are function values. Same theory, different vector space.

**Exercises:**

*Easy:* Compute the Wronskian of `f₁(t) = t` and `f₂(t) = t²` at t = 1. Are they linearly independent?

*Medium:* Show that `{e^t, e^(2t), e^(3t)}` are linearly independent by computing the Wronskian at t = 0.

*Challenge:* Given the ODE `y'' - 3y' + 2y = 0`, verify that `y₁ = e^t` and `y₂ = e^(2t)` are solutions by substitution. Then verify they form a basis for the solution space using the Wronskian.

---

## Task 22: Notebook 5.1 — Length and Dot Product in R^n

**Files:**
- Create: `notebooks/ch5_inner_product_spaces/5_1_length_and_dot_product.ipynb`
- Modify: `linalg_core/inner.py` (add `dot`, `norm`, `normalize`, `distance`, `angle`, `are_orthogonal`)

**Motivation Problem:**
"A search engine ranks documents by how 'similar' they are to a query. Both documents and queries are vectors (word frequency counts). The angle between them measures similarity. How do we compute angles between vectors?"

Document vector: `d = [3, 1, 0, 2]` (counts of 4 keywords). Query: `q = [1, 0, 0, 1]`. Cosine similarity = cos(angle between d and q).

**Build Section:**

1. **Dot product** — `u · v = u₁v₁ + u₂v₂ + ... + uₙvₙ`. Implement `dot(u, v)`.
2. **Properties** — commutative, distributive over addition, scalar factoring, `v · v ≥ 0` with equality iff v = 0.
3. **Norm (length)** — `‖v‖ = √(v · v)`. Implement `norm(v)`.
4. **Unit vectors** — `‖v‖ = 1`. Normalizing: `v/‖v‖`. Implement `normalize(v)`.
5. **Distance** — `d(u, v) = ‖u - v‖`. Implement `distance(u, v)`.
6. **Angle** — `cos θ = (u · v) / (‖u‖ · ‖v‖)`. Implement `angle(u, v)` returning radians.
7. **Orthogonality** — u ⊥ v iff `u · v = 0`. Implement `are_orthogonal(u, v)`.
8. **Cauchy-Schwarz Inequality** — `|u · v| ≤ ‖u‖ · ‖v‖`. Verify on random vectors.
9. **Triangle Inequality** — `‖u + v‖ ≤ ‖u‖ + ‖v‖`. Verify on random vectors.
10. **Solve the search problem** — compute cosine similarity between document and query.

**Verify:**
- `dot(u, v)` matches `np.dot`
- `norm(v)` matches `np.linalg.norm`
- Cauchy-Schwarz holds for 1000 random vector pairs
- Triangle Inequality holds for 1000 random vector pairs
- `angle(u, v)` matches `np.arccos(np.dot(u,v) / (np.linalg.norm(u) * np.linalg.norm(v)))`

**Visualize:**
- 2D: two vectors with the angle between them labeled
- 2D: orthogonal projection of u onto v (preview of Ch.5.3)

**Exercises:**

*Easy:* Find the angle between `u = [1, 2, 3]` and `v = [4, 5, 6]` in degrees.

*Medium:* Find a vector in R³ that is orthogonal to both `u = [1, 0, 1]` and `v = [0, 1, -1]`. (Hint: set up the system u·w = 0, v·w = 0.)

*Challenge:* Implement `cosine_similarity_matrix(documents)` that takes a list of document vectors and returns the n×n pairwise similarity matrix. Find the two most similar documents in a set of 5.

**Update `linalg_core/inner.py`:**
Add `dot`, `norm`, `normalize`, `distance`, `angle`, `are_orthogonal`.

---

## Task 23: Notebook 5.2 — Inner Product Spaces

**Files:**
- Create: `notebooks/ch5_inner_product_spaces/5_2_inner_product_spaces.ipynb`

**Motivation Problem:**
"The dot product works for Rⁿ. But what about measuring 'closeness' of polynomials or functions? We need a generalized notion of inner product that satisfies 4 axioms."

**Build Section:**

1. **The 4 axioms** — an inner product ⟨u, v⟩ must satisfy: (a) ⟨u, v⟩ = ⟨v, u⟩ (symmetry), (b) ⟨u+v, w⟩ = ⟨u,w⟩ + ⟨v,w⟩ (additivity), (c) ⟨cu, v⟩ = c⟨u,v⟩ (homogeneity), (d) ⟨v, v⟩ ≥ 0 with equality iff v = 0 (positive definiteness).
2. **Weighted dot product** — `⟨u, v⟩ = w₁u₁v₁ + w₂u₂v₂ + ...`. Verify axioms with weights [2, 1, 3].
3. **Integral inner product for functions** — `⟨f, g⟩ = ∫₀¹ f(t)g(t) dt`. Demo with polynomials using numerical integration.
4. **Norm and distance in general inner product spaces** — `‖v‖ = √⟨v,v⟩`, `d(u,v) = ‖u-v‖`.
5. **Orthogonality in general inner product spaces** — `⟨u, v⟩ = 0`. Demo: find two polynomials orthogonal under the integral inner product.
6. **Orthogonal complement** — `W⊥` is the set of all vectors orthogonal to every vector in W. If W is spanned by {w₁, ..., wₖ}, then v ∈ W⊥ iff ⟨v, wᵢ⟩ = 0 for all i.

**Exercises:**

*Easy:* Verify that the weighted inner product with weights [1, 2] satisfies all 4 axioms using `u = [3, 1]` and `v = [2, -1]`.

*Medium:* Using the integral inner product `⟨f, g⟩ = ∫₋₁¹ f(t)g(t) dt`, show that `f(t) = 1` and `g(t) = t` are orthogonal. (Use numerical integration.)

*Challenge:* Find the orthogonal complement of `W = span{[1, 1, 0, 0], [0, 0, 1, 1]}` in R⁴ with the standard dot product. Express your answer as a basis for W⊥.

---

## Task 24: Notebook 5.3 — Orthonormal Bases: Gram-Schmidt Process

**Files:**
- Create: `notebooks/ch5_inner_product_spaces/5_3_gram_schmidt_process.ipynb`
- Modify: `linalg_core/inner.py` (add `gram_schmidt`, `orthogonal_projection`)

**Motivation Problem:**
"Given a basis that's NOT orthogonal, how do we build an orthogonal (or orthonormal) one? This is the Gram-Schmidt process — the algorithm behind QR factorization, which is used in every serious linear algebra library."

**Build Section:**

1. **Orthogonal projection** — `proj_u(v) = (⟨v, u⟩ / ⟨u, u⟩) × u`. Implement `orthogonal_projection(v, u)`.
2. **Step 1 of Gram-Schmidt** — start with v₁ = w₁ (first basis vector, unchanged).
3. **Step 2** — v₂ = w₂ - proj_{v₁}(w₂). This makes v₂ orthogonal to v₁. Demo and verify `dot(v₁, v₂) ≈ 0`.
4. **Step 3** — v₃ = w₃ - proj_{v₁}(w₃) - proj_{v₂}(w₃). Orthogonal to both v₁ and v₂.
5. **General Gram-Schmidt** — implement `gram_schmidt(vectors)`. For each vector, subtract all projections onto previously orthogonalized vectors. Normalize at the end.
6. **Demo** — orthogonalize `{[1, 1, 0], [1, 0, 1], [0, 1, 1]}`. Show the step-by-step projections and subtractions.
7. **Fourier coefficients** — in an orthonormal basis Q, the coordinate of x is simply `⟨x, qᵢ⟩`. No system-solving needed. Demo.

**Verify:**
- All output pairs have dot product ≈ 0
- All output vectors have norm ≈ 1
- The output vectors span the same space as the input
- Compare against `np.linalg.qr` (Q matrix columns should match up to sign)

**Visualize:**
3D: show the original 3 basis vectors. Animate the Gram-Schmidt process: subtract projections, show the result becoming perpendicular. Color: original (red), orthogonalized (blue).

**Exercises:**

*Easy:* Apply Gram-Schmidt to `{[3, 4], [1, 0]}` to get an orthonormal basis for R².

*Medium:* Apply Gram-Schmidt to `{[1, 1, 0], [0, 1, 1], [1, 0, 1]}`. Verify all three orthogonality conditions and all three unit-norm conditions.

*Challenge:* Implement `qr_factorization(A)` using Gram-Schmidt. A = QR where Q is orthogonal and R is upper triangular. Verify `Q^T Q = I` and `Q R = A`. Compare against `np.linalg.qr`.

**Update `linalg_core/inner.py`:**
Add `gram_schmidt`, `orthogonal_projection`.

---

## Task 25: Notebook 5.4 — Mathematical Models and Least Squares Analysis

**Files:**
- Create: `notebooks/ch5_inner_product_spaces/5_4_least_squares_analysis.ipynb`
- Modify: `linalg_core/inner.py` (add `least_squares`)

**Motivation Problem:**
"A sensor takes noisy temperature readings every hour: (0, 32.1), (1, 33.5), (2, 36.2), (3, 40.1), (4, 45.3), (5, 51.0). You suspect a quadratic trend. But there's no parabola passing through all 6 noisy points. What's the *best* parabola?"

**Build Section:**

1. **Inconsistent systems** — more equations than unknowns, and no exact solution exists. But we want the "closest" solution.
2. **Least squares idea** — minimize `‖Ax - b‖²`. The residual `r = b - Ax̂` should be as small as possible.
3. **Normal equations** — the minimum is achieved when `A^T A x̂ = A^T b`. Derive by setting gradient to zero.
4. **Implement `least_squares(A, b)`** — compute `A^T A` and `A^T b` using existing `multiply` and `transpose`, then solve using `lu_factorize` + forward/back substitution.
5. **Linear regression** — fit `y = a + bx` to the temperature data. Build the Vandermonde matrix, solve normal equations.
6. **Quadratic regression** — fit `y = a + bx + cx²`. Build the 6×3 Vandermonde matrix.
7. **Orthogonal projection interpretation** — `Ax̂` is the projection of b onto the column space of A. The residual `b - Ax̂` is orthogonal to every column of A. Verify: `A^T(b - Ax̂) ≈ 0`.

**Verify:**
- Residual is orthogonal to every column of A: `A^T @ (b - A @ x_hat)` < epsilon
- Compare against `np.linalg.lstsq`
- Linear fit: slope and intercept match `np.polyfit(x, y, 1)`
- Quadratic fit: coefficients match `np.polyfit(x, y, 2)`

**Visualize:**
Plot data points as scatter, linear fit as a line, quadratic fit as a curve, cubic fit as a curve. Show residual bars from each data point to the fitted curve. Include R² value for each fit.

**Exercises:**

*Easy:* Find the best-fit line `y = a + bx` for the data points (1, 2), (2, 3), (3, 5), (4, 4).

*Medium:* Find the best-fit parabola for (0, 1), (1, 3), (2, 7), (3, 13), (4, 21). Compare the residuals of the linear and quadratic fits. Which is better?

*Challenge:* Fit polynomials of degree 1, 2, 3, 4, 5 to the temperature data. Plot all fits. Compute the residual norm for each. At what degree does increasing the polynomial stop significantly improving the fit? Implement a simple AIC or BIC criterion to pick the best degree.

**Update `linalg_core/inner.py`:**
Add `least_squares`.

---

## Task 26: Notebook 5.5 — Applications of Inner Product Spaces

**Files:**
- Create: `notebooks/ch5_inner_product_spaces/5_5_applications_of_inner_product_spaces.ipynb`
- Modify: `linalg_core/inner.py` (add `cross_product`)

**Motivation Problem:**
"A wrench applies a force F at the end of a lever arm r. The torque — the rotational force — is the cross product τ = r × F. How do we compute cross products, and what geometric information do they encode?"

**Build Section:**

1. **Cross product** — for u, v ∈ R³: `u × v = [u₂v₃ - u₃v₂, u₃v₁ - u₁v₃, u₁v₂ - u₂v₁]`. Implement `cross_product(u, v)`.
2. **Properties** — anticommutative (`u × v = -(v × u)`), not associative, distributive, `u × u = 0`.
3. **Geometric meaning** — `u × v` is perpendicular to both u and v. Its magnitude equals the area of the parallelogram formed by u and v.
4. **Parallelogram area** — `area = ‖u × v‖`. Demo.
5. **Parallelepiped volume** — `V = |u · (v × w)|` (triple scalar product). Demo.
6. **Torque calculation** — compute τ = r × F for the wrench problem.
7. **Connection to determinants** — the cross product can be written as a formal determinant: `u × v = det([[i, j, k], [u₁, u₂, u₃], [v₁, v₂, v₃]])`.

**Verify:**
- `cross_product(u, v)` is orthogonal to both u and v
- `norm(cross_product(u, v))` equals parallelogram area
- `cross_product(u, v)` matches `np.cross(u, v)`
- Triple scalar product matches det of the 3×3 matrix with u, v, w as rows

**Visualize:**
- 3D: two vectors and their cross product, all originating from the same point
- 3D: parallelogram shaded, area labeled
- 3D: parallelepiped rendered, volume labeled

**Exercises:**

*Easy:* Compute `[1, 2, 3] × [4, 5, 6]`. Verify the result is orthogonal to both input vectors.

*Medium:* Find the area of the triangle with vertices A = (1, 0, 0), B = (0, 1, 0), C = (0, 0, 1). (Hint: area = ½‖AB × AC‖.)

*Challenge:* Compute the volume of the parallelepiped defined by `u = [1, 0, 2]`, `v = [0, 1, -1]`, `w = [3, 1, 5]`. Verify using (a) the triple scalar product and (b) the determinant of the 3×3 matrix [u; v; w]. When is the volume zero?

**Update `linalg_core/inner.py`:**
Add `cross_product`.

---

## Execution Strategy

The 27 tasks (Task 0 + Tasks 1-26) can be partially parallelized by chapter:

- **Task 0** must complete first (shared package scaffold)
- **Chapter 1 (Tasks 1-3)** are sequential (each builds on prior elimination code)
- **Chapter 2 (Tasks 4-9)** sequential, depends on Chapter 1
- **Chapter 3 (Tasks 10-13)** sequential, depends on Chapter 2
- **Chapter 4 (Tasks 14-21)** sequential, depends on Chapter 3
- **Chapter 5 (Tasks 22-26)** sequential, depends on Chapter 4

Within each chapter, notebooks are sequential because later ones import functions added by earlier ones.

**Recommended approach:** Execute Task 0, then work chapter by chapter. Each notebook task has a clear deliverable: one `.ipynb` file + updated `linalg_core` module.
