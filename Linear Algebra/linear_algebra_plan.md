# Linear Algebra Through Code: A Multi-Language Learning Plan
## Larson, Elementary Linear Algebra 8e, Chapters 1-5

---

## Governing Principles

### Code as Proof Machine

Every algorithm you implement is a hypothesis about the math. You run it, compare against a known-correct reference (NumPy/SciPy), and any mismatch pinpoints a concept you do not yet own. The friction of writing it yourself is the entire point. Never import a library to do the computation; use libraries only to verify your output. The moment NumPy does the work, the project becomes a script, not a learning tool.

### Exact Mode vs Float Mode

Maintain two mental modes throughout:
- **Exact mode** (for learning): work with small integer examples where you can verify by hand. This isolates conceptual errors.
- **Float mode** (for robustness): add partial pivoting and epsilon tolerance (`1e-9`), test on random floating-point matrices. This isolates numerical errors.

Never use `== 0` to check a pivot. Always use `fabs(value) < EPSILON`. Gaussian elimination can lose all significant digits if pivots are chosen naively. Partial pivoting (selecting the row with the largest absolute value in the pivot column) prevents division by near-zero and is why production solvers survive ill-conditioned systems.

### Property-Based Verification

After every implementation, assert the mathematical invariants:
- Gaussian elimination: plug the solution back into the original system
- Inverse: A * A_inv = I within tolerance
- Determinant: det(AB) = det(A) * det(B)
- Rank-nullity: rank(A) + nullity(A) = n
- Gram-Schmidt: all output pairs orthogonal, all norms equal to 1
- Least squares: residual (b - Ax_hat) is orthogonal to every column of A

---

## Language Architecture

Four languages, each with a distinct role, wired together so they actually call each other. This is not cosmetic. Each boundary forces you to understand something the math alone never teaches.

### C: The Bedrock Engine

C owns raw memory. You implement every algorithm against flat arrays (`double*`) with explicit row/column indexing. No classes, no RAII, no templates. This forces you to:
- Manage memory manually (malloc/free for every matrix)
- Confront cache locality (row-major vs column-major layout matters for multiplication performance)
- See floating-point behavior at the metal level (signed zeros, NaN propagation, precision loss)

The C layer compiles to a shared library (`liblinalgcore.so` / `liblinalgcore.dylib`) that every other language consumes.

### C++: The Typed Wrapper

C++ wraps the C engine with a `Matrix` class that provides RAII (constructor/destructor handle allocation), operator overloads (`+`, `*`, `<<`), and const-correctness. The C++ layer:
- Links against the C shared library
- Adds no new algorithms; it only wraps C functions with safe interfaces
- Proves you understand the boundary between raw computation and abstraction

This is also where you write Catch2 unit tests that exercise every C function through the C++ wrapper.

### Python: The Proof Harness

Python calls the C shared library via `ctypes`. This forces you to:
- Understand the C ABI (how to pass a `double*` from Python, how to read results back)
- Marshal data between Python lists/NumPy arrays and raw C pointers

Python's job is exclusively verification and application-layer logic:
- Compare your C engine output against NumPy/SciPy for every algorithm
- Run property-based tests (the invariants listed above)
- Build matplotlib visualizations for geometric intuition
- Implement the application projects (curve fitting, Markov chains, regression)

### TypeScript: The Interactive Visualizer

TypeScript calls the C/C++ engine compiled to WebAssembly via Emscripten. This gives you browser-based interactive visualizations where you can:
- Manipulate vectors/matrices with sliders and see transformations in real time
- Step through Gaussian elimination visually
- Watch Gram-Schmidt orthogonalization happen geometrically

The WASM bridge forces you to understand how compiled native code runs in a sandboxed environment: memory is a flat `ArrayBuffer`, pointers become byte offsets, and you manage the heap manually from JS/TS.

### The Interop Chain

