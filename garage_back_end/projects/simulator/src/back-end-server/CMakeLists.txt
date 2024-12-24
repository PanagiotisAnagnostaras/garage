cmake_minimum_required(VERSION 3.0)
project(inverted-pendulum)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Source files
set(SOURCES
    main.cpp
)

find_package(PkgConfig)
pkg_check_modules(Pistache REQUIRED IMPORTED_TARGET libpistache)

add_executable(httpserver_run ${SOURCES})
target_include_directories(httpserver_run PRIVATE ${CMAKE_SOURCE_DIR}/src/inverted-pendulum/)
target_link_libraries(httpserver_run PkgConfig::Pistache inverted_pendulum)
