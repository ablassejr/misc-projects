# Linear Algebra Through Code

A multi-language linear algebra engine covering Larson's *Elementary Linear Algebra* (8th Edition), Chapters 1-5.

Every algorithm is implemented from scratch in C++ against raw `double*` arrays with `extern "C"` linkage. A C++ `Matrix` wrapper provides RAII and Catch2 tests. Python verifies against NumPy via ctypes. TypeScript visualizes via WebAssembly. **No library ever does the computation** -- libraries only verify your output.

## Architecture

```
                    TypeScript (Browser)
              Interactive visualizations
                        |
                   calls via WASM
                        v
              C++ compiled to WebAssembly
                  (Emscripten: em++)

                    Python (Desktop)
         Proof harness, NumPy cross-checks
                        |
                  calls via ctypes
                        v
             C++ shared library (.dylib)
         Core algorithms on raw double*
         (extern "C" linkage for FFI)
                        ^
                  links against
                        |
             C++ wrapper + Catch2 tests
            RAII Matrix class, overloads
```

## Repository Structure

```
engine/                     C++ core library (extern "C" API)
  include/                  Headers with function signatures
    la_config.h             EPSILON, LA_IDX macro
    la_matrix.h             LAMatrix struct, lifecycle
    la_elimination.h        Ch.1: REF, RREF, solve
    la_ops.h                Ch.2: add, mul, transpose, inverse, LU
    la_determinant.h        Ch.3: cofactor det, elimination det, Cramer
    la_vecspace.h           Ch.4: rank, nullity, null/col/row space
    la_inner.h              Ch.5: dot, norm, Gram-Schmidt, least squares
  src/                      Implementations (.cpp files)
  Makefile                  Builds liblinalgcore.dylib and .a

wrapper/                    C++ typed wrapper
  include/Matrix.h          RAII class wrapping la_matrix.h
  src/Matrix.cpp
  tests/                    Catch2 unit tests per chapter
  CMakeLists.txt            Links against liblinalgcore

bindings/                   Python ctypes bridge
  linalgcore.py             Load .dylib, define argtypes/restypes
  verify/                   NumPy cross-verification scripts

apps/                       Python application projects
  hill_cipher.py            Ch.2: encode/decode messages
  markov_chain.py           Ch.2: state simulation + convergence
  geo_engine.py             Ch.3: area, volume, collinearity
  rank_explorer.py          Ch.4: rank-nullity verification tool
  regression.py             Ch.5: least squares curve fitting (capstone)

web/                        TypeScript interactive visualizations
  src/wasm-bridge.ts        Load WASM module, expose typed API
  src/elimination-stepper   Ch.1: step through Gaussian elimination
  src/transform-playground  Ch.2: real-time matrix transformation
  src/det-visualizer        Ch.3: parallelogram/parallelepiped area
  src/basis-explorer        Ch.4: interactive change of basis
  src/gram-schmidt-3d       Ch.5: 3D orthogonalization animation
  wasm/build.sh             Emscripten compile script
```

## The Proof Loop

Apply this loop for every function you implement. No shortcuts.

### 1. Read the definition

Open Larson to the relevant section. Read the definition in full, mathematically. Not a summary, not a blog post -- the actual textbook definition with all its conditions.

### 2. Work problems by hand

Do 2-3 problems with pencil and paper. This isolates "I misread the definition" from "I coded it wrong." If you can't solve it by hand, you aren't ready to code it.

### 3. Identify the algorithm step by step

Not just "Gaussian elimination" but: which row do I swap? What do I multiply by? What does this operation preserve? Write the steps in comments before writing any code.

### 4. Implement in C++

Open `engine/src/la_<chapter>.cpp` and fill in the function body. The functions use `extern "C"` linkage (declared in the headers) so Python ctypes and WASM can call them. Inside the function body, you write C++ -- you can use `<cmath>`, `<algorithm>`, `static_cast`, etc. But the data is still raw `double*` arrays with explicit index computation via `LA_IDX(i, j, cols)`.

