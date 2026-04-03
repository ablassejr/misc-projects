# Textbook Notes: Chapters 3-5
## Elementary Linear Algebra (Larson, 8e)

Extracted examples, definitions, and numerical values for Colab notebook content.

---

## Section 3.1: The Determinant of a Matrix (pp. 110-117)

### Key Definitions

**2×2 determinant:** det([[a,b],[c,d]]) = ad - bc.

**Minor M_ij:** Determinant of the matrix with row i and column j deleted.

**Cofactor C_ij:** C_ij = (-1)^(i+j) × M_ij.

**Cofactor expansion:** det(A) = Σ a_{ij} × C_{ij} along any row i or column j (Theorem 3.1).

**Triangular matrix:** det = product of diagonal entries (Theorem 3.2).

### Numerical Examples

**2×2 determinants (Example 1):**
```
A = [[2,-3],[1,2]], |A| = 7
B = [[2,1],[4,2]], |B| = 0
C = [[0,3/2],[2,4]], |C| = -3
```

**3×3 minors and cofactors (Example 2):**
```
A = [[0,2,1],[3,-1,2],[4,0,1]]
Cofactors: C11=-1, C12=5, C13=4, C21=-2, C22=-4, C23=8, C31=5, C32=3, C33=-6
det(A) = 0(-1) + 2(5) + 1(4) = 14
```

**4×4 determinant (Example 4):**
```
A = [[1,-2,3,0],[-1,1,0,2],[0,2,0,3],[3,4,0,-2]]
Expand along column 3 (three zeros): |A| = 3(13) = 39
```

**Triangular (Example 6):**
```
A = [[2,0,0,0],[4,-2,0,0],[-5,6,1,0],[1,5,3,3]]
|A| = (2)(-2)(1)(3) = -12
```

---

## Section 3.2: Determinants and Elementary Operations (pp. 118-125)

### Key Theorems

- Row swap: det negates
- Row addition: det unchanged
- Row scaling by c: det multiplied by c
- Zero row/column → det = 0
- Two equal rows → det = 0

### Numerical Examples

**Row reduction determinant (Example 2):**
```
A = [[0,-7,14],[1,2,-2],[0,3,-8]]
After row swap and reduction: |A| = -14
```

**5×5 determinant (Example 6):**
```
A = [[2,0,1,3,-2],[-2,1,3,2,-1],[1,0,-1,2,3],[3,-1,2,4,-3],[1,1,3,2,0]]
|A| = -135
```

---

## Section 3.3: Properties of Determinants (pp. 126-133)

### Key Theorems

- det(AB) = det(A) × det(B) (Theorem 3.5)
- det(cA) = c^n × det(A) for n×n A (Theorem 3.6)
- A invertible ⟺ det(A) ≠ 0 (Theorem 3.7)
- det(A⁻¹) = 1/det(A) (Theorem 3.8)
- det(A^T) = det(A) (Theorem 3.9)

### Numerical Examples

**det(AB) = det(A)det(B) (Example 1):**
```
A = [[1,-2,2],[0,3,2],[1,0,1]], |A| = -7
B = [[2,0,1],[0,-1,-2],[3,1,-2]], |B| = 11
AB = [[8,4,1],[6,-1,-10],[5,1,-1]], |AB| = -77 = (-7)(11) ✓
```

**Scalar multiple (Example 2):**
```
A = [[10,-20,40],[30,0,50],[-20,-30,10]] = 10 × [[1,-2,4],[3,0,5],[-2,-3,1]]
|A| = 10³ × 5 = 5000
```

**Singular vs nonsingular (Example 3):**
```
A = [[0,2,-1],[3,-2,1],[3,2,-1]]: |A| = 0 → singular
B = [[0,2,-1],[3,-2,1],[3,2,1]]:  |B| = -12 → nonsingular
```

---

## Section 3.4: Applications of Determinants (pp. 134-143)

### Key Formulas

