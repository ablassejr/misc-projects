#include <catch2/catch_test_macros.hpp>
#include <catch2/matchers/catch_matchers_floating_point.hpp>
#include "Matrix.h"

TEST_CASE("Row swap", "[ch1]") {
    Matrix m(2, 2, {1, 2, 3, 4});
    m.swap_rows(0, 1);
    REQUIRE(m(0, 0) == 3.0);
    REQUIRE(m(1, 0) == 1.0);
}

TEST_CASE("Solve unique 3x3", "[ch1]") {
    Matrix aug(3, 4, {1,1,2,9, 2,4,-3,1, 3,6,-5,0});
    std::vector<double> sol;
    int type = aug.solve(sol);
    REQUIRE(type == 0);
    REQUIRE_THAT(sol[0], Catch::Matchers::WithinAbs(1.0, 1e-6));
    REQUIRE_THAT(sol[1], Catch::Matchers::WithinAbs(2.0, 1e-6));
    REQUIRE_THAT(sol[2], Catch::Matchers::WithinAbs(3.0, 1e-6));
}

TEST_CASE("Solve inconsistent", "[ch1]") {
    Matrix aug(3, 4, {1,1,1,2, 0,1,1,1, 0,0,0,3});
    std::vector<double> sol;
    REQUIRE(aug.solve(sol) == -1);
}

TEST_CASE("Solve infinite", "[ch1]") {
    Matrix aug(2, 3, {1,2,3, 2,4,6});
    std::vector<double> sol;
    REQUIRE(aug.solve(sol) == 1);
}

TEST_CASE("RREF", "[ch1]") {
    Matrix m(3, 4, {1,1,2,9, 2,4,-3,1, 3,6,-5,0});
    Matrix r = m.rref();
    REQUIRE_THAT(r(0, 3), Catch::Matchers::WithinAbs(1.0, 1e-6));
    REQUIRE_THAT(r(1, 3), Catch::Matchers::WithinAbs(2.0, 1e-6));
    REQUIRE_THAT(r(2, 3), Catch::Matchers::WithinAbs(3.0, 1e-6));
}
