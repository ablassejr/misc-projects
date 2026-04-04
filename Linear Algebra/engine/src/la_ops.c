#include "la_ops.h"
#include "la_config.h"
#include "la_elimination.h"
#include <math.h>
#include <string.h>

LAMatrix* la_matrix_add(const LAMatrix* A, const LAMatrix* B) {
    /* TODO: implement */
    return NULL;
}

LAMatrix* la_matrix_scalar_mul(const LAMatrix* A, double scalar) {
    /* TODO: implement */
    return NULL;
}

LAMatrix* la_matrix_mul(const LAMatrix* A, const LAMatrix* B) {
    /* TODO: implement */
    return NULL;
}

LAMatrix* la_matrix_mul_ikj(const LAMatrix* A, const LAMatrix* B) {
    /* TODO: implement */
    return NULL;
}

LAMatrix* la_matrix_transpose(const LAMatrix* A) {
    /* TODO: implement */
    return NULL;
}

LAMatrix* la_matrix_inverse(const LAMatrix* A) {
    /* TODO: implement */
    return NULL;
}

int la_lu_factorize(const LAMatrix* A, LAMatrix** L, LAMatrix** U) {
    /* TODO: implement */
    return 0;
}

void la_forward_sub(const LAMatrix* L, const double* b, double* y, int n) {
    /* TODO: implement */
}

void la_back_sub(const LAMatrix* U, const double* y, double* x, int n) {
    /* TODO: implement */
}

LAMatrix* la_elementary_swap(int n, int i, int j) {
    /* TODO: implement */
    return NULL;
}

LAMatrix* la_elementary_scale(int n, int i, double c) {
    /* TODO: implement */
    return NULL;
}

LAMatrix* la_elementary_add(int n, int target, int source, double c) {
    /* TODO: implement */
    return NULL;
}
