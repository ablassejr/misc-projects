#include "la_ops.h"
#include "la_config.h"
#include "la_elimination.h"
#include <math.h>
#include <string.h>

LAMatrix* la_matrix_add(const LAMatrix* A, const LAMatrix* B) {
    if (A->rows != B->rows || A->cols != B->cols) return NULL;
    LAMatrix* C = la_matrix_new(A->rows, A->cols);
    if (!C) return NULL;
    int n = A->rows * A->cols;
    for (int i = 0; i < n; i++)
        C->data[i] = A->data[i] + B->data[i];
    return C;
}

LAMatrix* la_matrix_scalar_mul(const LAMatrix* A, double scalar) {
    LAMatrix* C = la_matrix_new(A->rows, A->cols);
    if (!C) return NULL;
    int n = A->rows * A->cols;
    for (int i = 0; i < n; i++)
        C->data[i] = A->data[i] * scalar;
    return C;
}

LAMatrix* la_matrix_mul(const LAMatrix* A, const LAMatrix* B) {
    if (A->cols != B->rows) return NULL;
    LAMatrix* C = la_matrix_new(A->rows, B->cols);
    if (!C) return NULL;
    for (int i = 0; i < A->rows; i++)
        for (int j = 0; j < B->cols; j++) {
            double sum = 0.0;
            for (int k = 0; k < A->cols; k++)
                sum += A->data[LA_IDX(i, k, A->cols)] * B->data[LA_IDX(k, j, B->cols)];
            C->data[LA_IDX(i, j, C->cols)] = sum;
        }
    return C;
}

LAMatrix* la_matrix_mul_ikj(const LAMatrix* A, const LAMatrix* B) {
    if (A->cols != B->rows) return NULL;
    LAMatrix* C = la_matrix_new(A->rows, B->cols);
    if (!C) return NULL;
    for (int i = 0; i < A->rows; i++)
        for (int k = 0; k < A->cols; k++) {
            double a_ik = A->data[LA_IDX(i, k, A->cols)];
            for (int j = 0; j < B->cols; j++)
                C->data[LA_IDX(i, j, C->cols)] += a_ik * B->data[LA_IDX(k, j, B->cols)];
        }
    return C;
}

LAMatrix* la_matrix_transpose(const LAMatrix* A) {
    LAMatrix* T = la_matrix_new(A->cols, A->rows);
    if (!T) return NULL;
    for (int i = 0; i < A->rows; i++)
        for (int j = 0; j < A->cols; j++)
            T->data[LA_IDX(j, i, T->cols)] = A->data[LA_IDX(i, j, A->cols)];
    return T;
}

LAMatrix* la_matrix_inverse(const LAMatrix* A) {
    if (A->rows != A->cols) return NULL;
    int n = A->rows;

    LAMatrix* aug = la_matrix_new(n, 2 * n);
    if (!aug) return NULL;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++)
            aug->data[LA_IDX(i, j, 2 * n)] = A->data[LA_IDX(i, j, n)];
        aug->data[LA_IDX(i, n + i, 2 * n)] = 1.0;
    }

    la_to_rref(aug);

    /* Check that left half is identity (i.e., A was nonsingular) */
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double expected = (i == j) ? 1.0 : 0.0;
            if (fabs(aug->data[LA_IDX(i, j, 2 * n)] - expected) > LA_EPSILON) {
                la_matrix_free(aug);
                return NULL;
            }
        }
    }

    LAMatrix* inv = la_matrix_new(n, n);
    if (!inv) { la_matrix_free(aug); return NULL; }

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            inv->data[LA_IDX(i, j, n)] = aug->data[LA_IDX(i, n + j, 2 * n)];

    la_matrix_free(aug);
    return inv;
}

int la_lu_factorize(const LAMatrix* A, LAMatrix** L, LAMatrix** U) {
    if (A->rows != A->cols) return -1;
    int n = A->rows;

    *U = la_matrix_copy(A);
    *L = la_matrix_identity(n);
    if (!*U || !*L) return -1;

    for (int k = 0; k < n; k++) {
        double pivot = (*U)->data[LA_IDX(k, k, n)];
        if (fabs(pivot) < LA_EPSILON) {
            la_matrix_free(*L); *L = NULL;
            la_matrix_free(*U); *U = NULL;
            return -1;
        }
        for (int i = k + 1; i < n; i++) {
            double factor = (*U)->data[LA_IDX(i, k, n)] / pivot;
            (*L)->data[LA_IDX(i, k, n)] = factor;
            for (int j = k; j < n; j++)
                (*U)->data[LA_IDX(i, j, n)] -= factor * (*U)->data[LA_IDX(k, j, n)];
        }
    }
    return 0;
}

void la_forward_sub(const LAMatrix* L, const double* b, double* y, int n) {
    for (int i = 0; i < n; i++) {
        double sum = b[i];
        for (int j = 0; j < i; j++)
            sum -= L->data[LA_IDX(i, j, n)] * y[j];
        y[i] = sum / L->data[LA_IDX(i, i, n)];
    }
}

void la_back_sub(const LAMatrix* U, const double* y, double* x, int n) {
    for (int i = n - 1; i >= 0; i--) {
        double sum = y[i];
        for (int j = i + 1; j < n; j++)
            sum -= U->data[LA_IDX(i, j, n)] * x[j];
        x[i] = sum / U->data[LA_IDX(i, i, n)];
    }
}

LAMatrix* la_elementary_swap(int n, int i, int j) {
    LAMatrix* E = la_matrix_identity(n);
    if (!E) return NULL;
    E->data[LA_IDX(i, i, n)] = 0.0;
    E->data[LA_IDX(j, j, n)] = 0.0;
    E->data[LA_IDX(i, j, n)] = 1.0;
    E->data[LA_IDX(j, i, n)] = 1.0;
    return E;
}

LAMatrix* la_elementary_scale(int n, int i, double c) {
    LAMatrix* E = la_matrix_identity(n);
    if (!E) return NULL;
    E->data[LA_IDX(i, i, n)] = c;
    return E;
}

LAMatrix* la_elementary_add(int n, int target, int source, double c) {
    LAMatrix* E = la_matrix_identity(n);
    if (!E) return NULL;
    E->data[LA_IDX(target, source, n)] = c;
    return E;
}
