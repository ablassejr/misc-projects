#include <catch2/catch_test_macros.hpp>
#include <catch2/matchers/catch_matchers_floating_point.hpp>
#include "Matrix.h"
#include <cmath>

TEST_CASE("Determinant methods agree", "[ch3]") {
    Matrix A(3, 3, {2,1,1, 4,3,3, 8,7,9});
    REQUIRE_THAT(A.det(), Catch::Matchers::WithinAbs(A.det_cofactor(), 1e-6));
}

TEST_CASE("det(AB) = det(A)*det(B)", "[ch3]") {
    Matrix A(3, 3, {2,1,1, 4,3,3, 8,7,9});
    Matrix B(3, 3, {1,0,2, 0,3,1, 4,0,1});
    double det_AB = (A * B).det();
    double det_A_det_B = A.det() * B.det();
    REQUIRE_THAT(det_AB, Catch::Matchers::WithinAbs(det_A_det_B, 1e-6));
}

TEST_CASE("det(A^T) = det(A)", "[ch3]") {
    Matrix A(3, 3, {2,1,1, 4,3,3, 8,7,9});
    REQUIRE_THAT(A.transpose().det(), Catch::Matchers::WithinAbs(A.det(), 1e-6));
}

TEST_CASE("det(A^-1) = 1/det(A)", "[ch3]") {
    Matrix A(3, 3, {2,1,1, 4,3,3, 8,7,9});
    double det_inv = A.inverse().det();
    REQUIRE_THAT(det_inv, Catch::Matchers::WithinAbs(1.0 / A.det(), 1e-6));
}

TEST_CASE("Singular matrix det = 0", "[ch3]") {
    Matrix A(3, 3, {1,2,3, 4,5,6, 7,8,9});
    REQUIRE_THAT(A.det(), Catch::Matchers::WithinAbs(0.0, 1e-6));
}

TEST_CASE("2x2 determinant", "[ch3]") {
    Matrix A(2, 2, {3, 8, 4, 6});
    REQUIRE_THAT(A.det(), Catch::Matchers::WithinAbs(-14.0, 1e-9));
}

TEST_CASE("Cramer's rule matches solve", "[ch3]") {
    Matrix A(3, 3, {1,1,2, 2,4,-3, 3,6,-5});
    std::vector<double> b = {9, 1, 0};
    std::vector<double> cramer_sol;
    int rc = A.cramers_solve(b, cramer_sol);
    REQUIRE(rc == 0);

    Matrix aug(3, 4, {1,1,2,9, 2,4,-3,1, 3,6,-5,0});
    std::vector<double> gauss_sol;
    aug.solve(gauss_sol);

    for (int i = 0; i < 3; i++)
        REQUIRE_THAT(cramer_sol[i], Catch::Matchers::WithinAbs(gauss_sol[i], 1e-6));
}

TEST_CASE("Adjoint inverse matches Gauss-Jordan inverse", "[ch3]") {
    Matrix A(3, 3, {2,1,1, 4,3,3, 8,7,9});
    Matrix inv_gj = A.inverse();
    Matrix adj = A.adjoint();
    double det = A.det();
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            REQUIRE_THAT(adj(i, j) / det, Catch::Matchers::WithinAbs(inv_gj(i, j), 1e-6));
}
