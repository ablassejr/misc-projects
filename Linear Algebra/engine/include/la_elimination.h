#ifndef LA_ELIMINATION_H
#define LA_ELIMINATION_H

#include "la_matrix.h"

#ifdef __cplusplus
extern "C" {
#endif

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

#ifdef __cplusplus
}
#endif

#endif /* LA_ELIMINATION_H */
