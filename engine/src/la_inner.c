#include "la_inner.h"
#include "la_config.h"
#include "la_ops.h"
#include "la_elimination.h"
#include <math.h>
#include <string.h>

double la_dot(const double* u, const double* v, int n) {
    double sum = 0.0;
    for (int i = 0; i < n; i++)
        sum += u[i] * v[i];
    return sum;
}

double la_norm(const double* v, int n) {
    return sqrt(la_dot(v, v, n));
}

void la_normalize(const double* v, double* result, int n) {
    double len = la_norm(v, n);
    if (len < LA_EPSILON) {
        memset(result, 0, (size_t)n * sizeof(double));
        return;
    }
    for (int i = 0; i < n; i++)
        result[i] = v[i] / len;
}

double la_distance(const double* u, const double* v, int n) {
    double sum = 0.0;
    for (int i = 0; i < n; i++) {
        double d = u[i] - v[i];
        sum += d * d;
    }
    return sqrt(sum);
}

double la_angle(const double* u, const double* v, int n) {
    double d = la_dot(u, v, n);
    double nu = la_norm(u, n);
    double nv = la_norm(v, n);
    if (nu < LA_EPSILON || nv < LA_EPSILON) return 0.0;
    double cos_theta = d / (nu * nv);
    if (cos_theta > 1.0) cos_theta = 1.0;
    if (cos_theta < -1.0) cos_theta = -1.0;
    return acos(cos_theta);
}

int la_are_orthogonal(const double* u, const double* v, int n) {
    return fabs(la_dot(u, v, n)) < LA_EPSILON;
}

void la_cross_product(const double* u, const double* v, double* result) {
    result[0] = u[1] * v[2] - u[2] * v[1];
    result[1] = u[2] * v[0] - u[0] * v[2];
    result[2] = u[0] * v[1] - u[1] * v[0];
}

void la_gram_schmidt(const double* vectors, double* result, int num_vectors, int dim) {
    memset(result, 0, (size_t)dim * num_vectors * sizeof(double));

    for (int k = 0; k < num_vectors; k++) {
        const double* vk = vectors + k * dim;
        double* uk = result + k * dim;
        memcpy(uk, vk, (size_t)dim * sizeof(double));

        for (int j = 0; j < k; j++) {
            double* uj = result + j * dim;
            double d = la_dot(vk, uj, dim);
            double n = la_dot(uj, uj, dim);
            if (n < LA_EPSILON) continue;
            double scale = d / n;
            for (int i = 0; i < dim; i++)
                uk[i] -= scale * uj[i];
        }

        double len = la_norm(uk, dim);
        if (len > LA_EPSILON) {
            for (int i = 0; i < dim; i++)
                uk[i] /= len;
        }
    }
}

void la_orthogonal_projection(const double* v, const double* basis,
                              int num_basis, int dim, double* result) {
    memset(result, 0, (size_t)dim * sizeof(double));
    for (int k = 0; k < num_basis; k++) {
        const double* bk = basis + k * dim;
        double d = la_dot(v, bk, dim);
        double n = la_dot(bk, bk, dim);
        if (n < LA_EPSILON) continue;
        double scale = d / n;
        for (int i = 0; i < dim; i++)
            result[i] += scale * bk[i];
    }
}

int la_least_squares(const LAMatrix* A, const double* b, double* result) {
    LAMatrix* At = la_matrix_transpose(A);
    if (!At) return -1;

    LAMatrix* AtA = la_matrix_mul(At, A);
    if (!AtA) { la_matrix_free(At); return -1; }

    int n = A->cols;
    LAMatrix* b_mat = la_matrix_new(A->rows, 1);
    if (!b_mat) { la_matrix_free(At); la_matrix_free(AtA); return -1; }
    for (int i = 0; i < A->rows; i++)
        b_mat->data[i] = b[i];

    LAMatrix* Atb_mat = la_matrix_mul(At, b_mat);
    if (!Atb_mat) {
        la_matrix_free(At); la_matrix_free(AtA); la_matrix_free(b_mat);
        return -1;
    }

    LAMatrix* aug = la_matrix_new(n, n + 1);
    if (!aug) {
        la_matrix_free(At); la_matrix_free(AtA);
        la_matrix_free(b_mat); la_matrix_free(Atb_mat);
        return -1;
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++)
            aug->data[LA_IDX(i, j, n + 1)] = AtA->data[LA_IDX(i, j, n)];
        aug->data[LA_IDX(i, n, n + 1)] = Atb_mat->data[i];
    }

    int sol_type = la_solve(aug, result);

    la_matrix_free(At);
    la_matrix_free(AtA);
    la_matrix_free(b_mat);
    la_matrix_free(Atb_mat);
    la_matrix_free(aug);

    return sol_type;
}
