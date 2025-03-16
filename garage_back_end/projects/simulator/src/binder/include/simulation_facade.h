#include "simulation.h"

namespace simulation_facade {
class SimulationFacade {
 public:
  SimulationFacade() = default;
  ~SimulationFacade() = default;
    void setSystemPoint2D();
    void setSystemInvertedPendulum();
    void simulate(bool realtime, float horizon_s);
    std::vector<double> getState();
    void setState(const std::vector<double> &state);
    void setInput(const std::vector<double> &input);
 private:
  simulation::Simulation simulation_;
};
}  // namespace simulation_facade