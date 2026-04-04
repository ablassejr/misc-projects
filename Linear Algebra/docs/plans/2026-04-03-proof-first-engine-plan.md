# Proof-First Linear Algebra Engine Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a multi-language linear algebra engine (C engine, C++ wrapper, Python ctypes bindings, TypeScript/WASM visualizations) covering Larson's Elementary Linear Algebra 8e, Chapters 1-5.

**Architecture:** C owns all algorithms against flat `double*` arrays, compiled to `liblinalgcore.dylib`. C++ wraps with RAII `Matrix` class and Catch2 tests. Python calls the C library via `ctypes` for verification against NumPy and application projects. TypeScript calls C compiled to WebAssembly via Emscripten for interactive browser visualizations.

**Tech Stack:** C11 (Apple Clang), C++17 (Catch2 testing), Python 3.14 (ctypes + NumPy + matplotlib), TypeScript (Emscripten WASM), CMake, Make

**Platform:** macOS arm64, shared library as `.dylib`

---

## Task 0: Scaffold Repository Structure

**Files:**
- Create: `engine/include/la_config.h`
- Create: `engine/include/la_matrix.h`
- Create: `engine/src/la_matrix.c`
- Create: `engine/Makefile`
- Create: `wrapper/include/Matrix.h`
- Create: `wrapper/CMakeLists.txt`
- Create: `bindings/linalgcore.py`
- Create: `web/tsconfig.json`
- Create: `web/wasm/build.sh`
- Create: `.gitignore` (update)

**Step 1: Create directory structure**

```bash
mkdir -p engine/include engine/src
mkdir -p wrapper/include wrapper/src wrapper/tests
mkdir -p bindings/verify
mkdir -p apps
mkdir -p web/src web/wasm web/dist
```

**Step 2: Create `engine/include/la_config.h`**

```c
#ifndef LA_CONFIG_H
#define LA_CONFIG_H

#define LA_EPSILON 1e-9

/* Row-major indexing: element (i,j) in a matrix with `cols` columns */
#define LA_IDX(i, j, cols) ((i) * (cols) + (j))

#endif /* LA_CONFIG_H */
```

**Step 3: Create `engine/include/la_matrix.h`**

```c
#ifndef LA_MATRIX_H
#define LA_MATRIX_H

#include <stdlib.h>

typedef struct {
    double* data;   /* row-major flat array */
    int rows;
    int cols;
} LAMatrix;

/* Lifecycle */
LAMatrix* la_matrix_new(int rows, int cols);
LAMatrix* la_matrix_from_array(int rows, int cols, const double* data);
void      la_matrix_free(LAMatrix* mat);
LAMatrix* la_matrix_copy(const LAMatrix* mat);

/* Access */
double la_matrix_get(const LAMatrix* mat, int i, int j);
void   la_matrix_set(LAMatrix* mat, int i, int j, double val);
double* la_matrix_data_ptr(const LAMatrix* mat);

/* Utility */
LAMatrix* la_matrix_identity(int n);
void      la_matrix_print(const LAMatrix* mat);
int       la_matrix_rows(const LAMatrix* mat);
int       la_matrix_cols(const LAMatrix* mat);

#endif /* LA_MATRIX_H */
```

**Step 4: Create `engine/src/la_matrix.c`**

```c
#include "la_matrix.h"
#include "la_config.h"
#include <stdio.h>
#include <string.h>
#include <math.h>

LAMatrix* la_matrix_new(int rows, int cols) {
    LAMatrix* mat = malloc(sizeof(LAMatrix));
    if (!mat) return NULL;
    mat->rows = rows;
    mat->cols = cols;
    mat->data = calloc((size_t)rows * cols, sizeof(double));
    if (!mat->data) { free(mat); return NULL; }
    return mat;
}

LAMatrix* la_matrix_from_array(int rows, int cols, const double* data) {
    LAMatrix* mat = la_matrix_new(rows, cols);
    if (!mat) return NULL;
    memcpy(mat->data, data, (size_t)rows * cols * sizeof(double));
    return mat;
}

void la_matrix_free(LAMatrix* mat) {
    if (mat) {
        free(mat->data);
        free(mat);
    }
}

LAMatrix* la_matrix_copy(const LAMatrix* mat) {
    return la_matrix_from_array(mat->rows, mat->cols, mat->data);
}

double la_matrix_get(const LAMatrix* mat, int i, int j) {
    return mat->data[LA_IDX(i, j, mat->cols)];
}

void la_matrix_set(LAMatrix* mat, int i, int j, double val) {
    mat->data[LA_IDX(i, j, mat->cols)] = val;
}

double* la_matrix_data_ptr(const LAMatrix* mat) {
    return mat->data;
}

LAMatrix* la_matrix_identity(int n) {
    LAMatrix* mat = la_matrix_new(n, n);
    if (!mat) return NULL;
    for (int i = 0; i < n; i++)
        mat->data[LA_IDX(i, i, n)] = 1.0;
    return mat;
}

void la_matrix_print(const LAMatrix* mat) {
    for (int i = 0; i < mat->rows; i++) {
        printf("  [");
        for (int j = 0; j < mat->cols; j++) {
            printf("%8.4f", mat->data[LA_IDX(i, j, mat->cols)]);
            if (j < mat->cols - 1) printf(", ");
        }
        printf("]\n");
    }
}

int la_matrix_rows(const LAMatrix* mat) { return mat->rows; }
int la_matrix_cols(const LAMatrix* mat) { return mat->cols; }
```