**Cramer's Rule:** x_i = det(A_i)/det(A), where A_i replaces column i with b.

**Inverse via adjoint:** A⁻¹ = (1/det(A)) × adj(A).

**Triangle area:** ½|det([[x1,y1,1],[x2,y2,1],[x3,y3,1]])|.

**Collinearity test:** det = 0 → collinear.

**Line through 2 points:** det([[x,y,1],[x1,y1,1],[x2,y2,1]]) = 0.

**Volume of tetrahedron:** (1/6)|det of edge vectors|.

### Numerical Examples

**Adjoint (Example 1):**
```
A = [[-1,3,2],[0,-2,1],[1,0,-2]]
adj(A) = [[4,6,7],[1,0,1],[2,3,2]]
det(A) = 3
A⁻¹ = (1/3) × adj(A)
```

**Cramer's Rule 2×2 (Example 3):**
```
4x1 - 2x2 = 10, 3x1 - 5x2 = 11
|A| = -14, x1 = -28/-14 = 2, x2 = 14/-14 = -1
```

**Triangle area (Example 5):**
```
Vertices: (1,1), (2,2), (4,3)
Area = ½|det([[1,1,1],[2,2,1],[4,3,1]])| = ½|-1| = 1/2
```

**Line through 2 points (Example 6):**
```
Through (2,4) and (-1,3): x - 3y = -10
```

**Volume of tetrahedron (Example 7):**
```
Vertices: (0,4,1), (4,0,0), (3,5,2), (2,2,5)
V = (1/6)|(-72)| = 12
```

**Plane through 3 points (Example 8):**
```
Through (0,1,0), (-1,3,2), (-2,0,1): 4x - 3y + 5z = -3
```

---

## Section 4.1: Vectors in R^n (pp. 152-160)

### Numerical Examples

**R³ operations (Example 4):**
```
u = (-1,0,1), v = (2,-1,5)
u + v = (1,-1,6), 2u = (-2,0,2), v - 2u = (4,-1,3)
```

**Linear combination (Example 6):**
```
x = (-1,-2,-2), u = (0,1,4), v = (-1,1,2), w = (3,1,2)
x = 1u + (-2)v + (-1)w
```

---

## Section 4.2: Vector Spaces (pp. 161-167)

### Key Definition

**Vector space:** Set V with addition and scalar multiplication satisfying 10 axioms (closure ×2, commutativity, associativity, identity, inverse, scalar properties ×4).

**Standard vector spaces:** Rⁿ, Pₙ, M_{m,n}, C[a,b].

### Non-examples
- Integers under standard operations: not closed under scalar multiplication (½ · 1 = ½ ∉ Z)
- R² with c(x1,x2) = (cx1, 0): fails 1·v = v

---

## Section 4.3: Subspaces (pp. 168-174)

### Key Theorem

**Subspace test (Theorem 4.5):** W ⊆ V is a subspace iff closed under addition and scalar multiplication.

### Numerical Examples

**Subspace:** W = {(x1, 0, x3)} in R³ (the xz-plane) ✓

**NOT subspace:** Singular matrices — A=[[1,0],[0,0]], B=[[0,0],[0,1]] are singular, but A+B = I is not.

**NOT subspace:** First quadrant — (-1)(1,1) = (-1,-1) ∉ W.

---

## Section 4.4: Spanning Sets and Linear Independence (pp. 175-185)

### Key Definitions

**Linearly independent:** c1v1 + ... + ckvk = 0 ⟹ all ci = 0.

**Spanning set:** Every vector in V is a linear combination of S.

### Numerical Examples

**Spans R³ (Example 5):**
```
S = {(1,2,3), (0,1,2), (-2,0,1)}
det = -1 ≠ 0, so S spans R³
```

**Does NOT span R³ (Example 6):**
```
S = {(1,2,3), (0,1,2), (-1,0,1)}
det = 0, (1,-2,2) cannot be expressed as combination
```

