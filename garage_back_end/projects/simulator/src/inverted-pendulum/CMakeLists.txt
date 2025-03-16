cmake_minimum_required(VERSION 3.0)
project(inverted-pendulum)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Source files
set(SOURCES
    src/integrator.cpp
    src/linear_algebra.cpp
    src/simulation.cpp
    src/systems.cpp
)

set(TESTS
    tests/typesTests.cpp
)

set(Eigen
    /external_repos/eigen)

find_package(Threads REQUIRED) # Finds targets built here
add_library(inverted_pendulum SHARED ${SOURCES})
set_target_properties(inverted_pendulum PROPERTIES POSITION_INDEPENDENT_CODE ON)
target_include_directories(inverted_pendulum PUBLIC include PRIVATE ${Eigen})
target_link_libraries(inverted_pendulum PRIVATE Threads::Threads)
