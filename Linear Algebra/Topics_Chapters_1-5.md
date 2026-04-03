# Elementary Linear Algebra (8e, Ron Larson)
## Topics Covered: Chapters 1-5

---

## Chapter 1: Systems of Linear Equations (pp. 1-38)

### 1.1 Introduction to Systems of Linear Equations
- Definition of a linear equation in *n* variables
- Solutions and solution sets
- Parametric representation of solution sets
- Systems of linear equations (linear systems)
- Consistent vs. inconsistent systems
- Three types of solution sets: exactly one solution, infinitely many solutions, no solution
- Row-echelon form
- Back-substitution
- Gaussian elimination
- Operations that produce equivalent systems

### 1.2 Gaussian Elimination and Gauss-Jordan Elimination
- Definition of a matrix (size, entries, square matrices)
- Augmented matrices and coefficient matrices
- Elementary row operations (interchange, scalar multiply, row addition)
- Row-equivalent matrices
- Row-echelon form and reduced row-echelon form
- Gaussian elimination with back-substitution (algorithm)
- Gauss-Jordan elimination
- Homogeneous systems of linear equations
- Trivial vs. nontrivial solutions

### 1.3 Applications of Systems of Linear Equations
- Polynomial curve fitting
- Network analysis (traffic flow, electrical networks)
- Applications to science and engineering

---

## Chapter 2: Matrices (pp. 39-108)

### 2.1 Operations with Matrices
- Equality of matrices
- Matrix addition and scalar multiplication
- Matrix subtraction
- Matrix multiplication (definition, row-column rule)
- Properties of matrix multiplication (non-commutativity)
- The identity matrix
- Properties of the transpose

### 2.2 Properties of Matrix Operations
- Properties of matrix addition (commutative, associative, additive identity, additive inverse)
- Properties of scalar multiplication (associative, distributive)
- Properties of matrix multiplication (associative, distributive, identity)
- Properties of the transpose (double transpose, sum, scalar, product)
- The zero matrix and its properties
- Cancellation issues in matrix algebra

### 2.3 The Inverse of a Matrix
- Definition of the inverse (invertible/nonsingular vs. noninvertible/singular)
- Uniqueness of the inverse (Theorem 2.7)
- Finding the inverse of a matrix
- The inverse of a 2x2 matrix (formula)
- Using Gauss-Jordan elimination to find the inverse
- Using the inverse to solve systems of linear equations (AX = B implies X = A^(-1)B)