```
┌──────────────────────────────────────────────────────────────┐
│                    TypeScript (Browser)                       │
│         Interactive visualizations, step-through UIs         │
│                          │                                   │
│                    calls via WASM                             │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              C/C++ compiled to WebAssembly              │  │
│  │           (Emscripten: emcc -o engine.js)              │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     Python (Desktop)                         │
│      Proof harness, NumPy cross-checks, matplotlib plots     │
│                          │                                   │
│                   calls via ctypes                            │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │            C shared library (.so / .dylib)              │  │
│  │        Core algorithms on raw double* arrays           │  │
│  └────────────────────────────────────────────────────────┘  │
│                          ▲                                   │
│                   links against                               │
│                          │                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              C++ wrapper + Catch2 tests                 │  │
│  │       RAII Matrix class, operator overloads             │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
linear-algebra/
├── engine/                          # C core library
│   ├── include/
│   │   ├── la_matrix.h              # Matrix struct, alloc/free, print
│   │   ├── la_elimination.h         # Ch.1: REF, RREF, solve, partial pivoting
│   │   ├── la_ops.h                 # Ch.2: add, multiply, transpose, inverse, LU
│   │   ├── la_determinant.h         # Ch.3: cofactor det, elimination det
│   │   ├── la_vecspace.h            # Ch.4: rank, nullity, null space, col space, change of basis
│   │   └── la_inner.h              # Ch.5: dot, norm, Gram-Schmidt, least squares
│   ├── src/                         # Implementations (.c files)
│   ├── Makefile                     # Builds liblinalgcore.so and liblinalgcore.a
│   └── config.h                     # EPSILON constant, row-major macros
│
├── wrapper/                         # C++ typed wrapper
│   ├── include/
│   │   └── Matrix.h                 # RAII class wrapping la_matrix.h
│   ├── src/
│   │   └── Matrix.cpp
│   ├── tests/                       # Catch2 unit tests per chapter
│   │   ├── test_ch1_systems.cpp
│   │   ├── test_ch2_matrices.cpp
│   │   ├── test_ch3_determinants.cpp
│   │   ├── test_ch4_vecspaces.cpp
│   │   └── test_ch5_inner.cpp
│   └── CMakeLists.txt               # Links against liblinalgcore
│
├── bindings/                        # Python ctypes bridge
│   ├── linalgcore.py                # ctypes wrapper: load .so, define argtypes/restypes
│   └── verify/                      # NumPy cross-verification scripts
│       ├── verify_ch1.py
│       ├── verify_ch2.py
│       ├── verify_ch3.py
│       ├── verify_ch4.py
│       └── verify_ch5.py
│
├── apps/                            # Python application projects
│   ├── curve_fitter.py              # Ch.1: polynomial curve fitting
│   ├── network_flow.py              # Ch.1: traffic network solver
│   ├── hill_cipher.py               # Ch.2: encode/decode messages
│   ├── markov_chain.py              # Ch.2: state simulation + convergence
│   ├── geo_engine.py                # Ch.3: area, volume, collinearity
│   ├── rank_explorer.py             # Ch.4: rank-nullity verification tool
│   ├── change_of_basis_viz.py       # Ch.4: coordinate grid overlay
│   └── regression.py                # Ch.5: least squares curve fitting
│
├── web/                             # TypeScript interactive visualizations
│   ├── src/
│   │   ├── wasm-bridge.ts           # Load WASM module, expose typed API
│   │   ├── elimination-stepper.ts   # Ch.1: step through Gaussian elimination
│   │   ├── transform-playground.ts  # Ch.2: real-time matrix transformation
│   │   ├── det-visualizer.ts        # Ch.3: parallelogram/parallelepiped area/volume
│   │   ├── basis-explorer.ts        # Ch.4: interactive change of basis
│   │   └── gram-schmidt-3d.ts       # Ch.5: 3D orthogonalization animation
│   ├── wasm/
│   │   └── build.sh                 # emcc compile script -> engine.js + engine.wasm
│   ├── tsconfig.json
│   └── index.html                   # Entry point linking all visualizers
│
└── README.md
```

---

## Phase 1: Systems of Linear Equations (Chapter 1)

### Topics Covered

- Linear equations in n variables, solution sets, parametric representations
- Consistent vs inconsistent systems; three solution types
- Row-echelon form, reduced row-echelon form
- Gaussian elimination with back-substitution
- Gauss-Jordan elimination
- Homogeneous systems, trivial vs nontrivial solutions
- Applications: polynomial curve fitting, network analysis

### C Engine: `la_elimination.h / .c`

Define a `LAMatrix` struct:

```c
typedef struct {
    double* data;    // row-major flat array
    int rows;
    int cols;
} LAMatrix;
```

