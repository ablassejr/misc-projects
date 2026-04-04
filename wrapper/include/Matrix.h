#ifndef MATRIX_H
#define MATRIX_H

#include <iostream>
#include <vector>
#include <stdexcept>

extern "C" {
#include "la_matrix.h"
#include "la_elimination.h"
#include "la_ops.h"
}

#include <utility>

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

    /* Ch.1: Elimination */
    void swap_rows(int i, int j);
    void scale_row(int i, double scalar);
    void add_scaled_row(int target, int source, double scalar);
    Matrix ref() const;
    Matrix rref() const;
    int solve(std::vector<double>& result) const;

    /* Ch.2: Matrix Operations */
    Matrix operator+(const Matrix& other) const;
    Matrix operator*(const Matrix& other) const;
    Matrix operator*(double scalar) const;
    Matrix transpose() const;
    Matrix inverse() const;
    std::pair<Matrix, Matrix> lu() const;

    /* Factory */
    static Matrix identity(int n);

    /* I/O */
    friend std::ostream& operator<<(std::ostream& os, const Matrix& mat);
};

#endif /* MATRIX_H */
