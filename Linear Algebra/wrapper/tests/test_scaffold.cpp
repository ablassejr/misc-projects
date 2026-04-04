#include <catch2/catch_test_macros.hpp>
#include "Matrix.h"

TEST_CASE("Matrix allocation and access", "[matrix]") {
    Matrix m(2, 3);
    REQUIRE(m.rows() == 2);
    REQUIRE(m.cols() == 3);
    m(0, 0) = 5.0;
    REQUIRE(m(0, 0) == 5.0);
}

TEST_CASE("Matrix identity", "[matrix]") {
    Matrix I = Matrix::identity(3);
    REQUIRE(I(0, 0) == 1.0);
    REQUIRE(I(1, 1) == 1.0);
    REQUIRE(I(0, 1) == 0.0);
}

TEST_CASE("Matrix copy", "[matrix]") {
    Matrix a(2, 2, {1, 2, 3, 4});
    Matrix b = a;
    REQUIRE(b(0, 0) == 1.0);
    b(0, 0) = 99.0;
    REQUIRE(a(0, 0) == 1.0);  /* deep copy */
}
