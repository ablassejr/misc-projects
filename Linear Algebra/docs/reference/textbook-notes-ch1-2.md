# Textbook Notes: Chapters 1-2
## Elementary Linear Algebra (Larson, 8e)

Extracted examples, definitions, and numerical values for Colab notebook content.

---

## Section 1.1: Introduction to Systems of Linear Equations (pp. 2-12)

### Key Definitions

**Linear equation in n variables:** a1*x1 + a2*x2 + ... + an*xn = b, where coefficients and constant term are real numbers. Variables appear only to the first power.

**Consistent system:** Has at least one solution. **Inconsistent system:** Has no solution.

**Number of Solutions:** Precisely one of: (1) exactly one solution, (2) infinitely many, (3) no solution.

**Operations producing equivalent systems:** (1) interchange two equations, (2) multiply by nonzero constant, (3) add a multiple of one equation to another.

### Numerical Examples

**3x3 unique solution (Example 7):**
```
x - 2y + 3z =  9
-x + 3y      = -4
2x - 5y + 5z = 17
Solution: x = 1, y = -1, z = 2
```

**Inconsistent system (Example 8):**
```
x1 - 3x2 +  x3 =  1
2x1 -  x2 - 2x3 =  2
x1 + 2x2 - 3x3 = -1
Leads to 0 = -2 → NO SOLUTION
```

**Infinitely many solutions (Example 9):**
```
x2 -  x3 =  0
x1      - 3x3 = -1
-x1 + 3x2       =  1
Solution: x1 = 3t - 1, x2 = t, x3 = t
```

**2x2 three cases (Example 4):**
```
(a) x + y = 3, x - y = -1       → Unique: x=1, y=2
(b) x + y = 3, 2x + 2y = 6     → Infinite: x=3-t, y=t
(c) x + y = 3, x + y = 1       → No solution
```

---

## Section 1.2: Gaussian Elimination and Gauss-Jordan Elimination (pp. 13-24)

### Key Definitions

**Row-Echelon Form (REF):** (1) zero rows at bottom, (2) leading entry is 1, (3) each leading 1 is right of the one above.

**Reduced Row-Echelon Form (RREF):** REF plus every column with a leading 1 has zeros everywhere else.

**Homogeneous system:** Ax = 0. Always consistent (trivial solution). If fewer equations than variables → infinitely many solutions (Theorem 1.1).

### Numerical Examples

**Full Gaussian elimination (Example 3):**
```
Augmented: [[1,-2,3,9],[-1,3,0,-4],[2,-5,5,17]]

R2 + R1 → R2:     [[1,-2,3,9],[0,1,3,5],[2,-5,5,17]]
R3 + (-2)R1 → R3:  [[1,-2,3,9],[0,1,3,5],[0,-1,-1,-1]]
R3 + R2 → R3:      [[1,-2,3,9],[0,1,3,5],[0,0,2,4]]
(1/2)R3 → R3:      [[1,-2,3,9],[0,1,3,5],[0,0,1,2]]

Solution: x=1, y=-1, z=2
```

**Gauss-Jordan to RREF (Example 7):**
```
From REF: [[1,-2,3,9],[0,1,3,5],[0,0,1,2]]

R1 + 2R2 → R1:   [[1,0,9,19],[0,1,3,5],[0,0,1,2]]
R2 + (-3)R3 → R2: [[1,0,9,19],[0,1,0,-1],[0,0,1,2]]
R1 + (-9)R3 → R1: [[1,0,0,1],[0,1,0,-1],[0,0,1,2]]

RREF → x=1, y=-1, z=2
```

**4x4 system (Example 5):**
```
Augmented: [[0,1,1,-2,-3],[1,2,-1,0,2],[2,4,1,-3,-2],[1,-4,-7,-1,-19]]
Solution: x1=-1, x2=2, x3=1, x4=3
```

**Homogeneous system (Example 9):**
```
x1 - x2 + 3x3 = 0
2x1 + x2 + 3x3 = 0
RREF: [[1,0,2,0],[0,1,-1,0]]
Solution: x1 = -2t, x2 = t, x3 = t
```

---

## Section 1.3: Applications of Systems (pp. 25-34)

### Numerical Examples

**Polynomial curve fitting (Example 1):**
```
Points: (1,4), (2,0), (3,12)
System: a0 + a1 + a2 = 4, a0 + 2a1 + 4a2 = 0, a0 + 3a1 + 9a2 = 12
Solution: a0 = 24, a1 = -28, a2 = 8
p(x) = 24 - 28x + 8x²
```

**Electrical network / Kirchhoff's Laws (Example 6):**
```
R1=3Ω, R2=2Ω, R3=4Ω. Voltages: 7V, 8V.
I1 - I2 + I3 = 0
3I1 + 2I2 = 7
2I2 + 4I3 = 8
Solution: I1 = 1A, I2 = 2A, I3 = 1A
```

**Network flow (Example 5):**
```
5-junction network. System:
x1 + x2 = 20, x3 - x4 = -20, x2 + x3 = 20, x1 - x5 = -10, -x4 + x5 = -10
Parametric (t = x5): x1=t-10, x2=-t+30, x3=t-10, x4=t+10, x5=t
```

---

## Section 2.1: Operations with Matrices (pp. 40-51)

### Key Definitions

**Matrix multiplication:** A(m×n) × B(n×p) = C(m×p), where c_ij = Σ a_ik * b_kj.

**System as matrix equation:** Ax = b is consistent iff b is a linear combination of columns of A.

### Numerical Examples

