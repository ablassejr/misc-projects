#include "la_elimination.h"
#include "la_config.h"
#include <math.h>
#include <string.h>

void la_swap_rows(LAMatrix* mat, int i, int j) {
    /* TODO: implement */
}

void la_scale_row(LAMatrix* mat, int i, double scalar) {
    /* TODO: implement */
}

void la_add_scaled_row(LAMatrix* mat, int target, int source, double scalar) {
    /* TODO: implement */
}

int la_find_pivot(const LAMatrix* mat, int col, int start_row) {
    /* TODO: implement */
    return 0;
}

int la_to_ref(LAMatrix* mat) {
    /* TODO: implement */
    return 0;
}

int la_to_rref(LAMatrix* mat) {
    /* TODO: implement */
    return 0;
}

int la_solve(const LAMatrix* augmented, double* result) {
    /* TODO: implement */
    return 0;
}
