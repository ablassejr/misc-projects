#include "la_inner.h"
#include "la_config.h"
#include "la_ops.h"
#include "la_elimination.h"
#include <math.h>
#include <string.h>

double la_dot(const double* u, const double* v, int n) {
    /* TODO: implement */
    return 0.0;
}

double la_norm(const double* v, int n) {
    /* TODO: implement */
    return 0.0;
}

void la_normalize(const double* v, double* result, int n) {
    /* TODO: implement */
}

double la_distance(const double* u, const double* v, int n) {
    /* TODO: implement */
    return 0.0;
}

double la_angle(const double* u, const double* v, int n) {
    /* TODO: implement */
    return 0.0;
}

int la_are_orthogonal(const double* u, const double* v, int n) {
    /* TODO: implement */
    return 0;
}

void la_cross_product(const double* u, const double* v, double* result) {
    /* TODO: implement */
}

void la_gram_schmidt(const double* vectors, double* result, int num_vectors, int dim) {
    /* TODO: implement */
}

void la_orthogonal_projection(const double* v, const double* basis,
                              int num_basis, int dim, double* result) {
    /* TODO: implement */
}

int la_least_squares(const LAMatrix* A, const double* b, double* result) {
    /* TODO: implement */
    return 0;
}
