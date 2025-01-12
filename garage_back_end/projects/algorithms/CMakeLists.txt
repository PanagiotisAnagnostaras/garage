cmake_minimum_required(VERSION 3.0)
project(algorithms)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Source files
set(SOURCES
    src/main.cpp
    src/data_structures.cpp
    src/p1c1_is_unique.cpp
    src/p1c2_check_permutations.cpp
    src/p1c3_urlfy.cpp
    src/p1c4_palindrome_permutation.cpp
    src/p2c1_remove_dups.cpp
)

add_executable(main ${SOURCES})
target_include_directories(main PRIVATE include)
