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
