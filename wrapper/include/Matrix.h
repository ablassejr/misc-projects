#ifndef MATRIX_H
#define MATRIX_H

#include <iostream>
#include <vector>
#include <stdexcept>

extern "C" {
#include "la_matrix.h"
}

class Matrix {
    LAMatrix* m_;

public:
    Matrix(int rows, int cols);
    Matrix(int rows, int cols, const std::vector<double>& data);
    Matrix(const Matrix& other);
    Matrix& operator=(const Matrix& other);
    ~Matrix();

    /* Access */
    int rows() const;
    int cols() const;
    double& operator()(int i, int j);
    double  operator()(int i, int j) const;
    LAMatrix* raw() const;

    /* Factory */
    static Matrix identity(int n);

    /* I/O */
    friend std::ostream& operator<<(std::ostream& os, const Matrix& mat);
};

#endif /* MATRIX_H */
