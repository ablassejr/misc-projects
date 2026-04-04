#include "la_vecspace.h"
#include "la_config.h"
#include "la_elimination.h"
#include "la_ops.h"
#include <math.h>
#include <string.h>

int la_rank(const LAMatrix* A) {
    LAMatrix* m = la_matrix_copy(A);
    int num_pivots = la_to_rref(m);
    la_matrix_free(m);
    return num_pivots;
}

int la_nullity(const LAMatrix* A) {
    return A->cols - la_rank(A);
}

int la_null_space(const LAMatrix* A, LAMatrix** basis) {
    int m = A->rows, n = A->cols;
    LAMatrix* rref = la_matrix_copy(A);
    la_to_rref(rref);

    int is_pivot_col[n];
    int pivot_col[n];
    int free_col[n];
    int num_pivots = 0, num_free = 0;

    memset(is_pivot_col, 0, (size_t)n * sizeof(int));
    int pr = 0;
    for (int j = 0; j < n && pr < m; j++) {
        if (fabs(rref->data[LA_IDX(pr, j, n)]) > LA_EPSILON) {
            pivot_col[num_pivots++] = j;
            is_pivot_col[j] = 1;
            pr++;
        }
    }
    for (int j = 0; j < n; j++) {
        if (!is_pivot_col[j])
            free_col[num_free++] = j;
    }

    if (num_free == 0) {
        *basis = NULL;
        la_matrix_free(rref);
        return 0;
    }

    *basis = la_matrix_new(n, num_free);
    if (!*basis) { la_matrix_free(rref); return 0; }

    for (int f = 0; f < num_free; f++) {
        int fc = free_col[f];
        (*basis)->data[LA_IDX(fc, f, num_free)] = 1.0;
        for (int p = 0; p < num_pivots; p++) {
            int pc = pivot_col[p];
            (*basis)->data[LA_IDX(pc, f, num_free)] = -rref->data[LA_IDX(p, fc, n)];
        }
    }

    la_matrix_free(rref);
    return num_free;
}

int la_column_space(const LAMatrix* A, LAMatrix** basis) {
    int m = A->rows, n = A->cols;
    LAMatrix* rref = la_matrix_copy(A);
    la_to_rref(rref);

    int pivot_cols[n];
    int num_pivots = 0;
    int pr = 0;
    for (int j = 0; j < n && pr < m; j++) {
        if (fabs(rref->data[LA_IDX(pr, j, n)]) > LA_EPSILON) {
            pivot_cols[num_pivots++] = j;
            pr++;
        }
    }

    la_matrix_free(rref);

    if (num_pivots == 0) {
        *basis = NULL;
        return 0;
    }

    *basis = la_matrix_new(m, num_pivots);
    if (!*basis) return 0;

    for (int p = 0; p < num_pivots; p++)
        for (int i = 0; i < m; i++)
            (*basis)->data[LA_IDX(i, p, num_pivots)] = A->data[LA_IDX(i, pivot_cols[p], n)];

    return num_pivots;
}

int la_row_space(const LAMatrix* A, LAMatrix** basis) {
    int n = A->cols;
    LAMatrix* rref = la_matrix_copy(A);
    la_to_rref(rref);

    int rank = 0;
    for (int i = 0; i < rref->rows; i++) {
        int nonzero = 0;
        for (int j = 0; j < n; j++)
            if (fabs(rref->data[LA_IDX(i, j, n)]) > LA_EPSILON) { nonzero = 1; break; }
        if (nonzero) rank++;
    }

    if (rank == 0) {
        *basis = NULL;
        la_matrix_free(rref);
        return 0;
    }

    *basis = la_matrix_new(rank, n);
    if (!*basis) { la_matrix_free(rref); return 0; }

    int row = 0;
    for (int i = 0; i < rref->rows && row < rank; i++) {
        int nonzero = 0;
        for (int j = 0; j < n; j++)
            if (fabs(rref->data[LA_IDX(i, j, n)]) > LA_EPSILON) { nonzero = 1; break; }
        if (nonzero) {
            memcpy(&(*basis)->data[LA_IDX(row, 0, n)],
                   &rref->data[LA_IDX(i, 0, n)],
                   (size_t)n * sizeof(double));
            row++;
        }
    }

    la_matrix_free(rref);
    return rank;
}

int la_is_independent(const double* vectors, int num_vectors, int dim) {
    LAMatrix* M = la_matrix_new(dim, num_vectors);
    if (!M) return 0;
    for (int v = 0; v < num_vectors; v++)
        for (int i = 0; i < dim; i++)
            M->data[LA_IDX(i, v, num_vectors)] = vectors[v * dim + i];
    int r = la_rank(M);
    la_matrix_free(M);
    return r == num_vectors;
}

int la_is_in_span(const double* v, const double* vectors, int num_vectors, int dim) {
    LAMatrix* aug = la_matrix_new(dim, num_vectors + 1);
    if (!aug) return 0;
    for (int c = 0; c < num_vectors; c++)
        for (int i = 0; i < dim; i++)
            aug->data[LA_IDX(i, c, num_vectors + 1)] = vectors[c * dim + i];
    for (int i = 0; i < dim; i++)
        aug->data[LA_IDX(i, num_vectors, num_vectors + 1)] = v[i];

    LAMatrix* without_v = la_matrix_new(dim, num_vectors);
    for (int c = 0; c < num_vectors; c++)
        for (int i = 0; i < dim; i++)
            without_v->data[LA_IDX(i, c, num_vectors)] = vectors[c * dim + i];

    int rank_with = la_rank(aug);
    int rank_without = la_rank(without_v);

    la_matrix_free(aug);
    la_matrix_free(without_v);
    return rank_with == rank_without;
}

LAMatrix* la_change_of_basis(const LAMatrix* old_basis, const LAMatrix* new_basis) {
    LAMatrix* new_inv = la_matrix_inverse(new_basis);
    if (!new_inv) return NULL;
    LAMatrix* P = la_matrix_mul(new_inv, old_basis);
    la_matrix_free(new_inv);
    return P;
}