**Step 5: Create `engine/Makefile`**

```makefile
CC = cc
CFLAGS = -O2 -fPIC -Wall -Wextra -std=c11 -Iinclude
SOURCES = $(wildcard src/*.c)
OBJECTS = $(SOURCES:src/%.c=build/%.o)

.PHONY: all clean

all: build/liblinalgcore.dylib build/liblinalgcore.a

build/liblinalgcore.dylib: $(OBJECTS)
	$(CC) -dynamiclib -o $@ $^

build/liblinalgcore.a: $(OBJECTS)
	ar rcs $@ $^

build/%.o: src/%.c | build
	$(CC) $(CFLAGS) -c $< -o $@

build:
	mkdir -p build

clean:
	rm -rf build
```

**Step 6: Create `wrapper/CMakeLists.txt`**

```cmake
cmake_minimum_required(VERSION 3.20)
project(linalg_wrapper CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Catch2
find_package(Catch2 3 REQUIRED)

# C engine static library
add_library(linalgcore STATIC IMPORTED)
set_target_properties(linalgcore PROPERTIES
    IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/../engine/build/liblinalgcore.a
    INTERFACE_INCLUDE_DIRECTORIES ${CMAKE_SOURCE_DIR}/../engine/include
)

# C++ wrapper library
add_library(linalg_wrapper src/Matrix.cpp)
target_include_directories(linalg_wrapper PUBLIC include ../engine/include)
target_link_libraries(linalg_wrapper PUBLIC linalgcore)

# Test executable
file(GLOB TEST_SOURCES tests/*.cpp)
add_executable(tests ${TEST_SOURCES})
target_link_libraries(tests PRIVATE linalg_wrapper Catch2::Catch2WithMain)
```

**Step 7: Create stub `wrapper/include/Matrix.h`**

```cpp
#ifndef MATRIX_H
#define MATRIX_H

#include <iostream>
#include <vector>
#include <stdexcept>

extern "C" {
#include "la_matrix.h"
}

class Matrix {
    LAMatrix* m_;

public:
    Matrix(int rows, int cols);
    Matrix(int rows, int cols, const std::vector<double>& data);
    Matrix(const Matrix& other);
    Matrix& operator=(const Matrix& other);
    ~Matrix();

    /* Access */
    int rows() const;
    int cols() const;
    double& operator()(int i, int j);
    double  operator()(int i, int j) const;
    LAMatrix* raw() const;

    /* Factory */
    static Matrix identity(int n);

    /* I/O */
    friend std::ostream& operator<<(std::ostream& os, const Matrix& mat);
};

#endif /* MATRIX_H */
```

**Step 8: Create stub `wrapper/src/Matrix.cpp`**

```cpp
#include "Matrix.h"

Matrix::Matrix(int rows, int cols) : m_(la_matrix_new(rows, cols)) {
    if (!m_) throw std::runtime_error("Allocation failed");
}

Matrix::Matrix(int rows, int cols, const std::vector<double>& data) {
    if ((int)data.size() != rows * cols)
        throw std::invalid_argument("Data size mismatch");
    m_ = la_matrix_from_array(rows, cols, data.data());
    if (!m_) throw std::runtime_error("Allocation failed");
}

Matrix::Matrix(const Matrix& other) : m_(la_matrix_copy(other.m_)) {
    if (!m_) throw std::runtime_error("Copy failed");
}

Matrix& Matrix::operator=(const Matrix& other) {
    if (this != &other) {
        la_matrix_free(m_);
        m_ = la_matrix_copy(other.m_);
        if (!m_) throw std::runtime_error("Copy failed");
    }
    return *this;
}

Matrix::~Matrix() { la_matrix_free(m_); }

int Matrix::rows() const { return la_matrix_rows(m_); }
int Matrix::cols() const { return la_matrix_cols(m_); }

double& Matrix::operator()(int i, int j) {
    return m_->data[i * m_->cols + j];
}

double Matrix::operator()(int i, int j) const {
    return la_matrix_get(m_, i, j);
}

LAMatrix* Matrix::raw() const { return m_; }

Matrix Matrix::identity(int n) {
    Matrix m(n, n);
    for (int i = 0; i < n; i++) m(i, i) = 1.0;
    return m;
}

std::ostream& operator<<(std::ostream& os, const Matrix& mat) {
    for (int i = 0; i < mat.rows(); i++) {
        os << "  [";
        for (int j = 0; j < mat.cols(); j++) {
            char buf[16];
            snprintf(buf, sizeof(buf), "%8.4f", mat(i, j));
            os << buf;
            if (j < mat.cols() - 1) os << ", ";
        }
        os << "]\n";
    }
    return os;
}
```