Implement these functions:
- `la_matrix_new(rows, cols)` / `la_matrix_free(mat)`: allocation and cleanup
- `la_matrix_get(mat, i, j)` / `la_matrix_set(mat, i, j, val)`: access via `data[i * cols + j]`
- `la_swap_rows(mat, i, j)`: elementary row operation
- `la_scale_row(mat, i, scalar)`: elementary row operation
- `la_add_scaled_row(mat, target, source, scalar)`: elementary row operation
- `la_to_ref(mat)`: Gaussian elimination with partial pivoting to row-echelon form
- `la_to_rref(mat)`: Gauss-Jordan to reduced row-echelon form
- `la_solve(augmented, result, solution_type)`: classify and extract solution

Partial pivoting: before eliminating in column k, scan rows k..n for the largest `fabs()` in that column and swap it into the pivot position. This is a single addition to the naive algorithm that prevents catastrophic cancellation.

### C++ Wrapper

The `Matrix` class wraps `LAMatrix*` with:
- Constructor/destructor managing `la_matrix_new` / `la_matrix_free`
- `operator()(i, j)` for element access
- `ref()`, `rref()`, `solve()` methods that call the C functions
- `operator<<` for formatted printing

### Python Proof Harness: `verify_ch1.py`

```python
import ctypes, numpy as np

lib = ctypes.CDLL('./liblinalgcore.so')
# ... define argtypes/restypes ...

# For each test matrix:
# 1. Solve with your C engine via ctypes
# 2. Solve with numpy.linalg.solve
# 3. Assert solutions match within tolerance
# 4. Plug C solution back into original system, assert residual < epsilon
```

Test cases:
- 3x3 system with unique solution
- 4x3 underdetermined system (infinite solutions)
- Inconsistent system (no solution)
- Homogeneous system with nontrivial solution (more variables than equations)

### Python Application: Polynomial Curve Fitter (`apps/curve_fitter.py`)

Section 1.3 lists polynomial curve fitting as a core application.

1. Accept n data points (x_i, y_i)
2. Build the Vandermonde system (each row is [1, x_i, x_i^2, ..., x_i^(n-1)])
3. Call your C solver via ctypes
4. Plot the data and the fitted polynomial (matplotlib)
5. Feed an underdetermined case and confirm parametric output

### Python Application: Network Flow Solver (`apps/network_flow.py`)

Model a small traffic network (4-5 nodes) with flow conservation constraints. Each node produces one equation: flow in = flow out. Solve the resulting system and interpret the free variables as adjustable flow rates.

### TypeScript Visualizer: Elimination Stepper (`web/src/elimination-stepper.ts`)

Compile the C engine to WASM. Build a browser UI where:
- The user enters a system of equations
- Each click of "Next Step" performs one elementary row operation
- The matrix display highlights the current pivot, the row being modified, and shows the operation name
- Color-codes zero entries as they appear during elimination
- Displays solution classification at the end

This makes the mechanical process of elimination visual in a way that hand computation and terminal output cannot.

---

## Phase 2: Matrices (Chapter 2)

### Topics Covered

