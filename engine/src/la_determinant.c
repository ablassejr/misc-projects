#include "la_determinant.h"
#include "la_config.h"
#include "la_elimination.h"
#include <math.h>
#include <string.h>

static LAMatrix* submatrix(const LAMatrix* A, int skip_row, int skip_col) {
    int n = A->rows;
    LAMatrix* sub = la_matrix_new(n - 1, n - 1);
    if (!sub) return NULL;
    int si = 0;
    for (int i = 0; i < n; i++) {
        if (i == skip_row) continue;
        int sj = 0;
        for (int j = 0; j < n; j++) {
            if (j == skip_col) continue;
            sub->data[LA_IDX(si, sj, n - 1)] = A->data[LA_IDX(i, j, n)];
            sj++;
        }
        si++;
    }
    return sub;
}

double la_minor(const LAMatrix* A, int i, int j) {
    LAMatrix* sub = submatrix(A, i, j);
    double det = la_det_cofactor(sub);
    la_matrix_free(sub);
    return det;
}

double la_cofactor(const LAMatrix* A, int i, int j) {
    double sign = ((i + j) % 2 == 0) ? 1.0 : -1.0;
    return sign * la_minor(A, i, j);
}

double la_det_cofactor(const LAMatrix* A) {
    if (A->rows != A->cols) return 0.0;
    int n = A->rows;
    if (n == 1) return A->data[0];
    if (n == 2)
        return A->data[LA_IDX(0, 0, 2)] * A->data[LA_IDX(1, 1, 2)]
             - A->data[LA_IDX(0, 1, 2)] * A->data[LA_IDX(1, 0, 2)];

    double det = 0.0;
    for (int j = 0; j < n; j++)
        det += A->data[LA_IDX(0, j, n)] * la_cofactor(A, 0, j);
    return det;
}

double la_det_elimination(const LAMatrix* A) {
    if (A->rows != A->cols) return 0.0;
    int n = A->rows;
    LAMatrix* m = la_matrix_copy(A);
    int swaps = 0;
    int pivot_row = 0;

    for (int col = 0; col < n && pivot_row < n; col++) {
        int best = la_find_pivot(m, col, pivot_row);
        if (best < 0) {
            la_matrix_free(m);
            return 0.0;
        }
        if (best != pivot_row) {
            la_swap_rows(m, pivot_row, best);
            swaps++;
        }
        double pv = m->data[LA_IDX(pivot_row, col, n)];
        for (int r = pivot_row + 1; r < n; r++) {
            double factor = m->data[LA_IDX(r, col, n)] / pv;
            if (fabs(factor) > LA_EPSILON)
                la_add_scaled_row(m, r, pivot_row, -factor);
        }
        pivot_row++;
    }

    double det = (swaps % 2 == 0) ? 1.0 : -1.0;
    for (int i = 0; i < n; i++)
        det *= m->data[LA_IDX(i, i, n)];

    la_matrix_free(m);
    return det;
}

LAMatrix* la_cofactor_matrix(const LAMatrix* A) {
    if (A->rows != A->cols) return NULL;
    int n = A->rows;
    LAMatrix* C = la_matrix_new(n, n);
    if (!C) return NULL;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            C->data[LA_IDX(i, j, n)] = la_cofactor(A, i, j);
    return C;
}

LAMatrix* la_adjoint(const LAMatrix* A) {
    LAMatrix* cof = la_cofactor_matrix(A);
    if (!cof) return NULL;
    LAMatrix* adj = la_matrix_new(A->rows, A->cols);
    if (!adj) { la_matrix_free(cof); return NULL; }
    int n = A->rows;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            adj->data[LA_IDX(i, j, n)] = cof->data[LA_IDX(j, i, n)];
    la_matrix_free(cof);
    return adj;
}

LAMatrix* la_inverse_adjoint(const LAMatrix* A) {
    double det = la_det_cofactor(A);
    if (fabs(det) < LA_EPSILON) return NULL;
    LAMatrix* adj = la_adjoint(A);
    if (!adj) return NULL;
    int n = A->rows;
    for (int i = 0; i < n * n; i++)
        adj->data[i] /= det;
    return adj;
}

int la_cramers_rule(const LAMatrix* A, const double* b, double* result) {
    if (A->rows != A->cols) return -1;
    int n = A->rows;
    double det_A = la_det_elimination(A);
    if (fabs(det_A) < LA_EPSILON) return -1;

    for (int j = 0; j < n; j++) {
        LAMatrix* Aj = la_matrix_copy(A);
        for (int i = 0; i < n; i++)
            Aj->data[LA_IDX(i, j, n)] = b[i];
        result[j] = la_det_elimination(Aj) / det_A;
        la_matrix_free(Aj);
    }
    return 0;
}