### 2.4 Elementary Matrices
- Definition of elementary matrices
- Relationship between elementary row operations and elementary matrices
- Row equivalence and elementary matrices
- Conditions for invertibility
- LU-factorization (Doolittle's method)

### 2.5 Markov Chains
- Stochastic matrices (transition matrices)
- State matrices and state vectors
- Markov chains and regular Markov chains
- Steady-state probability vectors
- Absorbing Markov chains

### 2.6 More Applications of Matrix Operations
- Cryptography (encoding and decoding messages)
- Leontief input-output models
- The Leontief production equation
- Demand matrices and output matrices

---

## Chapter 3: Determinants (pp. 109-148)

### 3.1 The Determinant of a Matrix
- Determinant of a 1x1 and 2x2 matrix
- Minors and cofactors
- Cofactor expansion (expansion by cofactors)
- Determinant of a triangular matrix
- Determinant of matrices of any size (recursive definition)

### 3.2 Determinants and Elementary Operations
- Effect of elementary row operations on determinants
  - Row interchange: changes sign
  - Scalar row multiplication: multiplies determinant by the scalar
  - Row addition: determinant unchanged
- Determinant of a product: det(AB) = det(A) * det(B)
- Conditions for zero determinant (row of zeros, proportional rows)
- Determinant of an inverse: det(A^(-1)) = 1/det(A)
- Determinant of a transpose: det(A^T) = det(A)

### 3.3 Properties of Determinants
- Determinant of a matrix product
- Determinant of a scalar multiple of a matrix
- Determinant of an invertible matrix (nonzero iff invertible)
- Equivalent conditions for a singular matrix
- Summary of equivalent conditions for nonsingular matrices

### 3.4 Applications of Determinants
- Cramer's Rule (for 2x2 and nxn systems)
- Adjoint of a matrix (matrix of cofactors, transposed)
- Formula for the inverse using the adjoint: A^(-1) = (1/det(A)) * adj(A)
- Area of a triangle using determinants
- Volume of a tetrahedron
- Test for collinear points
- Two-point form of the equation of a line
- Three-point form of the equation of a plane

---

## Chapter 4: Vector Spaces (pp. 151-230)

### 4.1 Vectors in R^n
- n-tuples and vectors in R^n
- Vector addition and scalar multiplication in R^n
- Properties of vector operations (10 axioms preview)
- Linear combinations of vectors
- Standard unit vectors (e1, e2, ..., en)

### 4.2 Vector Spaces
- Definition of a vector space (10 axioms)
  - Closure under addition and scalar multiplication
  - Commutativity, associativity of addition
  - Additive identity and inverse
  - Scalar multiplication properties (associativity, distributivity, identity)
- Examples of vector spaces: R^n, matrices, polynomials, continuous functions
- Properties of vector spaces (uniqueness of zero, additive inverse, zero scalar)

### 4.3 Subspaces of Vector Spaces
- Definition of a subspace
- Test for a subspace (closure under addition and scalar multiplication, nonempty)
- The trivial subspace ({0}) and the whole space
- Subspaces of R^2 (origin, lines through origin, R^2)
- Subspaces of R^3 (origin, lines through origin, planes through origin, R^3)
- The subspace spanned by a set of vectors

### 4.4 Spanning Sets and Linear Independence
- Spanning sets for a vector space
- Linear independence and linear dependence
- Testing for linear independence (homogeneous system approach)
- Relationship between number of vectors and dimension
- Wronskian test for linear independence of functions

### 4.5 Basis and Dimension
- Definition of a basis (linearly independent spanning set)
- Standard bases for R^n, P_n, M_(m,n)
- Uniqueness of representation (coordinate uniqueness)
- Dimension of a vector space
- Theorems relating number of vectors, linear independence, and spanning
- Every linearly independent set can be extended to a basis

### 4.6 Rank of a Matrix and Systems of Linear Equations
- Row space and column space of a matrix
- Rank of a matrix (dimension of row space = dimension of column space)
- Nullity of a matrix (dimension of solution space)
- Rank-Nullity Theorem (Dimension Theorem): rank(A) + nullity(A) = n
- Relationship between rank and solutions of Ax = b
- Conditions for consistency of linear systems using rank

### 4.7 Coordinates and Change of Basis
- Coordinate representation relative to a basis
- Coordinate vectors
- Transition matrices (change of basis matrices)
- Finding the transition matrix using Gauss-Jordan elimination
- Inverse of a transition matrix

### 4.8 Applications of Vector Spaces
- Differential equations and vector spaces
- Solution spaces of homogeneous linear differential equations
- Wronskian and linear independence of solutions
- Conic sections and rotation of axes

---

## Chapter 5: Inner Product Spaces (pp. 231-294)

### 5.1 Length and Dot Product in R^n
- The dot product (Euclidean inner product) in R^n
- Properties of the dot product
- Length (norm) of a vector
- Unit vectors and normalizing a vector
- Distance between two vectors
- Angle between two vectors (cosine formula)
- Orthogonal vectors
- The Cauchy-Schwarz Inequality
- The Triangle Inequality

### 5.2 Inner Product Spaces
- Definition of an inner product (4 axioms: positivity, symmetry, linearity, positive definiteness)
- General inner product spaces
- Examples: weighted dot product, integral-based inner product for functions
- Norm, distance, and angle in inner product spaces
- Orthogonality in inner product spaces
- Pythagorean Theorem generalization
- Orthogonal complement of a subspace

### 5.3 Orthonormal Bases: Gram-Schmidt Process
- Orthogonal and orthonormal sets
- Orthogonal and orthonormal bases
- Coordinates relative to an orthonormal basis (Fourier coefficients)
- Orthogonal projection onto a subspace
- The Gram-Schmidt orthogonalization process
- Converting an arbitrary basis to an orthonormal basis

### 5.4 Mathematical Models and Least Squares Analysis
- Least squares regression
- The normal equations (A^T A x = A^T b)
- Least squares solution when Ax = b is inconsistent
- Linear least squares regression (best-fit line)
- Polynomial least squares regression (quadratic, cubic fits)
- Least squares approximation of functions (Fourier approximations)

### 5.5 Applications of Inner Product Spaces
- Cross product in R^3
- Properties of the cross product (anticommutativity, distributivity)
- Geometric properties: area of a parallelogram, volume of a parallelepiped (triple scalar product)
- Applications to physics (work, projections)
- Fourier approximations

---

## Key Theorems and Results Across Chapters 1-5

| Theorem | Chapter | Description |
|---------|---------|-------------|
| Number of Solutions | 1 | A system has exactly one, infinitely many, or no solutions |
| Homogeneous System | 1 | A homogeneous system with more variables than equations has nontrivial solutions |
| Invertible Matrix Theorem | 2-4 | Equivalent conditions for invertibility (built across chapters) |
| Determinant Product | 3 | det(AB) = det(A)det(B) |
| Cramer's Rule | 3 | Solve Ax = b using determinants when A is invertible |
| Rank-Nullity Theorem | 4 | rank(A) + nullity(A) = n (number of columns) |
| Cauchy-Schwarz Inequality | 5 | |u . v| <= ||u|| * ||v|| |
| Triangle Inequality | 5 | ||u + v|| <= ||u|| + ||v|| |
| Gram-Schmidt Process | 5 | Any basis can be orthogonalized |
| Least Squares Theorem | 5 | A^T Ax = A^T b always has a solution |

---

*Source: Elementary Linear Algebra, 8th Edition by Ron Larson (Cengage Learning, 2017)*
