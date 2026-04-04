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
