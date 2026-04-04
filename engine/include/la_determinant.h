#ifndef LA_DETERMINANT_H
#define LA_DETERMINANT_H

#include "la_matrix.h"

double    la_det_cofactor(const LAMatrix* A);
double    la_det_elimination(const LAMatrix* A);
double    la_minor(const LAMatrix* A, int i, int j);
double    la_cofactor(const LAMatrix* A, int i, int j);
LAMatrix* la_cofactor_matrix(const LAMatrix* A);
LAMatrix* la_adjoint(const LAMatrix* A);
LAMatrix* la_inverse_adjoint(const LAMatrix* A);
int       la_cramers_rule(const LAMatrix* A, const double* b, double* result);

#endif /* LA_DETERMINANT_H */
