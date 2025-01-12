cmake_minimum_required(VERSION 3.0)
project(algorithms)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Source files
set(SOURCES
    src/main.cpp
    src/is_unique.cpp
    src/check_permutations.cpp
    src/urlfy.cpp
    src/palindrome_permutation.cpp
)

add_executable(main ${SOURCES})
target_include_directories(main PRIVATE include)
