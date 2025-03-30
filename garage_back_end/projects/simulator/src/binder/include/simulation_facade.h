#include "simulation.h"

namespace simulation_facade {
class SimulationFacade {
 public:
  SimulationFacade() = default;
  ~SimulationFacade() = default;
  void setSystemPoint2D();
  void setSystemInvertedPendulum();
  void simulate(bool realtime, float horizon_s);
  std::vector<float> getState();
  std::vector<float> getInput();
  void setState(const std::vector<float> &state);
  void setInput(const std::vector<float> &input);
  float getTime();

 private:
  simulation::Simulation simulation_;
};
}  // namespace simulation_facade