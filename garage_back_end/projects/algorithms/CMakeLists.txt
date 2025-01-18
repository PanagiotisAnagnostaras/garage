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
    src/p2c2_k_to_last.cpp
    src/p2c3_delete_middle_node.cpp
    src/p2c4_partition.cpp
    src/p8c1_triple_step.cpp
    src/p8c2_robot_in_grid.cpp
    src/p8c3_magic_index.cpp
    src/p8c5_recursive_multiply.cpp
    )

add_executable(main ${SOURCES})
target_include_directories(main PRIVATE include)