**Independence test (Example 8):**
```
S = {(1,2,3), (0,1,2), (-2,0,1)}
System reduces to I → only trivial solution → independent
```

**Dependent in P₂ (Example 9):**
```
S = {1+x-2x², 2+5x-x², x+x²}
Nontrivial solution: c1=2, c2=-1, c3=3 → dependent
```

---

## Section 4.5: Basis and Dimension (pp. 186-194)

### Key Theorems

- All bases have the same number of vectors (Theorem 4.11)
- dim(Rⁿ) = n, dim(Pₙ) = n+1, dim(M_{m,n}) = mn

### Numerical Examples

**Nonstandard basis for R² (Example 2):**
```
S = {(1,1), (1,-1)}, det = -2 ≠ 0 → basis
```

**Dimension of subspace (Example 9):**
```
W = {(d, c-d, c)} in R³
Basis: {(0,1,1), (1,-1,0)}, dim = 2
```

---

## Section 4.6: Rank and Systems (pp. 195-207)

### Key Theorems

**Rank-Nullity Theorem (4.17):** rank(A) + nullity(A) = n (number of columns).

**Row space basis:** Nonzero rows of REF.
**Column space basis:** Columns of A at pivot positions.
**Null space basis:** Free-variable solutions of Ax = 0.

### Numerical Examples

**Rank and row space (Example 2):**
```
A = [[1,3,1,3],[0,1,1,0],[-3,0,6,-1],[3,4,-2,1],[2,0,-4,-2]]
Rank = 3
```

**Null space (Example 7):**
```
A = [[1,2,-2,1],[3,6,-5,4],[1,2,0,3]]
RREF: [[1,2,0,3],[0,0,1,1],[0,0,0,0]]
Null space basis: {(-2,1,0,0), (-3,0,-1,1)}
Nullity = 2, rank = 2, n = 4 = 2+2 ✓
```

**Nonhomogeneous solution (Example 9):**
```
x = [5,-7,0,0] + s[2,-1,1,0] + t[-1,3,0,1]
(particular + null space)
```

---

## Section 4.7: Coordinates and Change of Basis (pp. 208-214)

### Numerical Examples

**Coordinates in nonstandard basis (Example 3):**
```
x = (1,2,-1), B' = {(1,0,1), (0,-1,2), (2,3,-5)}
[x]_{B'} = [5, -8, -2]
```

**Transition matrix (Example 4):**
```
B = standard, B' = {(1,0,1), (0,-1,3), (2,3,-5)}
P⁻¹ = [[-1,4,2],[3,-7,-3],[1,-2,-1]]
```

**R² transition (Example 5):**
```
B = {(-3,2),(4,-2)}, B' = {(-1,2),(2,-2)}
P⁻¹ = [[-1,2],[-2,3]]
```

---

## Section 5.1: Length and Dot Product in R^n (pp. 232-242)

### Key Theorems

- Cauchy-Schwarz: |u·v| ≤ ‖u‖·‖v‖
- Triangle Inequality: ‖u+v‖ ≤ ‖u‖+‖v‖
- Pythagorean: u⊥v ⟹ ‖u+v‖² = ‖u‖²+‖v‖²

### Numerical Examples

**Norm (Example 1a):**
```
v = (0,-2,1,4,-2), ‖v‖ = √25 = 5
```

**Unit vector (Example 2):**
```
v = (3,-1,2), ‖v‖ = √14
unit = (3/√14, -1/√14, 2/√14)
```

**Dot product (Example 4):**
```
u = (1,2,0,-3), v = (3,-2,4,2)
u·v = 3 - 4 + 0 - 6 = -7
```

**Angle (Example 8):**
```
u = (-4,0,2,-2), v = (2,0,-1,1)
cos θ = -12/√(24·6) = -1, θ = π (opposite)
```

**Orthogonal (Example 9):**
```
u = (3,2,-1,4), v = (1,-1,1,0)
u·v = 3 - 2 - 1 + 0 = 0 → orthogonal
```

---

