#include "simulation_facade.h"

namespace simulation_facade {
void SimulationFacade::setSystemPoint2D() {
  simulation_.setSystemType(systems::POINT_2D);
};

void SimulationFacade::setSystemInvertedPendulum() {
  simulation_.setSystemType(systems::INVERTED_PENDULUM);
};

void SimulationFacade::simulate(bool realtime, float horizon_s) {
  simulation_.simulate(realtime, horizon_s);
};

std::vector<float> SimulationFacade::getState() {
  return simulation_.getState().getInternalVector();
};

std::vector<float> SimulationFacade::getInput() {
  return simulation_.getInput().getInternalVector();
};

void SimulationFacade::setState(const std::vector<float> &state) {
  Vf stateVf;
  for (float el : state) {
    stateVf.push_back(el);
  }
  simulation_.setState(stateVf);
};

void SimulationFacade::setInput(const std::vector<float> &input) {
  Vf inputVf;
  for (float el : input) {
    inputVf.push_back(el);
  }
  simulation_.setInput(inputVf);
};

float SimulationFacade::getTime() { return simulation_.getTime(); }
}  // namespace simulation_facade