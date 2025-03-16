#include "simulation_facade.h"
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace simulation_facade;

PYBIND11_MODULE(binder, m) {
    py::class_<SimulationFacade>(m, "SimulationFacade")
        .def(py::init<>())
        .def("setSystemPoint2D", &SimulationFacade::setSystemPoint2D)
        .def("setSystemInvertedPendulum", &SimulationFacade::setSystemInvertedPendulum)
        .def("simulate", &SimulationFacade::simulate)
        .def("getState", &SimulationFacade::getState)
        .def("setState", &SimulationFacade::setState)
        .def("setInput", &SimulationFacade::setInput)
        .def("getTime", &SimulationFacade::getTime);
}