## Section 5.2: Inner Product Spaces (pp. 243-250)

### Key Definition

**Inner product axioms:** (1) ⟨u,v⟩ = ⟨v,u⟩, (2) ⟨u,v+w⟩ = ⟨u,v⟩+⟨u,w⟩, (3) c⟨u,v⟩ = ⟨cu,v⟩, (4) ⟨v,v⟩ ≥ 0 with = 0 iff v = 0.

### Numerical Examples

**Weighted inner product (Example 2):**
```
⟨u,v⟩ = u1v1 + 2u2v2 on R²
```

**Projection (Example 9):**
```
u = (4,2), v = (3,4)
proj_v(u) = (20/25)(3,4) = (12/5, 16/5)
```

**R³ projection (Example 10):**
```
u = (6,2,4), v = (1,2,0)
proj_v(u) = 2(1,2,0) = (2,4,0)
```

---

## Section 5.3: Gram-Schmidt Process (pp. 255-264)

### Algorithm

Given basis {v1,...,vn}:
1. w1 = v1
2. w2 = v2 - (⟨v2,w1⟩/⟨w1,w1⟩)w1
3. w3 = v3 - (⟨v3,w1⟩/⟨w1,w1⟩)w1 - (⟨v3,w2⟩/⟨w2,w2⟩)w2
4. Normalize: ui = wi/‖wi‖

### Numerical Examples

**R² (Example 6):**
```
B = {(1,1), (0,1)}
w1 = (1,1), w2 = (-1/2, 1/2)
u1 = (√2/2, √2/2), u2 = (-√2/2, √2/2)
```

**R³ (Example 7):**
```
B = {(1,1,0), (1,2,0), (0,1,2)}
w1 = (1,1,0), w2 = (-1/2,1/2,0), w3 = (0,0,2)
u1 = (√2/2, √2/2, 0), u2 = (-√2/2, √2/2, 0), u3 = (0,0,1)
```

**R⁴ orthogonal basis (Example 4):**
```
S = {(2,3,2,-2), (1,0,0,1), (-1,0,2,1), (-1,2,-1,1)}
All pairwise dots = 0 → orthogonal → basis for R⁴
```

---

## Section 5.4: Least Squares Analysis (pp. 265-276)

### Key Formula

**Normal equations:** A^T A x̂ = A^T b minimizes ‖Ax - b‖².

### Numerical Examples

**Linear regression (Example 1):**
```
Points: (1,0), (2,1), (3,3)
A = [[1,1],[1,2],[1,3]], b = [0,1,3]
A^T A = [[3,6],[6,14]], A^T b = [4,11]
Solution: c0 = -5/3, c1 = 3/2
Line: y = -5/3 + (3/2)x
```

**Orthogonal complement (Example 3):**
```
S spanned by columns of A = [[1,0],[2,0],[1,0],[0,1]]
S⊥ = N(A^T), basis: {(-2,1,0,0), (-1,0,1,0)}
```

**Four fundamental subspaces (Example 6):**
```
A = [[1,2,0],[0,0,1],[0,0,0],[0,0,0]]
R(A) = span{[1,0,0,0], [0,1,0,0]}
N(A^T) = span{[0,0,1,0], [0,0,0,1]}
R(A^T) = span{[1,2,0], [0,0,1]}
N(A) = span{[-2,1,0]}
```

---

## Section 5.5: Applications of Inner Product Spaces (pp. 277-294)

### Key Formulas

**Cross product:** u × v = [u2v3-u3v2, u3v1-u1v3, u1v2-u2v1]

**Properties:** anticommutative, not associative, u × u = 0, ‖u × v‖ = parallelogram area.

**Triple scalar product:** u · (v × w) = parallelepiped volume = det([u;v;w]).

### Application Notes
- Cross product is perpendicular to both u and v
- ‖u × v‖ = ‖u‖·‖v‖·sin θ
- Triangle area = ½‖AB × AC‖
- Torque τ = r × F