```bash
cd engine && make
```

### 5. Test via C++ wrapper

The Catch2 tests are already written. They call your functions through the C++ `Matrix` class. Rebuild and run:

```bash
cd wrapper/build && cmake .. && make && ./tests
```

Failures tell you exactly which mathematical property your implementation violates.

### 6. Verify in Python against NumPy

The verification scripts call your shared library via `ctypes` and compare every result against NumPy:

```bash
python3 bindings/verify/verify_ch1.py    # Chapter 1
python3 bindings/verify/verify_ch2.py    # Chapter 2
python3 bindings/verify/verify_ch3.py    # etc.
```

### 7. Build an application or visualization

Run the corresponding Python app or build the TypeScript visualizer. This is where geometric and applied intuition forms.

### 8. When verification fails

A mismatch is **not a bug to fix.** It is a concept to investigate. Trace the discrepancy back to the specific mathematical property you violated. That investigation is where the actual learning happens.

## The One Rule

Never import NumPy, Eigen, LAPACK, or any linear algebra library to do the computation. Use them **only** in the `verify/` directory to check your answers. The moment a library does the work, the project becomes a script instead of a proof.

## Chapter Roadmap

Work sequentially. Each chapter depends on the previous.

| Chapter | File | Functions | Verification Invariants |
|---------|------|-----------|------------------------|
| 1. Systems | `la_elimination.cpp` | `swap_rows`, `scale_row`, `add_scaled_row`, `find_pivot`, `to_ref`, `to_rref`, `solve` | Plug solution back into original system: residual < epsilon |
| 2. Matrices | `la_ops.cpp` | `add`, `scalar_mul`, `mul`, `mul_ikj`, `transpose`, `inverse`, `lu_factorize`, `forward_sub`, `back_sub`, `elementary_*` | `A * inv(A) = I`, `L * U = A`, `(AB)^T = B^T A^T` |
| 3. Determinants | `la_determinant.cpp` | `minor`, `cofactor`, `det_cofactor`, `det_elimination`, `cofactor_matrix`, `adjoint`, `inverse_adjoint`, `cramers_rule` | `det(AB) = det(A) * det(B)`, `det(A^T) = det(A)`, `det(inv(A)) = 1/det(A)` |
| 4. Vector Spaces | `la_vecspace.cpp` | `rank`, `nullity`, `null_space`, `column_space`, `row_space`, `is_independent`, `is_in_span`, `change_of_basis` | `rank(A) + nullity(A) = n`, null space vectors satisfy `Ax = 0` |
| 5. Inner Products | `la_inner.cpp` | `dot`, `norm`, `normalize`, `distance`, `angle`, `are_orthogonal`, `cross_product`, `gram_schmidt`, `orthogonal_projection`, `least_squares` | GS output: all pairs orthogonal + unit norm, LS residual orthogonal to column space |

## Two Mental Modes

- **Exact mode** (for learning): small integer examples you can verify by hand. Isolates conceptual errors.
- **Float mode** (for robustness): partial pivoting + epsilon tolerance. Test on random floating-point matrices. Isolates numerical errors.

Never use `== 0` to check a pivot. Always use `std::fabs(value) < LA_EPSILON`.

## Quick Start

```bash
# Build the engine
cd engine && make

# Build and run tests (expect 15 failures until you implement)
cd ../wrapper && mkdir -p build && cd build && cmake .. && make && ./tests

# After implementing Chapter 1, verify against NumPy
cd ../../ && python3 bindings/verify/verify_ch1.py
```

## Prerequisites

- C++17 compiler (Apple Clang or GCC)
- CMake 3.20+
- Catch2 (`brew install catch2`)
- Python 3.10+ with NumPy and matplotlib
- Emscripten (`brew install emscripten`) for WASM build
- Node.js for TypeScript compilation
