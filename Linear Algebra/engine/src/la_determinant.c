#include "la_determinant.h"
#include "la_config.h"
#include "la_elimination.h"
#include <math.h>
#include <string.h>

double la_minor(const LAMatrix* A, int i, int j) {
    /* TODO: implement */
    return 0.0;
}

double la_cofactor(const LAMatrix* A, int i, int j) {
    /* TODO: implement */
    return 0.0;
}

double la_det_cofactor(const LAMatrix* A) {
    /* TODO: implement */
    return 0.0;
}

double la_det_elimination(const LAMatrix* A) {
    /* TODO: implement */
    return 0.0;
}

LAMatrix* la_cofactor_matrix(const LAMatrix* A) {
    /* TODO: implement */
    return NULL;
}

LAMatrix* la_adjoint(const LAMatrix* A) {
    /* TODO: implement */
    return NULL;
}

LAMatrix* la_inverse_adjoint(const LAMatrix* A) {
    /* TODO: implement */
    return NULL;
}

int la_cramers_rule(const LAMatrix* A, const double* b, double* result) {
    /* TODO: implement */
    return 0;
}
