#include "simulation_facade.h"

namespace simulation_facade {
void SimulationFacade::setSystemPoint2D() {};
void SimulationFacade::setSystemInvertedPendulum() {};
void SimulationFacade::simulate(bool realtime, float horizon_s) {};
std::vector<double> SimulationFacade::getState() {};
void SimulationFacade::setState(const std::vector<double> &state) {};
void SimulationFacade::setInput(const std::vector<double> &input) {};
}  // namespace simulation_facade