**Step 9: Create stub `wrapper/tests/test_scaffold.cpp`**

```cpp
#include <catch2/catch_test_macros.hpp>
#include "Matrix.h"

TEST_CASE("Matrix allocation and access", "[matrix]") {
    Matrix m(2, 3);
    REQUIRE(m.rows() == 2);
    REQUIRE(m.cols() == 3);
    m(0, 0) = 5.0;
    REQUIRE(m(0, 0) == 5.0);
}

TEST_CASE("Matrix identity", "[matrix]") {
    Matrix I = Matrix::identity(3);
    REQUIRE(I(0, 0) == 1.0);
    REQUIRE(I(1, 1) == 1.0);
    REQUIRE(I(0, 1) == 0.0);
}

TEST_CASE("Matrix copy", "[matrix]") {
    Matrix a(2, 2, {1, 2, 3, 4});
    Matrix b = a;
    REQUIRE(b(0, 0) == 1.0);
    b(0, 0) = 99.0;
    REQUIRE(a(0, 0) == 1.0);  /* deep copy */
}
```

**Step 10: Create `bindings/linalgcore.py` stub**

```python
"""Python ctypes bridge to liblinalgcore.dylib."""

import ctypes
import ctypes.util
import os

_lib_path = os.path.join(os.path.dirname(__file__), '..', 'engine', 'build', 'liblinalgcore.dylib')
_lib = ctypes.CDLL(_lib_path)


class _LAMatrix(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.POINTER(ctypes.c_double)),
        ('rows', ctypes.c_int),
        ('cols', ctypes.c_int),
    ]


# la_matrix_new
_lib.la_matrix_new.argtypes = [ctypes.c_int, ctypes.c_int]
_lib.la_matrix_new.restype = ctypes.POINTER(_LAMatrix)

# la_matrix_free
_lib.la_matrix_free.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_free.restype = None

# la_matrix_from_array
_lib.la_matrix_from_array.argtypes = [
    ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)
]
_lib.la_matrix_from_array.restype = ctypes.POINTER(_LAMatrix)

# la_matrix_get / la_matrix_set
_lib.la_matrix_get.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.c_int, ctypes.c_int]
_lib.la_matrix_get.restype = ctypes.c_double
_lib.la_matrix_set.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.c_int, ctypes.c_int, ctypes.c_double]
_lib.la_matrix_set.restype = None

# la_matrix_data_ptr
_lib.la_matrix_data_ptr.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_data_ptr.restype = ctypes.POINTER(ctypes.c_double)

# la_matrix_rows / la_matrix_cols
_lib.la_matrix_rows.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_rows.restype = ctypes.c_int
_lib.la_matrix_cols.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_cols.restype = ctypes.c_int


class CMatrix:
    """Python wrapper around a C LAMatrix pointer."""

    def __init__(self, rows, cols, data=None):
        if data is not None:
            arr = (ctypes.c_double * len(data))(*data)
            self._ptr = _lib.la_matrix_from_array(rows, cols, arr)
        else:
            self._ptr = _lib.la_matrix_new(rows, cols)
        if not self._ptr:
            raise MemoryError("Failed to allocate LAMatrix")

    def __del__(self):
        if hasattr(self, '_ptr') and self._ptr:
            _lib.la_matrix_free(self._ptr)

    @property
    def rows(self):
        return _lib.la_matrix_rows(self._ptr)

    @property
    def cols(self):
        return _lib.la_matrix_cols(self._ptr)

    def __getitem__(self, key):
        i, j = key
        return _lib.la_matrix_get(self._ptr, i, j)

    def __setitem__(self, key, value):
        i, j = key
        _lib.la_matrix_set(self._ptr, i, j, value)

    def to_list(self):
        return [[self[i, j] for j in range(self.cols)] for i in range(self.rows)]

    @property
    def ptr(self):
        return self._ptr
```

**Step 11: Create `web/wasm/build.sh`**

```bash
#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGINE_DIR="$SCRIPT_DIR/../../engine"
OUT_DIR="$SCRIPT_DIR/../dist"

mkdir -p "$OUT_DIR"

emcc \
    "$ENGINE_DIR"/src/*.c \
    -I"$ENGINE_DIR"/include \
    -o "$OUT_DIR/engine.js" \
    -s EXPORTED_FUNCTIONS="[\
        '_la_matrix_new','_la_matrix_free','_la_matrix_from_array',\
        '_la_matrix_get','_la_matrix_set','_la_matrix_data_ptr',\
        '_la_matrix_rows','_la_matrix_cols','_la_matrix_identity'\
    ]" \
    -s EXPORTED_RUNTIME_METHODS="['ccall','cwrap','getValue','setValue']" \
    -s MODULARIZE=1 \
    -s EXPORT_NAME="LinAlgEngine" \
    -s ALLOW_MEMORY_GROWTH=1 \
    -O2

echo "WASM build complete: $OUT_DIR/engine.js + engine.wasm"
```

**Step 12: Create `web/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ES2020",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true
  },
  "include": ["src/**/*.ts"]
}
```

**Step 13: Create `web/src/wasm-bridge.ts` stub**

