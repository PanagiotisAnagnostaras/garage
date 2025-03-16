cmake_minimum_required(VERSION 3.0)
project(binder)

pybind11_add_module(binder src/binder.cpp src/simulation_facade.cpp)
target_link_libraries(binder PRIVATE inverted_pendulum)
target_include_directories(binder PRIVATE include ${CMAKE_SOURCE_DIR}/src/inverted-pendulum/include)
