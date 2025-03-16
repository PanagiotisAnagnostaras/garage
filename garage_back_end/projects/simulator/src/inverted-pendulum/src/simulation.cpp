// https://techteach.no/simview_2010/pendulum/pendulum_model.pdf

#include "simulation.h"

namespace simulation {
Simulation::Simulation(float timestep_s, integrator::solverType solver_type,
                       systems::SystemType system_type)
    : timestep_s_(timestep_s), sim_is_over_(false), elapsed_sim_time_s_(0.0) {
  setSystemType(systems::POINT_2D);
  setSolverType(integrator::EXPLICIT_EULER);
}

void Simulation::simulate(bool realtime, float horizon) {
  std::cout << "before Simulation::simulate" << std::endl;
  sim_is_over_ = false;
  uint32_t total_steps = horizon / timestep_s_;
  uint32_t current_step = 0;
  auto last_step = std::chrono::high_resolution_clock::now();
  while (current_step < total_steps) {
    std::cout << "current_step = " << current_step << "/" << total_steps
              << std::endl;
    auto t = std::chrono::high_resolution_clock::now();
    auto duration_since_last_step =
        std::chrono::duration_cast<std::chrono::microseconds>(t - last_step)
            .count();
    if (duration_since_last_step >= (timestep_s_ * 1e6) && realtime ||
        !realtime) {
      guard{mutex_};
      std::cout << "1" << std::endl;
      std::cout << system_ptr_->getName() << std::endl;
      system_ptr_->computeDerivative();
      std::cout << "2" << std::endl;
      Vf state = solver_ptr_->step(system_ptr_->getDerivative(),
                                   system_ptr_->getState());
      system_ptr_->setState(state);
      std::cout << "3" << std::endl;
      last_step = std::chrono::high_resolution_clock::now();
      current_step += 1;
      elapsed_sim_time_s_ = current_step * timestep_s_;
    }
  }
  sim_is_over_ = true;
  std::cout << "after Simulation::simulate" << std::endl;
}

void simulation::Simulation::setState(Vf state) {
  guard{mutex_};
  system_ptr_->setState(state);
}

void simulation::Simulation::setInput(Vf input) {
  guard{mutex_};
  system_ptr_->setInput(input);
}

Vf Simulation::getState() {
  guard{mutex_};
  return system_ptr_->getState();
}

Vf Simulation::getInput() {
  guard{mutex_};
  return system_ptr_->getInput();
}

bool Simulation::isRunning() {
  guard{mutex_};
  return !sim_is_over_;
}

float Simulation::getTime() {
  guard{mutex_};
  return elapsed_sim_time_s_;
};

void Simulation::setSystemType(systems::SystemType system_type) {
  switch (system_type) {
    case systems::SystemType::POINT_2D:
      system_ptr_ = std::make_unique<systems::Point2D>();
      break;
    case systems::SystemType::INVERTED_PENDULUM:
      system_ptr_ = std::make_unique<systems::InvertedPendulum>();
      break;
    default:
      system_ptr_ = std::make_unique<systems::Point2D>();
      break;
  }
  std::cout << "Set system: " << system_ptr_->getName() << std::endl;

  auto state = system_ptr_->getState().getInternalVector();
  auto input = system_ptr_->getInput().getInternalVector();
  std::cout << "States: " << std::endl;
  for (auto i : state) {
    std::cout << i << std::endl;
  }
  std::cout << "Inputs: " << std::endl;
  for (auto i : input) {
    std::cout << i << std::endl;
  }
};

void Simulation::setSolverType(integrator::solverType solver_type) {
  switch (solver_type) {
    case integrator::solverType::EXPLICIT_EULER:
      solver_ptr_ = std::make_unique<integrator::ExplicitEuler>(timestep_s_);
      break;

    default:
      solver_ptr_ = std::make_unique<integrator::ExplicitEuler>(timestep_s_);
      break;
  }
}

}  // namespace simulation