```typescript
/* eslint-disable @typescript-eslint/no-explicit-any */

let engine: any = null;

export async function init(): Promise<void> {
    const LinAlgEngine = (await import('../dist/engine.js')).default;
    engine = await LinAlgEngine();
}

export function createMatrix(rows: number, cols: number, data?: number[]): number {
    if (!engine) throw new Error('Engine not initialized — call init() first');
    const ptr = engine._la_matrix_new(rows, cols);
    if (data) {
        const dataPtr = engine._la_matrix_data_ptr(ptr);
        for (let i = 0; i < data.length; i++) {
            engine.HEAPF64[dataPtr / 8 + i] = data[i];
        }
    }
    return ptr;
}

export function getElement(matPtr: number, i: number, j: number): number {
    return engine._la_matrix_get(matPtr, i, j);
}

export function setElement(matPtr: number, i: number, j: number, val: number): void {
    engine._la_matrix_set(matPtr, i, j, val);
}

export function freeMatrix(matPtr: number): void {
    engine._la_matrix_free(matPtr);
}

export function matrixRows(matPtr: number): number {
    return engine._la_matrix_rows(matPtr);
}

export function matrixCols(matPtr: number): number {
    return engine._la_matrix_cols(matPtr);
}
```

**Step 14: Update `.gitignore`**

Append:
```
engine/build/
wrapper/build/
web/dist/
web/node_modules/
__pycache__/
*.o
*.a
*.dylib
*.so
*.wasm
```

**Step 15: Build, test, and commit**

```bash
cd engine && make
cd ../wrapper && mkdir -p build && cd build && cmake .. && make && ./tests
cd ../../
chmod +x web/wasm/build.sh && web/wasm/build.sh
python3 -c "from bindings.linalgcore import CMatrix; m = CMatrix(2, 2, [1,2,3,4]); print(m.to_list())"
git add -A && git commit -m "scaffold: multi-language linear algebra engine structure"
```

---

## Task 1: C Engine — Chapter 1 (Elimination)

**Files:**
- Create: `engine/include/la_elimination.h`
- Create: `engine/src/la_elimination.c`
- Modify: `engine/Makefile` (no change needed, wildcard picks up new .c)

**Step 1: Create `engine/include/la_elimination.h`**

```c
#ifndef LA_ELIMINATION_H
#define LA_ELIMINATION_H

#include "la_matrix.h"

/* Elementary row operations (in-place) */
void la_swap_rows(LAMatrix* mat, int i, int j);
void la_scale_row(LAMatrix* mat, int i, double scalar);
void la_add_scaled_row(LAMatrix* mat, int target, int source, double scalar);

/* Gaussian elimination with partial pivoting */
int la_to_ref(LAMatrix* mat);   /* Returns number of row swaps */
int la_to_rref(LAMatrix* mat);  /* Returns number of pivot columns */

/* System solving */
/* solution_type: 0 = unique, 1 = infinite, -1 = inconsistent */
/* For unique: result is filled with the solution vector (n_vars doubles) */
/* For infinite: result is NULL (caller inspects RREF manually) */
/* Returns solution_type */
int la_solve(const LAMatrix* augmented, double* result);

/* Pivot finding (partial pivoting) */
int la_find_pivot(const LAMatrix* mat, int col, int start_row);

#endif /* LA_ELIMINATION_H */
```

**Step 2: Create `engine/src/la_elimination.c`**

