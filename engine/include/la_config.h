#ifndef LA_CONFIG_H
#define LA_CONFIG_H

#define LA_EPSILON 1e-9

/* Row-major indexing: element (i,j) in a matrix with `cols` columns */
#define LA_IDX(i, j, cols) ((i) * (cols) + (j))

#endif /* LA_CONFIG_H */
