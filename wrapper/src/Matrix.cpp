#include "Matrix.h"

Matrix::Matrix(int rows, int cols) : m_(la_matrix_new(rows, cols)) {
    if (!m_) throw std::runtime_error("Allocation failed");
}

Matrix::Matrix(int rows, int cols, const std::vector<double>& data) {
    if ((int)data.size() != rows * cols)
        throw std::invalid_argument("Data size mismatch");
    m_ = la_matrix_from_array(rows, cols, data.data());
    if (!m_) throw std::runtime_error("Allocation failed");
}

Matrix::Matrix(const Matrix& other) : m_(la_matrix_copy(other.m_)) {
    if (!m_) throw std::runtime_error("Copy failed");
}

Matrix& Matrix::operator=(const Matrix& other) {
    if (this != &other) {
        la_matrix_free(m_);
        m_ = la_matrix_copy(other.m_);
        if (!m_) throw std::runtime_error("Copy failed");
    }
    return *this;
}

Matrix::~Matrix() { la_matrix_free(m_); }

int Matrix::rows() const { return la_matrix_rows(m_); }
int Matrix::cols() const { return la_matrix_cols(m_); }

double& Matrix::operator()(int i, int j) {
    return m_->data[i * m_->cols + j];
}

double Matrix::operator()(int i, int j) const {
    return la_matrix_get(m_, i, j);
}

LAMatrix* Matrix::raw() const { return m_; }

Matrix Matrix::identity(int n) {
    Matrix m(n, n);
    for (int i = 0; i < n; i++) m(i, i) = 1.0;
    return m;
}

std::ostream& operator<<(std::ostream& os, const Matrix& mat) {
    for (int i = 0; i < mat.rows(); i++) {
        os << "  [";
        for (int j = 0; j < mat.cols(); j++) {
            char buf[16];
            snprintf(buf, sizeof(buf), "%8.4f", mat(i, j));
            os << buf;
            if (j < mat.cols() - 1) os << ", ";
        }
        os << "]\n";
    }
    return os;
}
