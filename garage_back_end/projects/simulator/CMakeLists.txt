cmake_minimum_required(VERSION 3.0)
project(App)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(external/pybind11/include)
add_subdirectory(external/pybind11)
add_subdirectory(src/simulator_core)
add_subdirectory(src/binder)
