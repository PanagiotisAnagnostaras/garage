#pragma once

#include <chrono>
#include <cmath>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
#include <mutex>

#include "integrator.h"
#include "systems.h"
#include "types.h"

namespace simulation {

class Simulation {
 public:
  Simulation(float timestep_s = 1e-3,
             integrator::solverType solver_type =
                 integrator::solverType::EXPLICIT_EULER,
             systems::SystemType system_type = systems::SystemType::POINT_2D);
  void simulate(bool realtime, float horizon_s);
  void setState(Vf state);
  void setInput(Vf input);
  Vf getState();
  Vf getInput();
  bool isRunning();
  float getTime();
  void setSystemType(systems::SystemType system_type);
  void setSolverType(integrator::solverType solver_type);

 private:
  bool sim_is_over_;
  float timestep_s_, elapsed_sim_time_s_;
  std::unique_ptr<systems::SystemsBase> system_ptr_;
  std::unique_ptr<integrator::I_NumericalIntegrator> solver_ptr_;
  std::mutex mutex_;
};
}  // namespace simulation