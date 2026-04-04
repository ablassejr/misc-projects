#include "la_elimination.h"
#include "la_config.h"
#include <math.h>
#include <string.h>

void la_swap_rows(LAMatrix* mat, int i, int j) {
    if (i == j) return;
    for (int k = 0; k < mat->cols; k++) {
        double tmp = mat->data[LA_IDX(i, k, mat->cols)];
        mat->data[LA_IDX(i, k, mat->cols)] = mat->data[LA_IDX(j, k, mat->cols)];
        mat->data[LA_IDX(j, k, mat->cols)] = tmp;
    }
}

void la_scale_row(LAMatrix* mat, int i, double scalar) {
    for (int k = 0; k < mat->cols; k++)
        mat->data[LA_IDX(i, k, mat->cols)] *= scalar;
}

void la_add_scaled_row(LAMatrix* mat, int target, int source, double scalar) {
    for (int k = 0; k < mat->cols; k++)
        mat->data[LA_IDX(target, k, mat->cols)] +=
            scalar * mat->data[LA_IDX(source, k, mat->cols)];
}

int la_find_pivot(const LAMatrix* mat, int col, int start_row) {
    int best = -1;
    double best_val = LA_EPSILON;
    for (int r = start_row; r < mat->rows; r++) {
        double v = fabs(mat->data[LA_IDX(r, col, mat->cols)]);
        if (v > best_val) {
            best_val = v;
            best = r;
        }
    }
    return best;
}

int la_to_ref(LAMatrix* mat) {
    int swaps = 0;
    int pivot_row = 0;

    for (int col = 0; col < mat->cols && pivot_row < mat->rows; col++) {
        int best = la_find_pivot(mat, col, pivot_row);
        if (best < 0) continue;

        if (best != pivot_row) {
            la_swap_rows(mat, pivot_row, best);
            swaps++;
        }

        double pv = mat->data[LA_IDX(pivot_row, col, mat->cols)];
        la_scale_row(mat, pivot_row, 1.0 / pv);

        for (int r = pivot_row + 1; r < mat->rows; r++) {
            double factor = mat->data[LA_IDX(r, col, mat->cols)];
            if (fabs(factor) > LA_EPSILON)
                la_add_scaled_row(mat, r, pivot_row, -factor);
        }
        pivot_row++;
    }
    return swaps;
}

int la_to_rref(LAMatrix* mat) {
    int swaps = 0;
    int pivot_row = 0;
    int pivot_cols[mat->cols];
    int num_pivots = 0;

    for (int col = 0; col < mat->cols && pivot_row < mat->rows; col++) {
        int best = la_find_pivot(mat, col, pivot_row);
        if (best < 0) continue;

        if (best != pivot_row) {
            la_swap_rows(mat, pivot_row, best);
            swaps++;
        }

        double pv = mat->data[LA_IDX(pivot_row, col, mat->cols)];
        la_scale_row(mat, pivot_row, 1.0 / pv);

        for (int r = pivot_row + 1; r < mat->rows; r++) {
            double factor = mat->data[LA_IDX(r, col, mat->cols)];
            if (fabs(factor) > LA_EPSILON)
                la_add_scaled_row(mat, r, pivot_row, -factor);
        }

        pivot_cols[num_pivots] = col;
        num_pivots++;
        pivot_row++;
    }

    for (int p = num_pivots - 1; p >= 0; p--) {
        int col = pivot_cols[p];
        int row = p;
        for (int r = row - 1; r >= 0; r--) {
            double factor = mat->data[LA_IDX(r, col, mat->cols)];
            if (fabs(factor) > LA_EPSILON)
                la_add_scaled_row(mat, r, row, -factor);
        }
    }

    (void)swaps;
    return num_pivots;
}

int la_solve(const LAMatrix* augmented, double* result) {
    int n_vars = augmented->cols - 1;
    LAMatrix* m = la_matrix_copy(augmented);
    int num_pivots = la_to_rref(m);

    int pivot_col[m->rows];
    int pcount = 0;
    for (int i = 0; i < m->rows && pcount < num_pivots; i++) {
        for (int j = 0; j < n_vars; j++) {
            if (fabs(m->data[LA_IDX(i, j, m->cols)]) > LA_EPSILON) {
                pivot_col[pcount++] = j;
                break;
            }
        }
    }

    for (int i = 0; i < m->rows; i++) {
        int all_zero = 1;
        for (int j = 0; j < n_vars; j++) {
            if (fabs(m->data[LA_IDX(i, j, m->cols)]) > LA_EPSILON) {
                all_zero = 0;
                break;
            }
        }
        if (all_zero && fabs(m->data[LA_IDX(i, n_vars, m->cols)]) > LA_EPSILON) {
            la_matrix_free(m);
            return -1;
        }
    }

    if (pcount < n_vars) {
        la_matrix_free(m);
        return 1;
    }

    if (result) {
        for (int i = 0; i < pcount && i < n_vars; i++)
            result[pivot_col[i]] = m->data[LA_IDX(i, n_vars, m->cols)];
    }

    la_matrix_free(m);
    return 0;
}
