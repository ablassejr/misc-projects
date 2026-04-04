#include "la_vecspace.h"
#include "la_config.h"
#include "la_elimination.h"
#include "la_ops.h"
#include <math.h>
#include <string.h>

int la_rank(const LAMatrix* A) {
    /* TODO: implement */
    return 0;
}

int la_nullity(const LAMatrix* A) {
    /* TODO: implement */
    return 0;
}

int la_null_space(const LAMatrix* A, LAMatrix** basis) {
    /* TODO: implement */
    return 0;
}

int la_column_space(const LAMatrix* A, LAMatrix** basis) {
    /* TODO: implement */
    return 0;
}

int la_row_space(const LAMatrix* A, LAMatrix** basis) {
    /* TODO: implement */
    return 0;
}

int la_is_independent(const double* vectors, int num_vectors, int dim) {
    /* TODO: implement */
    return 0;
}

int la_is_in_span(const double* v, const double* vectors, int num_vectors, int dim) {
    /* TODO: implement */
    return 0;
}

LAMatrix* la_change_of_basis(const LAMatrix* old_basis, const LAMatrix* new_basis) {
    /* TODO: implement */
    return NULL;
}
