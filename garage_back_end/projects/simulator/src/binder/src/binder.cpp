#include "simulation.h"
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace simulation;

PYBIND11_MODULE(binder, m) {
    py::class_<Simulation>(m, "Simulation")
        .def(py::init<>())
        .def("run", &Simulation::run)
        .def("isRunning", &Simulation::isRunning)
        .def("getTime", &Simulation::getTime)
        .def("getCartPos", &Simulation::getCartPos)
        .def("getCartVel", &Simulation::getCartVel)
        .def("getPendAng", &Simulation::getPendAng)
        .def("getPendVel", &Simulation::getPendVel)
        .def("getInput", &Simulation::getInput)
        .def("applyInput", &Simulation::applyInput);
}