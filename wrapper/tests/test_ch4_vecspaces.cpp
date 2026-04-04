#include <catch2/catch_test_macros.hpp>
#include <catch2/matchers/catch_matchers_floating_point.hpp>
#include "Matrix.h"
#include <cmath>

TEST_CASE("Rank of full rank matrix", "[ch4]") {
    Matrix A(3, 3, {1,0,0, 0,1,0, 0,0,1});
    REQUIRE(A.rank() == 3);
}

TEST_CASE("Rank of rank-deficient matrix", "[ch4]") {
    Matrix A(3, 3, {1,2,3, 4,5,6, 7,8,9});
    REQUIRE(A.rank() == 2);
}

TEST_CASE("Rank-nullity theorem", "[ch4]") {
    Matrix A(3, 4, {1,2,0,1, 0,0,1,1, 1,2,1,2});
    REQUIRE(A.rank() + A.nullity() == A.cols());
}

TEST_CASE("Null space Ax=0", "[ch4]") {
    Matrix A(3, 4, {1,2,0,1, 0,0,1,1, 1,2,1,2});
    Matrix ns = A.null_space();
    REQUIRE(ns.cols() == A.nullity());
    for (int c = 0; c < ns.cols(); c++) {
        Matrix v(ns.rows(), 1);
        for (int r = 0; r < ns.rows(); r++) v(r, 0) = ns(r, c);
        Matrix Av = A * v;
        for (int r = 0; r < Av.rows(); r++)
            REQUIRE_THAT(Av(r, 0), Catch::Matchers::WithinAbs(0.0, 1e-6));
    }
}

TEST_CASE("Column space dimension = rank", "[ch4]") {
    Matrix A(3, 4, {1,2,0,1, 0,0,1,1, 1,2,1,2});
    Matrix cs = A.column_space();
    REQUIRE(cs.cols() == A.rank());
}

TEST_CASE("Row space dimension = rank", "[ch4]") {
    Matrix A(3, 4, {1,2,0,1, 0,0,1,1, 1,2,1,2});
    Matrix rs = A.row_space();
    REQUIRE(rs.rows() == A.rank());
}

TEST_CASE("Independence check", "[ch4]") {
    double indep[] = {1,0,0, 0,1,0, 0,0,1};
    REQUIRE(la_is_independent(indep, 3, 3) == 1);

    double dep[] = {1,2,3, 4,5,6, 5,7,9};
    REQUIRE(la_is_independent(dep, 3, 3) == 0);
}

TEST_CASE("Span membership", "[ch4]") {
    double basis[] = {1,0,0, 0,1,0};
    double in_span[] = {3, 5, 0};
    double not_in_span[] = {1, 1, 1};
    REQUIRE(la_is_in_span(in_span, basis, 2, 3) == 1);
    REQUIRE(la_is_in_span(not_in_span, basis, 2, 3) == 0);
}

TEST_CASE("Change of basis", "[ch4]") {
    Matrix std_basis(2, 2, {1,0, 0,1});
    Matrix new_basis(2, 2, {1,1, 0,1});
    LAMatrix* P = la_change_of_basis(std_basis.raw(), new_basis.raw());
    REQUIRE(P != nullptr);

    double v_std[] = {3, 2};
    Matrix v(2, 1, {3, 2});
    Matrix Pm(P->rows, P->cols);
    for (int i = 0; i < P->rows; i++)
        for (int j = 0; j < P->cols; j++)
            Pm(i, j) = la_matrix_get(P, i, j);
    Matrix v_new = Pm * v;
    REQUIRE_THAT(v_new(0, 0), Catch::Matchers::WithinAbs(1.0, 1e-6));
    REQUIRE_THAT(v_new(1, 0), Catch::Matchers::WithinAbs(2.0, 1e-6));
    la_matrix_free(P);
}