```c
#include "la_elimination.h"
#include "la_config.h"
#include <math.h>
#include <string.h>

void la_swap_rows(LAMatrix* mat, int i, int j) {
    if (i == j) return;
    for (int k = 0; k < mat->cols; k++) {
        double tmp = mat->data[LA_IDX(i, k, mat->cols)];
        mat->data[LA_IDX(i, k, mat->cols)] = mat->data[LA_IDX(j, k, mat->cols)];
        mat->data[LA_IDX(j, k, mat->cols)] = tmp;
    }
}

void la_scale_row(LAMatrix* mat, int i, double scalar) {
    for (int k = 0; k < mat->cols; k++)
        mat->data[LA_IDX(i, k, mat->cols)] *= scalar;
}

void la_add_scaled_row(LAMatrix* mat, int target, int source, double scalar) {
    for (int k = 0; k < mat->cols; k++)
        mat->data[LA_IDX(target, k, mat->cols)] +=
            scalar * mat->data[LA_IDX(source, k, mat->cols)];
}

int la_find_pivot(const LAMatrix* mat, int col, int start_row) {
    int best = -1;
    double best_val = LA_EPSILON;
    for (int r = start_row; r < mat->rows; r++) {
        double v = fabs(mat->data[LA_IDX(r, col, mat->cols)]);
        if (v > best_val) {
            best_val = v;
            best = r;
        }
    }
    return best;
}

int la_to_ref(LAMatrix* mat) {
    int swaps = 0;
    int pivot_row = 0;

    for (int col = 0; col < mat->cols && pivot_row < mat->rows; col++) {
        int best = la_find_pivot(mat, col, pivot_row);
        if (best < 0) continue;

        if (best != pivot_row) {
            la_swap_rows(mat, pivot_row, best);
            swaps++;
        }

        double pv = mat->data[LA_IDX(pivot_row, col, mat->cols)];
        la_scale_row(mat, pivot_row, 1.0 / pv);

        for (int r = pivot_row + 1; r < mat->rows; r++) {
            double factor = mat->data[LA_IDX(r, col, mat->cols)];
            if (fabs(factor) > LA_EPSILON)
                la_add_scaled_row(mat, r, pivot_row, -factor);
        }
        pivot_row++;
    }
    return swaps;
}

int la_to_rref(LAMatrix* mat) {
    int swaps = 0;
    int pivot_row = 0;
    int pivot_cols[mat->cols];
    int num_pivots = 0;

    /* Forward elimination to REF */
    for (int col = 0; col < mat->cols && pivot_row < mat->rows; col++) {
        int best = la_find_pivot(mat, col, pivot_row);
        if (best < 0) continue;

        if (best != pivot_row) {
            la_swap_rows(mat, pivot_row, best);
            swaps++;
        }

        double pv = mat->data[LA_IDX(pivot_row, col, mat->cols)];
        la_scale_row(mat, pivot_row, 1.0 / pv);

        for (int r = pivot_row + 1; r < mat->rows; r++) {
            double factor = mat->data[LA_IDX(r, col, mat->cols)];
            if (fabs(factor) > LA_EPSILON)
                la_add_scaled_row(mat, r, pivot_row, -factor);
        }

        pivot_cols[num_pivots] = col;
        num_pivots++;
        pivot_row++;
    }

    /* Back elimination */
    for (int p = num_pivots - 1; p >= 0; p--) {
        int col = pivot_cols[p];
        int row = p;
        for (int r = row - 1; r >= 0; r--) {
            double factor = mat->data[LA_IDX(r, col, mat->cols)];
            if (fabs(factor) > LA_EPSILON)
                la_add_scaled_row(mat, r, row, -factor);
        }
    }

    return num_pivots;
}

int la_solve(const LAMatrix* augmented, double* result) {
    int n_vars = augmented->cols - 1;
    LAMatrix* m = la_matrix_copy(augmented);
    int num_pivots = la_to_rref(m);

    /* Find pivot columns */
    int pivot_col[m->rows];
    int pcount = 0;
    for (int i = 0; i < m->rows && pcount < num_pivots; i++) {
        for (int j = 0; j < n_vars; j++) {
            if (fabs(m->data[LA_IDX(i, j, m->cols)]) > LA_EPSILON) {
                pivot_col[pcount++] = j;
                break;
            }
        }
    }

    /* Check for inconsistency: zero row on left, nonzero on right */
    for (int i = 0; i < m->rows; i++) {
        int all_zero = 1;
        for (int j = 0; j < n_vars; j++) {
            if (fabs(m->data[LA_IDX(i, j, m->cols)]) > LA_EPSILON) {
                all_zero = 0;
                break;
            }
        }
        if (all_zero && fabs(m->data[LA_IDX(i, n_vars, m->cols)]) > LA_EPSILON) {
            la_matrix_free(m);
            return -1; /* inconsistent */
        }
    }

    /* Check for free variables */
    if (pcount < n_vars) {
        la_matrix_free(m);
        return 1; /* infinite */
    }

    /* Unique solution: read from RREF */
    if (result) {
        for (int i = 0; i < pcount && i < n_vars; i++)
            result[pivot_col[i]] = m->data[LA_IDX(i, n_vars, m->cols)];
    }

    la_matrix_free(m);
    return 0; /* unique */
}
```

**Step 3: Build and test**

```bash
cd engine && make
```

**Step 4: Add C++ wrapper methods and Catch2 tests**

Modify `wrapper/include/Matrix.h` — add to the class:
```cpp
/* Ch.1: Elimination */
void swap_rows(int i, int j);
void scale_row(int i, double scalar);
void add_scaled_row(int target, int source, double scalar);
Matrix ref() const;
Matrix rref() const;
/* solve: returns solution_type (0=unique, 1=infinite, -1=inconsistent) */
int solve(std::vector<double>& result) const;
```

