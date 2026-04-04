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
