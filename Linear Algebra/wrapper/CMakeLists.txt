cmake_minimum_required(VERSION 3.20)
project(linalg_wrapper CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Catch2
find_package(Catch2 3 REQUIRED)

# C engine static library
add_library(linalgcore STATIC IMPORTED)
set_target_properties(linalgcore PROPERTIES
    IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/../engine/build/liblinalgcore.a
    INTERFACE_INCLUDE_DIRECTORIES ${CMAKE_SOURCE_DIR}/../engine/include
)

# C++ wrapper library
add_library(linalg_wrapper src/Matrix.cpp)
target_include_directories(linalg_wrapper PUBLIC include ../engine/include)
target_link_libraries(linalg_wrapper PUBLIC linalgcore)

# Test executable
file(GLOB TEST_SOURCES tests/*.cpp)
add_executable(tests ${TEST_SOURCES})
target_link_libraries(tests PRIVATE linalg_wrapper Catch2::Catch2WithMain)