Create `wrapper/tests/test_ch1_systems.cpp`:
```cpp
#include <catch2/catch_test_macros.hpp>
#include <catch2/matchers/catch_matchers_floating_point.hpp>
#include "Matrix.h"

extern "C" {
#include "la_elimination.h"
}

TEST_CASE("Row swap", "[ch1]") {
    Matrix m(2, 2, {1, 2, 3, 4});
    m.swap_rows(0, 1);
    REQUIRE(m(0, 0) == 3.0);
    REQUIRE(m(1, 0) == 1.0);
}

TEST_CASE("Solve unique 3x3", "[ch1]") {
    // x + y + 2z = 9, 2x + 4y - 3z = 1, 3x + 6y - 5z = 0
    Matrix aug(3, 4, {1,1,2,9, 2,4,-3,1, 3,6,-5,0});
    std::vector<double> sol;
    int type = aug.solve(sol);
    REQUIRE(type == 0);
    REQUIRE_THAT(sol[0], Catch::Matchers::WithinAbs(1.0, 1e-6));
    REQUIRE_THAT(sol[1], Catch::Matchers::WithinAbs(2.0, 1e-6));
    REQUIRE_THAT(sol[2], Catch::Matchers::WithinAbs(3.0, 1e-6));
}

TEST_CASE("Solve inconsistent", "[ch1]") {
    Matrix aug(3, 4, {1,1,1,2, 0,1,1,1, 0,0,0,3});
    std::vector<double> sol;
    REQUIRE(aug.solve(sol) == -1);
}

TEST_CASE("Solve infinite", "[ch1]") {
    Matrix aug(2, 3, {1,2,3, 2,4,6});
    std::vector<double> sol;
    REQUIRE(aug.solve(sol) == 1);
}

TEST_CASE("RREF", "[ch1]") {
    Matrix m(3, 4, {1,1,2,9, 2,4,-3,1, 3,6,-5,0});
    Matrix r = m.rref();
    // Should be identity on left, solution on right
    REQUIRE_THAT(r(0, 3), Catch::Matchers::WithinAbs(1.0, 1e-6));
    REQUIRE_THAT(r(1, 3), Catch::Matchers::WithinAbs(2.0, 1e-6));
    REQUIRE_THAT(r(2, 3), Catch::Matchers::WithinAbs(3.0, 1e-6));
}
```

**Step 5: Build wrapper, run tests**

```bash
cd engine && make
cd ../wrapper && mkdir -p build && cd build && cmake .. && make && ./tests
```

**Step 6: Create Python verification `bindings/verify/verify_ch1.py`**

```python
"""Verify Ch.1 elimination against NumPy."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from linalgcore import CMatrix

# Bind C elimination functions
import ctypes
_lib_path = os.path.join(os.path.dirname(__file__), '..', '..', 'engine', 'build', 'liblinalgcore.dylib')
_lib = ctypes.CDLL(_lib_path)

class _LAMatrix(ctypes.Structure):
    _fields_ = [('data', ctypes.POINTER(ctypes.c_double)), ('rows', ctypes.c_int), ('cols', ctypes.c_int)]

_lib.la_solve.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.POINTER(ctypes.c_double)]
_lib.la_solve.restype = ctypes.c_int

def c_solve(A_lists, b_list):
    """Solve Ax=b via C engine. Returns (type, solution_or_None)."""
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

# Test 1: Unique 3x3
A = [[1,1,2],[2,4,-3],[3,6,-5]]
b = [9,1,0]
sol_type, sol = c_solve(A, b)
np_sol = np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float))
check("Unique 3x3 type", sol_type == 0)
check("Unique 3x3 matches NumPy", all(abs(s - n) < 1e-6 for s, n in zip(sol, np_sol)))
residual = np.array(A) @ np.array(sol) - np.array(b)
check("Unique 3x3 residual < epsilon", np.linalg.norm(residual) < 1e-6)

# Test 2: Inconsistent
sol_type2, _ = c_solve([[1,1,1],[0,1,1],[0,0,0]], [2,1,3])
check("Inconsistent detected", sol_type2 == -1)

# Test 3: Infinite (underdetermined)
sol_type3, _ = c_solve([[1,2],[2,4]], [3,6])
check("Infinite detected", sol_type3 == 1)

# Test 4: Homogeneous with nontrivial solution
sol_type4, _ = c_solve([[1,2,3],[4,5,6],[7,8,9]], [0,0,0])
check("Homogeneous infinite", sol_type4 == 1)

print(f"\n{passed}/{passed+failed} passed")
```

**Step 7: Run Python verification**

```bash
cd bindings/verify && python3 verify_ch1.py
```

**Step 8: Commit**

```bash
git add -A && git commit -m "feat(ch1): elimination engine — C + C++ wrapper + Python verification"
```

---

## Task 2: C Engine — Chapter 2 (Matrix Operations)

**Files:**
- Create: `engine/include/la_ops.h`
- Create: `engine/src/la_ops.c`
- Modify: `wrapper/include/Matrix.h` (add operator overloads)
- Modify: `wrapper/src/Matrix.cpp` (implement)
- Create: `wrapper/tests/test_ch2_matrices.cpp`
- Create: `bindings/verify/verify_ch2.py`
- Create: `apps/hill_cipher.py`
- Create: `apps/markov_chain.py`

**Step 1: Create `engine/include/la_ops.h`**

```c
#ifndef LA_OPS_H
#define LA_OPS_H

#include "la_matrix.h"

/* Arithmetic */
LAMatrix* la_matrix_add(const LAMatrix* A, const LAMatrix* B);
LAMatrix* la_matrix_scalar_mul(const LAMatrix* A, double scalar);
LAMatrix* la_matrix_mul(const LAMatrix* A, const LAMatrix* B);
LAMatrix* la_matrix_mul_ikj(const LAMatrix* A, const LAMatrix* B);  /* cache-friendly */
LAMatrix* la_matrix_transpose(const LAMatrix* A);

/* Inverse via Gauss-Jordan on [A|I] */
/* Returns NULL if singular */
LAMatrix* la_matrix_inverse(const LAMatrix* A);

/* LU factorization (Doolittle, no pivoting) */
/* Returns 0 on success, -1 if zero pivot encountered */
int la_lu_factorize(const LAMatrix* A, LAMatrix** L, LAMatrix** U);
void la_forward_sub(const LAMatrix* L, const double* b, double* y, int n);
void la_back_sub(const LAMatrix* U, const double* y, double* x, int n);

/* Elementary matrices */
LAMatrix* la_elementary_swap(int n, int i, int j);
LAMatrix* la_elementary_scale(int n, int i, double c);
LAMatrix* la_elementary_add(int n, int target, int source, double c);

#endif /* LA_OPS_H */
```

