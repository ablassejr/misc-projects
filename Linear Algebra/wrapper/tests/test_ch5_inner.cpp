#include <catch2/catch_test_macros.hpp>
#include <catch2/matchers/catch_matchers_floating_point.hpp>
#include "Matrix.h"
#include <cmath>

extern "C" {
#include "la_inner.h"
}

TEST_CASE("Dot product", "[ch5]") {
    double u[] = {1, 2, 3};
    double v[] = {4, 5, 6};
    REQUIRE_THAT(la_dot(u, v, 3), Catch::Matchers::WithinAbs(32.0, 1e-9));
}

TEST_CASE("Norm", "[ch5]") {
    double v[] = {3, 4};
    REQUIRE_THAT(la_norm(v, 2), Catch::Matchers::WithinAbs(5.0, 1e-9));
}

TEST_CASE("Cauchy-Schwarz inequality", "[ch5]") {
    double u[] = {1, 2, 3};
    double v[] = {4, -1, 2};
    double lhs = std::abs(la_dot(u, v, 3));
    double rhs = la_norm(u, 3) * la_norm(v, 3);
    REQUIRE(lhs <= rhs + 1e-9);
}

TEST_CASE("Triangle inequality", "[ch5]") {
    double u[] = {1, 2, 3};
    double v[] = {4, -1, 2};
    double w[3];
    for (int i = 0; i < 3; i++) w[i] = u[i] + v[i];
    double lhs = la_norm(w, 3);
    double rhs = la_norm(u, 3) + la_norm(v, 3);
    REQUIRE(lhs <= rhs + 1e-9);
}

TEST_CASE("Normalize", "[ch5]") {
    double v[] = {3, 4};
    double result[2];
    la_normalize(v, result, 2);
    REQUIRE_THAT(la_norm(result, 2), Catch::Matchers::WithinAbs(1.0, 1e-9));
}

TEST_CASE("Cross product", "[ch5]") {
    double u[] = {1, 0, 0};
    double v[] = {0, 1, 0};
    double result[3];
    la_cross_product(u, v, result);
    REQUIRE_THAT(result[0], Catch::Matchers::WithinAbs(0.0, 1e-9));
    REQUIRE_THAT(result[1], Catch::Matchers::WithinAbs(0.0, 1e-9));
    REQUIRE_THAT(result[2], Catch::Matchers::WithinAbs(1.0, 1e-9));
}

TEST_CASE("Orthogonality check", "[ch5]") {
    double u[] = {1, 0, 0};
    double v[] = {0, 1, 0};
    REQUIRE(la_are_orthogonal(u, v, 3) == 1);
    double w[] = {1, 1, 0};
    REQUIRE(la_are_orthogonal(u, w, 3) == 0);
}

TEST_CASE("Gram-Schmidt produces orthonormal set", "[ch5]") {
    double vecs[] = {1, 1, 0,   1, 0, 1,   0, 1, 1};  /* 3 vectors, dim 3 */
    double result[9];
    la_gram_schmidt(vecs, result, 3, 3);

    for (int i = 0; i < 3; i++)
        REQUIRE_THAT(la_norm(result + i * 3, 3),
                     Catch::Matchers::WithinAbs(1.0, 1e-6));

    for (int i = 0; i < 3; i++)
        for (int j = i + 1; j < 3; j++)
            REQUIRE_THAT(la_dot(result + i * 3, result + j * 3, 3),
                         Catch::Matchers::WithinAbs(0.0, 1e-6));
}

TEST_CASE("Least squares residual orthogonality", "[ch5]") {
    Matrix A(4, 2, {1,1, 1,2, 1,3, 1,4});
    double b[] = {1, 2, 1.5, 3.5};
    double x[2];
    int rc = la_least_squares(A.raw(), b, x);
    REQUIRE(rc == 0);

    double residual[4];
    for (int i = 0; i < 4; i++) {
        residual[i] = b[i];
        for (int j = 0; j < 2; j++)
            residual[i] -= la_matrix_get(A.raw(), i, j) * x[j];
    }

    for (int j = 0; j < 2; j++) {
        double dot = 0.0;
        for (int i = 0; i < 4; i++)
            dot += la_matrix_get(A.raw(), i, j) * residual[i];
        REQUIRE_THAT(dot, Catch::Matchers::WithinAbs(0.0, 1e-6));
    }
}

TEST_CASE("Angle between vectors", "[ch5]") {
    double u[] = {1, 0};
    double v[] = {0, 1};
    REQUIRE_THAT(la_angle(u, v, 2),
                 Catch::Matchers::WithinAbs(M_PI / 2.0, 1e-9));

    double w[] = {1, 1};
    REQUIRE_THAT(la_angle(u, w, 2),
                 Catch::Matchers::WithinAbs(M_PI / 4.0, 1e-9));
}