**Matrix multiplication (Example 4):**
```
A = [[-1,3],[4,-2],[5,0]], B = [[-3,2],[-4,1]]
AB = [[-9,1],[-4,6],[-15,10]]
Note: BA is NOT defined.
```

**Non-commutativity:**
```
A = [[1,3],[2,-1]], B = [[2,-1],[0,2]]
AB = [[2,5],[4,-4]], BA = [[0,7],[4,-2]]
AB ≠ BA
```

**Concession sales:**
```
[[120,250,305],[207,140,419],[29,120,190]] × [[2.00],[3.00],[2.75]] = [[1828.75],[1986.25],[940.50]]
```

---

## Section 2.2: Properties of Matrix Operations (pp. 52-61)

### Key Theorems
- A + B = B + A (commutative)
- A(BC) = (AB)C (associative)
- (AB)^T = B^T A^T (transpose reverses order)
- AB ≠ BA in general (non-commutative)

### Numerical Examples

**Cancellation failure (Example 5):**
```
A = [[1,3],[0,1]], B = [[2,4],[2,3]], C = [[1,-2],[-1,2]]
AC = [[-2,4],[-1,2]], BC = [[-2,4],[-1,2]]
AC = BC but A ≠ B (cancellation fails)
```

**AA^T is symmetric (Example 10):**
```
A = [[1,3],[0,-2],[-2,-1]]
AA^T = [[10,-6,-5],[-6,4,2],[-5,2,5]]
(AA^T)^T = AA^T ✓
```

---

## Section 2.3: The Inverse of a Matrix (pp. 62-73)

### Key Definitions

**2×2 inverse:** A = [[a,b],[c,d]], A⁻¹ = (1/(ad-bc)) × [[d,-b],[-c,a]] when ad-bc ≠ 0.

**Gauss-Jordan method:** [A|I] → RREF → [I|A⁻¹] if A is invertible.

### Numerical Examples

**2×2 inverse (Example 5):**
```
A = [[3,-1],[-2,2]]
ad-bc = 4, A⁻¹ = [[1/2,1/4],[1/2,3/4]]

B = [[3,-1],[-6,2]]
ad-bc = 0 → SINGULAR
```

**3×3 inverse via Gauss-Jordan (Example 3):**
```
A = [[1,-1,0],[1,0,-1],[-6,2,3]]
A⁻¹ = [[-2,-3,-1],[-3,-3,-1],[-2,-4,-1]]
```

**Solving multiple systems (Example 8):**
```
A = [[2,3,1],[3,3,1],[2,4,1]]
A⁻¹ = [[-1,1,0],[-1,0,1],[6,-2,-3]]
b₁ = [-1,1,-2] → x = [2,-1,-2]
b₂ = [4,8,5]   → x = [4,1,-7]
```

---

## Section 2.4: Elementary Matrices (pp. 74-83)

### Key Definitions

**LU-Factorization:** A = LU where L is lower triangular (1s on diagonal, multipliers below) and U is upper triangular (the REF).

### Numerical Examples

**LU-Factorization (Example 5b):**
```
A = [[1,-3,0],[0,1,3],[2,-10,2]]
L = [[1,0,0],[0,1,0],[2,-4,1]]
U = [[1,-3,0],[0,1,3],[0,0,14]]
Verify: L × U = A
```

**LU solve (Example 7):**
```
System: x1-3x2=-5, x2+3x3=-1, 2x1-10x2+2x3=-20
Step 1 (Ly=b): y = [-5,-1,-14]
Step 2 (Ux=y): x = [1,2,-1]
```

---

## Section 2.5: Markov Chains (pp. 84-93)

### Key Definitions

**Stochastic matrix:** Each column sums to 1, all entries ∈ [0,1].
**State matrix:** Column vector, entries sum to 1.
**Steady state:** P × X̄ = X̄ with entries summing to 1.

### Numerical Examples

**Consumer preference (Examples 2-5):**
```
P = [[0.70,0.15,0.15],[0.20,0.80,0.15],[0.10,0.05,0.70]]
X0 = [0.15,0.20,0.65]

Convergence: X15 ≈ [0.3333, 0.4756, 0.1911]

Steady state (algebraic): x1=1/3, x2=10/21, x3=4/21
≈ [0.3333, 0.4762, 0.1905]
```

**Absorbing chain (Example 7a):**
```
P = [[0.4,0,0],[0,1,0.5],[0.6,0,0.5]]
Steady state: X̄ = [0,1,0] (state 2 absorbs everything)
```

---

## Section 2.6: Applications of Matrix Operations (pp. 94-103)

### Numerical Examples

**Hill cipher encoding (Example 2):**
```
Message: "MEET ME MONDAY"
Encoding matrix: A = [[1,-2,2],[-1,1,3],[1,-1,-4]]
Uncoded blocks: [13,5,5], [20,0,13], [5,0,13], [15,14,4], [1,25,0]
Coded: 13,-26,21,33,-53,-12,18,-23,-42,5,-20,56,-24,23,77
```

**Leontief model (Example 5):**
```
D = [[0.10,0.43,0.00],[0.15,0.00,0.37],[0.23,0.03,0.02]]
E = [20000,30000,25000]
X = (I-D)⁻¹ × E ≈ [46750, 50950, 37800]
```

**Least squares regression (Example 7):**
```
Points: (1,1), (2,2), (3,4), (4,4), (5,6)
X = [[1,1],[1,2],[1,3],[1,4],[1,5]], Y = [1,2,4,4,6]
Line: y = -0.2 + 1.2x, SSE = 0.8
```