**Step 2: Implement `engine/src/la_ops.c`** with all functions from the header.

**Step 3: C++ wrapper — add operator overloads:**
```cpp
Matrix operator+(const Matrix& other) const;
Matrix operator*(const Matrix& other) const;
Matrix operator*(double scalar) const;
Matrix transpose() const;
Matrix inverse() const;
std::pair<Matrix, Matrix> lu() const;
```

**Step 4: Create Catch2 tests `wrapper/tests/test_ch2_matrices.cpp`:**
- A+B, scalar*A, A*B, transpose, inverse round-trip, LU=A, (AB)^T = B^T A^T, non-commutativity

**Step 5: Create `bindings/verify/verify_ch2.py`:**
- Compare all operations against NumPy
- Test: A*inv(A) = I, LU = A, (AB)^T = B^T A^T

**Step 6: Create `apps/hill_cipher.py`** — encode/decode using C engine via ctypes

**Step 7: Create `apps/markov_chain.py`** — iterate P^k via C engine, plot convergence

**Step 8: Build, test, verify, commit**

---

## Task 3: C Engine — Chapter 3 (Determinants)

**Files:**
- Create: `engine/include/la_determinant.h`
- Create: `engine/src/la_determinant.c`
- Create: `wrapper/tests/test_ch3_determinants.cpp`
- Create: `bindings/verify/verify_ch3.py`
- Create: `apps/geo_engine.py`

**Step 1: Create `engine/include/la_determinant.h`**

```c
#ifndef LA_DETERMINANT_H
#define LA_DETERMINANT_H

#include "la_matrix.h"

double    la_det_cofactor(const LAMatrix* A);
double    la_det_elimination(const LAMatrix* A);
double    la_minor(const LAMatrix* A, int i, int j);
double    la_cofactor(const LAMatrix* A, int i, int j);
LAMatrix* la_cofactor_matrix(const LAMatrix* A);
LAMatrix* la_adjoint(const LAMatrix* A);
LAMatrix* la_inverse_adjoint(const LAMatrix* A);
int       la_cramers_rule(const LAMatrix* A, const double* b, double* result);

#endif /* LA_DETERMINANT_H */
```

**Step 2: Implement `engine/src/la_determinant.c`** — cofactor expansion (recursive), elimination-based (O(n^3)), adjoint, Cramer's Rule.

**Step 3: C++ wrapper** — add `det()`, `det_cofactor()`, `adjoint()`, `cramers_solve(b)` methods.

**Step 4: Catch2 tests** — det methods agree, det(AB)=det(A)*det(B), det(A^T)=det(A), det(A^-1)=1/det(A), Cramer matches solve.

**Step 5: Python verification** — compare against `np.linalg.det`, cross-check adjoint inverse vs Gauss-Jordan inverse.

**Step 6: `apps/geo_engine.py`** — triangle area, tetrahedron volume, collinearity, line/plane equations with matplotlib.

**Step 7: Build, test, verify, commit**

---

## Task 4: C Engine — Chapter 4 (Vector Spaces)

**Files:**
- Create: `engine/include/la_vecspace.h`
- Create: `engine/src/la_vecspace.c`
- Create: `wrapper/tests/test_ch4_vecspaces.cpp`
- Create: `bindings/verify/verify_ch4.py`
- Create: `apps/rank_explorer.py`
- Create: `apps/change_of_basis_viz.py`

**Step 1: Create `engine/include/la_vecspace.h`**

```c
#ifndef LA_VECSPACE_H
#define LA_VECSPACE_H

#include "la_matrix.h"

int  la_rank(const LAMatrix* A);
int  la_nullity(const LAMatrix* A);

/* null_space: allocates and returns basis vectors as columns of result matrix */
/* Returns number of basis vectors (= nullity) */
int  la_null_space(const LAMatrix* A, LAMatrix** basis);

/* column_space: returns basis as columns of result (original pivot columns) */
int  la_column_space(const LAMatrix* A, LAMatrix** basis);

/* row_space: returns basis as rows of result (nonzero rows of RREF) */
int  la_row_space(const LAMatrix* A, LAMatrix** basis);

/* Independence: 1 = independent, 0 = dependent */
int  la_is_independent(const double* vectors, int num_vectors, int dim);

/* Span membership: 1 = in span, 0 = not */
int  la_is_in_span(const double* v, const double* vectors, int num_vectors, int dim);

/* Change of basis: computes transition matrix P (n x n) */
/* old_basis and new_basis are n x n matrices (basis vectors as columns) */
LAMatrix* la_change_of_basis(const LAMatrix* old_basis, const LAMatrix* new_basis);

#endif /* LA_VECSPACE_H */
```

