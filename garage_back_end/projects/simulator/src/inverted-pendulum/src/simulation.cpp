// https://techteach.no/simview_2010/pendulum/pendulum_model.pdf

#include "physics_sim.h"

namespace physics_simulator {
PhysicSimulator::PhysicSimulator(float timestep_s,
                                 integrator::solverType solver_type,
                                 systems::SystemType system_type)
    : timestep_s_(timestep_s), sim_is_over_(false), elapsed_sim_time_s_(0.0) {
  switch (solver_type) {
    case integrator::solverType::EXPLICIT_EULER:
      solver_ptr_ = std::make_unique<integrator::ExplicitEuler>(timestep_s_);
      break;

    default:
      solver_ptr_ = std::make_unique<integrator::ExplicitEuler>(timestep_s_);
      break;
  }
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
}

void PhysicSimulator::simulate(bool realtime, float horizon) {
  sim_is_over_ = false;
  uint32_t total_steps = horizon / timestep_s_;
  uint32_t current_step = 0;
  auto last_step = std::chrono::high_resolution_clock::now();
  while (current_step < total_steps) {
    auto t = std::chrono::high_resolution_clock::now();
    auto duration_since_last_step =
        std::chrono::duration_cast<std::chrono::microseconds>(t - last_step)
            .count();
    if (duration_since_last_step >= (timestep_s_ * 1e6) && realtime ||
        !realtime) {
      guard{mutex_};
      system_ptr_->computeDerivative();
      Vf state = solver_ptr_->step(system_ptr_->getDerivative(),
                                   system_ptr_->getState());
      system_ptr_->setState(state);
      last_step = std::chrono::high_resolution_clock::now();
      current_step += 1;
      elapsed_sim_time_s_ = current_step * timestep_s_;
    }
  }
  sim_is_over_ = true;
}

void physics_simulator::PhysicSimulator::setState(Vf state) {
  guard{mutex_};
  system_ptr_->setState(state);
}

void physics_simulator::PhysicSimulator::setInput(Vf input) {
  guard{mutex_};
  system_ptr_->setInput(input);
}

Vf PhysicSimulator::getState() {
  guard{mutex_};
  return system_ptr_->getState();
}

Vf PhysicSimulator::getInput() {
  guard{mutex_};
  return system_ptr_->getInput();
}

bool PhysicSimulator::isRunning() {
  guard{mutex_};
  return !sim_is_over_;
}

float PhysicSimulator::getTime() {
  guard{mutex_};
  return elapsed_sim_time_s_;
};

}  // namespace physics_simulator