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

void Matrix::swap_rows(int i, int j) { la_swap_rows(m_, i, j); }
void Matrix::scale_row(int i, double scalar) { la_scale_row(m_, i, scalar); }
void Matrix::add_scaled_row(int target, int source, double scalar) {
    la_add_scaled_row(m_, target, source, scalar);
}

Matrix Matrix::ref() const {
    Matrix copy(*this);
    la_to_ref(copy.m_);
    return copy;
}

Matrix Matrix::rref() const {
    Matrix copy(*this);
    la_to_rref(copy.m_);
    return copy;
}

int Matrix::solve(std::vector<double>& result) const {
    int n_vars = m_->cols - 1;
    result.resize(n_vars, 0.0);
    return la_solve(m_, result.data());
}

Matrix Matrix::operator+(const Matrix& other) const {
    LAMatrix* r = la_matrix_add(m_, other.m_);
    if (!r) throw std::runtime_error("Addition failed (dimension mismatch?)");
    Matrix res(r->rows, r->cols);
    la_matrix_free(res.m_);
    res.m_ = r;
    return res;
}

Matrix Matrix::operator*(const Matrix& other) const {
    LAMatrix* r = la_matrix_mul(m_, other.m_);
    if (!r) throw std::runtime_error("Multiplication failed (dimension mismatch?)");
    Matrix res(r->rows, r->cols);
    la_matrix_free(res.m_);
    res.m_ = r;
    return res;
}

Matrix Matrix::operator*(double scalar) const {
    LAMatrix* r = la_matrix_scalar_mul(m_, scalar);
    if (!r) throw std::runtime_error("Scalar multiply failed");
    Matrix res(r->rows, r->cols);
    la_matrix_free(res.m_);
    res.m_ = r;
    return res;
}

Matrix Matrix::transpose() const {
    LAMatrix* r = la_matrix_transpose(m_);
    if (!r) throw std::runtime_error("Transpose failed");
    Matrix res(r->rows, r->cols);
    la_matrix_free(res.m_);
    res.m_ = r;
    return res;
}

Matrix Matrix::inverse() const {
    LAMatrix* r = la_matrix_inverse(m_);
    if (!r) throw std::runtime_error("Matrix is singular");
    Matrix res(r->rows, r->cols);
    la_matrix_free(res.m_);
    res.m_ = r;
    return res;
}

std::pair<Matrix, Matrix> Matrix::lu() const {
    LAMatrix *L = nullptr, *U = nullptr;
    int rc = la_lu_factorize(m_, &L, &U);
    if (rc != 0) throw std::runtime_error("LU factorization failed (zero pivot)");
    Matrix Lm(L->rows, L->cols);
    la_matrix_free(Lm.m_);
    Lm.m_ = L;
    Matrix Um(U->rows, U->cols);
    la_matrix_free(Um.m_);
    Um.m_ = U;
    return {Lm, Um};
}

double Matrix::det() const { return la_det_elimination(m_); }
double Matrix::det_cofactor() const { return la_det_cofactor(m_); }

Matrix Matrix::adjoint() const {
    LAMatrix* r = la_adjoint(m_);
    if (!r) throw std::runtime_error("Adjoint failed");
    Matrix res(r->rows, r->cols);
    la_matrix_free(res.m_);
    res.m_ = r;
    return res;
}

int Matrix::cramers_solve(const std::vector<double>& b, std::vector<double>& result) const {
    result.resize(m_->rows, 0.0);
    return la_cramers_rule(m_, b.data(), result.data());
}

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