- Matrix equality, addition, scalar multiplication, matrix multiplication (row-column rule)
- Non-commutativity of multiplication, identity matrix, transpose properties
- Additive/multiplicative properties, zero matrix, cancellation pitfalls
- Inverse (definition, uniqueness, 2x2 formula, Gauss-Jordan method)
- Elementary matrices, row equivalence, conditions for invertibility
- LU-factorization (Doolittle's method)
- Markov chains: stochastic matrices, steady-state vectors, absorbing chains
- Applications: cryptography (Hill cipher), Leontief input-output models

### C Engine: `la_ops.h / .c`

Extend with:
- `la_matrix_add(A, B, result)`, `la_matrix_scalar_mul(A, scalar, result)`
- `la_matrix_mul(A, B, result)`: triple loop, row-column rule. Implement both `i-j-k` and `i-k-j` loop orders so you can benchmark cache effects.
- `la_matrix_transpose(A, result)`
- `la_matrix_inverse(A, result)`: augment [A | I], call `la_to_rref`, extract right half. Return error code if singular.
- `la_lu_factorize(A, L, U)`: Doolittle's method. Store multipliers in L as you eliminate.
- `la_forward_sub(L, b, y)` and `la_back_sub(U, y, x)`: solve via LU in two passes

### C++ Wrapper

Add operator overloads: `Matrix operator+(const Matrix&)`, `Matrix operator*(const Matrix&)`, `Matrix operator*(double)`. Add `inverse()`, `lu()`, `transpose()` methods.

### Python Proof Harness: `verify_ch2.py`

- `A * inverse(A)` equals identity within tolerance
- `L * U` reconstructs original matrix
- LU-based solve matches Gaussian elimination solve for same system
- `(A * B).transpose() == B.transpose() * A.transpose()`
- Verify non-commutativity: find A, B where A*B != B*A

### Python Application: Hill Cipher (`apps/hill_cipher.py`)

Section 2.6 covers cryptography.

1. Map letters to numbers (A=0, B=1, ..., Z=25)
2. Choose an invertible nxn key matrix K
3. Encrypt: break plaintext into n-vectors, multiply each by K (mod 26)
4. Decrypt: multiply ciphertext vectors by K^(-1) (mod 26)
5. If K is singular, refuse the key and explain why

If your inverse implementation is wrong, the decoded message is garbage. This is immediate, visceral feedback that no unit test can replicate.

### Python Application: Markov Chain Simulator (`apps/markov_chain.py`)

Section 2.5 covers stochastic matrices.

1. Define a transition matrix P (e.g., weather: sunny/cloudy/rainy)
2. Iterate state = P * state for n steps using your C engine
3. Plot probability distributions over time (matplotlib line chart)
4. Compute steady-state by solving (P - I)x = 0 with your Ch.1 solver
5. Verify: the iterated state converges to the algebraically computed steady-state

This directly parallels discrete-time state updates x[k+1] = Ax[k] in control systems.

### TypeScript Visualizer: Transform Playground (`web/src/transform-playground.ts`)

A 2D canvas where:
- A unit square (or set of points) is displayed
- The user enters a 2x2 matrix via input fields
- The transformed shape is drawn in real time as values change
- Shows determinant (area scaling factor) live
- Demonstrates non-commutativity: apply A then B vs B then A, see different results
- Toggle to show column vectors of the matrix as arrows (where the basis vectors land)

---

## Phase 3: Determinants (Chapter 3)

### Topics Covered

- Determinant of 1x1 and 2x2 matrices
- Minors, cofactors, cofactor expansion
- Determinant of triangular matrices, recursive definition for any size
- Effect of elementary row operations on determinants
- det(AB) = det(A)det(B), det(A^T) = det(A), det(A^(-1)) = 1/det(A)
- Conditions for zero determinant
- Cramer's Rule, adjoint matrix, inverse via adjoint
- Geometric applications: triangle area, tetrahedron volume, collinearity, line/plane equations

### C Engine: `la_determinant.h / .c`

Implement two determinant methods:
1. `la_det_cofactor(A)`: recursive cofactor expansion along first row. Allocate sub-matrices for minors at each recursion level. This matches Larson's definition directly.
2. `la_det_elimination(A)`: copy A, reduce to upper triangular tracking sign flips (row swaps negate) and scalar multiplications, multiply the diagonal. O(n^3) vs O(n!) for cofactor.

Also:
- `la_cofactor_matrix(A, result)`: matrix of cofactors
- `la_adjoint(A, result)`: transpose of cofactor matrix
- `la_inverse_adjoint(A, result)`: A^(-1) = (1/det(A)) * adj(A)
- `la_cramers_rule(A, b, result)`: replace columns, compute determinant ratios

### C++ Wrapper

Add `det()` method (defaults to elimination-based), `det_cofactor()` for explicit recursive version. Add `adjoint()`, `cramers_solve(b)`.

### Python Proof Harness: `verify_ch3.py`

- Both determinant methods agree on the same matrix
- `det(A * B) == det(A) * det(B)` within tolerance
- `det(transpose(A)) == det(A)`
- `det(inverse(A)) == 1.0 / det(A)`
- Inverse via adjoint matches inverse via Gauss-Jordan
- Cramer's Rule solution matches Gaussian elimination solution

### Performance Benchmark

In Python, time both C determinant functions on matrices from 2x2 to 12x12. Cofactor expansion is O(n!) and will visibly stall around 10-12. Elimination is O(n^3) and remains instant. Plot the timing curves. This makes algorithmic complexity physical.

### Python Application: Geometric Engine (`apps/geo_engine.py`)

Section 3.4 applications are all geometric.

1. Area of a triangle from three 2D points (half the absolute 3x3 determinant)
2. Volume of a tetrahedron from four 3D points
3. Collinearity test for three points (det = 0 means collinear)
4. Two-point form of a line equation via determinant
5. Three-point form of a plane equation via determinant
6. Visualize with matplotlib 2D and 3D

This grounds determinants in geometry: det = 0 means degeneracy (collinear/coplanar), which is the same thing as linear dependence.

### TypeScript Visualizer: Determinant Visualizer (`web/src/det-visualizer.ts`)

2D mode:
- Two draggable vectors from the origin
- The parallelogram formed by them is shaded
- Its signed area (the 2x2 determinant) updates live
- When vectors become parallel (dependent), area collapses to zero visually

3D mode (using a simple projection or a lightweight 3D library):
- Three draggable vectors
- The parallelepiped is rendered
- Volume (triple scalar product / 3x3 determinant) updates live

---

## Phase 4: Vector Spaces (Chapter 4)

### Topics Covered

- Vectors in R^n, vector addition, scalar multiplication, linear combinations
- Vector space definition (10 axioms), examples (R^n, matrices, polynomials, continuous functions)
- Subspaces, subspace test, span of a set
- Linear independence/dependence, testing via homogeneous system
- Basis (linearly independent spanning set), dimension
- Row space, column space, null space
- Rank, nullity, Rank-Nullity Theorem: rank(A) + nullity(A) = n
- Coordinate representation, transition matrices (change of basis)
- Applications: differential equations, Wronskian

### C Engine: `la_vecspace.h / .c`

- `la_rank(A)`: RREF the matrix, count pivot rows
- `la_nullity(A)`: n - rank(A)
- `la_null_space(A, basis_out, num_basis)`: identify free variables from RREF, construct basis vectors for the solution space of Ax = 0
- `la_column_space(A, basis_out, num_basis)`: pivot columns of A (identified via RREF) form the basis
- `la_row_space(A, basis_out, num_basis)`: nonzero rows of RREF
- `la_is_independent(vectors, num_vectors, dim)`: stack as rows, RREF, check if every row has a pivot
- `la_is_in_span(v, vectors, num_vectors, dim)`: augment and check consistency
- `la_change_of_basis(B_old, B_new, transition, n)`: compute transition matrix via Gauss-Jordan on [B_new | B_old]

### C++ Wrapper

Add methods: `rank()`, `nullity()`, `null_space()`, `column_space()`, `row_space()`. Add static method `Matrix::change_of_basis(old_basis, new_basis)`.

### Python Proof Harness: `verify_ch4.py`

- rank(A) + nullity(A) = n for every test matrix (the Rank-Nullity Theorem)
- Every null space basis vector satisfies Ax = 0
- Column space basis vectors are actual columns of A
- 4 vectors in R^3 are always dependent (pigeonhole)
- Transition matrix: P * P_inverse = I
- Coordinate round-trip: convert to new basis, convert back, recover original

### Python Application: Rank-Nullity Explorer (`apps/rank_explorer.py`)

An interactive tool that:
1. Takes any matrix A
2. Displays rank(A), nullity(A), n (columns)
3. Asserts the Rank-Nullity Theorem
4. Prints bases for row space, column space, and null space
5. Verifies every null space vector against Ax = 0
6. Acts as your regression test harness for all Ch.4 implementations

### Python Application: Change of Basis Visualizer (`apps/change_of_basis_viz.py`)

In R^2:
1. Define standard basis and a custom basis B'
2. Compute transition matrix P via your C engine
3. Express a vector in B' coordinates, multiply by P, verify recovery of standard coordinates
4. Plot both coordinate grids overlaid (matplotlib)

### TypeScript Visualizer: Basis Explorer (`web/src/basis-explorer.ts`)

Interactive 2D canvas:
- The standard grid is drawn in light gray
- The user defines two basis vectors by dragging endpoints
- The custom basis grid is drawn in a second color, overlaid
- A movable point shows its coordinates in both bases simultaneously
- When basis vectors become dependent, the grid collapses to a line (visually shows dimension drop)

---

## Phase 5: Inner Product Spaces (Chapter 5)

### Topics Covered

- Dot product, properties, length/norm, unit vectors, distance
- Angle between vectors, orthogonality
- Cauchy-Schwarz Inequality, Triangle Inequality
- Inner product spaces (4 axioms), general examples
- Orthogonal complement
- Orthogonal/orthonormal sets and bases, Fourier coefficients
- Orthogonal projection, Gram-Schmidt process
- Least squares regression, normal equations (A^T A x = A^T b)
- Polynomial regression, Fourier approximation
- Cross product in R^3, geometric properties (parallelogram area, parallelepiped volume)

### C Engine: `la_inner.h / .c`

- `la_dot(u, v, n)`: dot product of two vectors
- `la_norm(v, n)`: Euclidean norm
- `la_normalize(v, result, n)`: unit vector
- `la_distance(u, v, n)`: norm of difference
- `la_angle(u, v, n)`: arccos(dot / (norm * norm))
- `la_are_orthogonal(u, v, n)`: fabs(dot) < EPSILON
- `la_cross_product(u, v, result)`: R^3 only
- `la_gram_schmidt(vectors, result, num_vectors, dim)`: takes a basis, outputs orthonormal basis
- `la_orthogonal_projection(v, subspace_basis, num_basis, dim, result)`: project v onto subspace
- `la_least_squares(A, b, result)`: form A^T*A and A^T*b using `la_matrix_mul` and `la_matrix_transpose`, solve using `la_lu_factorize` + forward/back substitution

### C++ Wrapper

Free functions: `dot(v1, v2)`, `norm(v)`, `normalize(v)`, `angle(v1, v2)`, `cross(v1, v2)`. Matrix methods: `gram_schmidt()`, `least_squares_solve(b)`.

### Python Proof Harness: `verify_ch5.py`

- Cauchy-Schwarz: `abs(dot(u,v)) <= norm(u) * norm(v)` for many random vectors
- Triangle Inequality: `norm(u+v) <= norm(u) + norm(v)`
- Gram-Schmidt output: all pairs have dot product = 0 within tolerance, all norms = 1
- Least squares: residual vector (b - A*x_hat) is orthogonal to every column of A
- Compare least squares output against `numpy.linalg.lstsq`

### Python Capstone: Least Squares Regression (`apps/regression.py`)

This is the flagship project. It ties together nearly every chapter.

1. Load real data with noise (sensor readings, stock prices, anything messy)
2. Build the Vandermonde matrix A for polynomial degree d
3. Solve the normal equations A^T A x = A^T b via your C LU solver
4. Fit linear (d=1), quadratic (d=2), and cubic (d=3) models
5. Compute residuals, plot data points + fitted curves + residual bars
6. Deliberately overfit (d = n-1) and observe what happens
7. Compare all results against numpy.linalg.lstsq

Why this is the capstone: the normal equations require matrix multiplication and transpose (Ch.2), checking if A^T*A is invertible requires determinants (Ch.3), the column space of A determines what projections are possible (Ch.4), and orthogonal projection is the geometric meaning of least squares (Ch.5).

### TypeScript Visualizer: Gram-Schmidt 3D (`web/src/gram-schmidt-3d.ts`)

An interactive 3D scene (Three.js or a lightweight alternative, compiled from C via WASM for the math):
- The user defines 3 linearly independent vectors by adjusting sliders
- Clicking "Step" advances Gram-Schmidt one iteration:
  - Shows the projection of the current vector onto the previous orthogonal vectors
  - Subtracts the projection (animated)
  - Normalizes the result (animated)
- Original vectors in one color, orthogonalized result in another
- At each step, displays dot products (approaching zero) and norms (approaching one)

---

## How Languages Call Each Other: Implementation Notes

### C -> Shared Library

```makefile
# engine/Makefile
CC = gcc
CFLAGS = -O2 -fPIC -Wall -Wextra -std=c11
SOURCES = $(wildcard src/*.c)
OBJECTS = $(SOURCES:.c=.o)

liblinalgcore.so: $(OBJECTS)
	$(CC) -shared -o $@ $^

liblinalgcore.a: $(OBJECTS)
	ar rcs $@ $^
```

### C++ -> Links Against C

```cmake
# wrapper/CMakeLists.txt
add_library(linalg_wrapper Matrix.cpp)
target_link_libraries(linalg_wrapper PRIVATE ${PROJECT_SOURCE_DIR}/../engine/liblinalgcore.a)
target_include_directories(linalg_wrapper PUBLIC ../engine/include)

add_executable(tests test_ch1_systems.cpp test_ch2_matrices.cpp ...)
target_link_libraries(tests PRIVATE linalg_wrapper Catch2::Catch2WithMain)
```

In `Matrix.h`, the C functions are declared with `extern "C"`:

```cpp
extern "C" {
    #include "la_matrix.h"
    #include "la_elimination.h"
    #include "la_ops.h"
    // ...
}
```

### Python -> Calls C via ctypes

```python
# bindings/linalgcore.py
import ctypes, os

lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), '..', 'engine', 'liblinalgcore.so'))

# Example: la_matrix_mul(A, B, result)
lib.la_matrix_mul.argtypes = [
    ctypes.POINTER(LAMatrix),
    ctypes.POINTER(LAMatrix),
    ctypes.POINTER(LAMatrix)
]
lib.la_matrix_mul.restype = ctypes.c_int

def multiply(A_data, B_data):
    # Marshal Python lists -> C LAMatrix structs
    # Call lib.la_matrix_mul
    # Marshal C result -> Python list
    # Return
    ...
```

Every `verify_*.py` and `apps/*.py` file imports from `linalgcore.py`. The marshal/unmarshal boundary is where you learn the C ABI.

### TypeScript -> Calls C via WebAssembly

```bash
# web/wasm/build.sh
emcc \
    ../../engine/src/*.c \
    -o ../dist/engine.js \
    -s EXPORTED_FUNCTIONS="['_la_matrix_new','_la_matrix_free','_la_to_rref','_la_matrix_mul',...]" \
    -s EXPORTED_RUNTIME_METHODS="['ccall','cwrap','getValue','setValue']" \
    -s MODULARIZE=1 \
    -s EXPORT_NAME="LinAlgEngine" \
    -O2
```

```typescript
// web/src/wasm-bridge.ts
import LinAlgEngine from '../dist/engine.js';

let engine: any;

export async function init() {
    engine = await LinAlgEngine();
}

export function createMatrix(rows: number, cols: number, data: number[]): number {
    const ptr = engine._la_matrix_new(rows, cols);
    // Write data into WASM heap
    const dataPtr = engine._la_matrix_data_ptr(ptr);
    for (let i = 0; i < data.length; i++) {
        engine.HEAPF64[dataPtr / 8 + i] = data[i];
    }
    return ptr; // pointer is just a number in WASM
}

export function toRREF(matPtr: number): void {
    engine._la_to_rref(matPtr);
}

export function freeMatrix(matPtr: number): void {
    engine._la_matrix_free(matPtr);
}
```

Each TypeScript visualizer imports from `wasm-bridge.ts` and never reimplements any algorithm. The same C code that Python verifies against NumPy is the same C code running in the browser.

---

## The Proof Loop (Apply Per Topic)

Before writing a single line of code for any section:

1. **Read the definition** in Larson, in full, mathematically.
2. **Work 2-3 problems by hand.** No shortcuts. This isolates "I misread the definition" from "I coded it wrong."
3. **Identify the algorithm step by step.** Not just "Gaussian elimination" but: which row do I swap? What do I multiply by? What does this operation preserve?
4. **Implement in C.** Raw arrays, no abstractions. Every index computation is explicit.
5. **Wrap in C++.** Add the safe interface. Run Catch2 tests.
6. **Verify in Python.** Call via ctypes, compare against NumPy. Assert mathematical invariants.
7. **Build one visualization or application.** This is where geometric/applied intuition forms.
8. **If any verification fails:** the mismatch is not a "bug to fix." It is a concept to investigate. Trace the discrepancy back to the specific mathematical property you violated. That investigation is where the actual learning happens.

---

## The One Rule

Never import NumPy, Eigen, LAPACK, or any linear algebra library to do the computation. Use them only in the `verify/` directory to check your answers. The moment a library does the work, the project becomes a script instead of a proof. Every mismatch between your engine's output and NumPy's is a concept you have not yet fully internalized.