**Step 2-7:** Implement C, C++ wrapper, Catch2 tests, Python verify (rank-nullity theorem, null space Ax=0, compare rank against np.linalg.matrix_rank), apps, commit.

---

## Task 5: C Engine — Chapter 5 (Inner Product Spaces)

**Files:**
- Create: `engine/include/la_inner.h`
- Create: `engine/src/la_inner.c`
- Create: `wrapper/tests/test_ch5_inner.cpp`
- Create: `bindings/verify/verify_ch5.py`
- Create: `apps/regression.py` (capstone)

**Step 1: Create `engine/include/la_inner.h`**

```c
#ifndef LA_INNER_H
#define LA_INNER_H

#include "la_matrix.h"

double la_dot(const double* u, const double* v, int n);
double la_norm(const double* v, int n);
void   la_normalize(const double* v, double* result, int n);
double la_distance(const double* u, const double* v, int n);
double la_angle(const double* u, const double* v, int n);
int    la_are_orthogonal(const double* u, const double* v, int n);
void   la_cross_product(const double* u, const double* v, double* result);

/* Gram-Schmidt: vectors is dim x num_vectors (columns), result same shape */
void la_gram_schmidt(const double* vectors, double* result, int num_vectors, int dim);

/* Orthogonal projection of v onto subspace spanned by basis columns */
void la_orthogonal_projection(const double* v, const double* basis,
                              int num_basis, int dim, double* result);

/* Least squares: solve min ||Ax - b||^2 via normal equations */
/* A is m x n, b is m, result is n */
int la_least_squares(const LAMatrix* A, const double* b, double* result);

#endif /* LA_INNER_H */
```

**Step 2-7:** Implement C, C++ wrapper (free functions `dot`, `norm`, `cross`, class methods `gram_schmidt`, `least_squares_solve`), Catch2 tests (Cauchy-Schwarz, triangle inequality, GS orthonormality, LS residual orthogonality), Python verify against NumPy, capstone `apps/regression.py` (polynomial regression degrees 1-5), commit.

---

## Task 6: TypeScript/WASM — Interactive Visualizations

**Files:**
- Modify: `web/wasm/build.sh` (add all exported C functions)
- Modify: `web/src/wasm-bridge.ts` (expose full API)
- Create: `web/src/elimination-stepper.ts`
- Create: `web/src/transform-playground.ts`
- Create: `web/src/det-visualizer.ts`
- Create: `web/src/basis-explorer.ts`
- Create: `web/src/gram-schmidt-3d.ts`
- Create: `web/index.html`
- Create: `web/package.json`

**Step 1: Update `web/wasm/build.sh`** — export all `la_*` functions from all 6 headers.

**Step 2: Update `web/src/wasm-bridge.ts`** — typed wrappers for all exported C functions.

**Step 3: Create `web/src/elimination-stepper.ts`:**
- User enters system of equations
- "Next Step" button performs one row operation via WASM
- Matrix display highlights current pivot, modified row
- Shows solution classification at end

**Step 4: Create `web/src/transform-playground.ts`:**
- 2D canvas with unit square
- User enters 2x2 matrix via input fields
- Transformed shape drawn in real time
- Shows determinant (area scaling factor) live
- Toggle column vectors as arrows

**Step 5: Create `web/src/det-visualizer.ts`:**
- 2D: two draggable vectors, parallelogram area = det, updates live
- When vectors become parallel, area collapses to zero

**Step 6: Create `web/src/basis-explorer.ts`:**
- Standard grid (gray) + custom basis grid (color)
- Draggable basis vectors
- Point shows coordinates in both bases simultaneously

**Step 7: Create `web/src/gram-schmidt-3d.ts`:**
- 3D scene (Three.js or CSS3D)
- 3 adjustable vectors via sliders
- Step-through: show projection, subtraction, normalization (animated)

**Step 8: Create `web/index.html`** — entry point linking all visualizers.

**Step 9: Build WASM, compile TS, test in browser, commit**

```bash
cd web/wasm && bash build.sh
cd .. && npx tsc
# Open index.html in browser to verify
git add -A && git commit -m "feat: TypeScript/WASM interactive visualizations"
```

---

## Execution Strategy

Tasks must be executed **sequentially** because:
- Task 0 (scaffold) must complete first
- Tasks 1-5 (C engine chapters) are sequential: each chapter builds on previous C functions
- Task 6 (TypeScript/WASM) depends on all C functions being compiled

Within each task, the proof loop is: **C implementation → C++ wrapper + Catch2 test → Python ctypes verification → Application → Commit**.

**Estimated files per task:**
- Task 0: ~15 files (scaffold)
- Tasks 1-5: ~8-10 files each (header + impl + wrapper + test + verify + apps)
- Task 6: ~10 files (WASM build + 5 visualizers + bridge + HTML)

**Total: ~75 files across 7 tasks**
