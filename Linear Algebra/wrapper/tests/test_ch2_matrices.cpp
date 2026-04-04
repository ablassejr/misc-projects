#include <catch2/catch_test_macros.hpp>
#include <catch2/matchers/catch_matchers_floating_point.hpp>
#include "Matrix.h"

TEST_CASE("Matrix addition", "[ch2]") {
    Matrix A(2, 2, {1, 2, 3, 4});
    Matrix B(2, 2, {5, 6, 7, 8});
    Matrix C = A + B;
    REQUIRE(C(0, 0) == 6.0);
    REQUIRE(C(1, 1) == 12.0);
}

TEST_CASE("Scalar multiplication", "[ch2]") {
    Matrix A(2, 2, {1, 2, 3, 4});
    Matrix B = A * 3.0;
    REQUIRE(B(0, 0) == 3.0);
    REQUIRE(B(1, 1) == 12.0);
}

TEST_CASE("Matrix multiplication", "[ch2]") {
    Matrix A(2, 3, {1,2,3, 4,5,6});
    Matrix B(3, 2, {7,8, 9,10, 11,12});
    Matrix C = A * B;
    REQUIRE(C.rows() == 2);
    REQUIRE(C.cols() == 2);
    REQUIRE_THAT(C(0, 0), Catch::Matchers::WithinAbs(58.0, 1e-9));
    REQUIRE_THAT(C(0, 1), Catch::Matchers::WithinAbs(64.0, 1e-9));
    REQUIRE_THAT(C(1, 0), Catch::Matchers::WithinAbs(139.0, 1e-9));
    REQUIRE_THAT(C(1, 1), Catch::Matchers::WithinAbs(154.0, 1e-9));
}

TEST_CASE("Matrix multiplication non-commutativity", "[ch2]") {
    Matrix A(2, 2, {1, 2, 3, 4});
    Matrix B(2, 2, {5, 6, 7, 8});
    Matrix AB = A * B;
    Matrix BA = B * A;
    bool same = true;
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            if (std::abs(AB(i, j) - BA(i, j)) > 1e-9) same = false;
    REQUIRE_FALSE(same);
}

TEST_CASE("Transpose", "[ch2]") {
    Matrix A(2, 3, {1,2,3, 4,5,6});
    Matrix T = A.transpose();
    REQUIRE(T.rows() == 3);
    REQUIRE(T.cols() == 2);
    REQUIRE(T(0, 0) == 1.0);
    REQUIRE(T(0, 1) == 4.0);
    REQUIRE(T(2, 0) == 3.0);
}

TEST_CASE("(AB)^T = B^T A^T", "[ch2]") {
    Matrix A(2, 3, {1,2,3, 4,5,6});
    Matrix B(3, 2, {7,8, 9,10, 11,12});
    Matrix AB_T = (A * B).transpose();
    Matrix BT_AT = B.transpose() * A.transpose();
    for (int i = 0; i < AB_T.rows(); i++)
        for (int j = 0; j < AB_T.cols(); j++)
            REQUIRE_THAT(AB_T(i, j), Catch::Matchers::WithinAbs(BT_AT(i, j), 1e-9));
}

TEST_CASE("Inverse round-trip", "[ch2]") {
    Matrix A(3, 3, {2,1,1, 4,3,3, 8,7,9});
    Matrix Ainv = A.inverse();
    Matrix I = A * Ainv;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++) {
            double expected = (i == j) ? 1.0 : 0.0;
            REQUIRE_THAT(I(i, j), Catch::Matchers::WithinAbs(expected, 1e-6));
        }
}

TEST_CASE("Singular matrix inverse throws", "[ch2]") {
    Matrix A(2, 2, {1, 2, 2, 4});
    REQUIRE_THROWS(A.inverse());
}

TEST_CASE("LU factorization LU = A", "[ch2]") {
    Matrix A(3, 3, {2,1,1, 4,3,3, 8,7,9});
    auto [L, U] = A.lu();
    Matrix LU = L * U;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            REQUIRE_THAT(LU(i, j), Catch::Matchers::WithinAbs(A(i, j), 1e-9));
}
