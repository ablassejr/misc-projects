#ifndef LA_MATRIX_H
#define LA_MATRIX_H

#include <stdlib.h>

typedef struct {
    double* data;   /* row-major flat array */
    int rows;
    int cols;
} LAMatrix;

#ifdef __cplusplus
extern "C" {
#endif

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

#ifdef __cplusplus
}
#endif

#endif /* LA_MATRIX_H */
