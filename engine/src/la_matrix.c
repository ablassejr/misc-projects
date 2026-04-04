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
