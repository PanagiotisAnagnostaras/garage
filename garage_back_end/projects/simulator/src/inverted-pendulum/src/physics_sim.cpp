// https://techteach.no/simview_2010/pendulum/pendulum_model.pdf

#include "physics_sim.h"

namespace physics_simulator {
PhysicSimulator::PhysicSimulator(float timestep_s, solver_type solver,
                                 controller::PID pid)
    : timestep_s_(timestep_s), solver_(solver), pid_(pid), sim_is_over_{false} {
  solver_ptr_ = std::make_shared<integrator::ExplicitEuler>(timestep_s);
  number_of_steps_ = horizon_s_ / timestep_s_;
  initializeStates();
}

void PhysicSimulator::simulate(bool realtime) {
  uint32_t total_steps = horizon_s_ / timestep_s_;
  uint32_t current_step = 0;
  auto last_step = std::chrono::high_resolution_clock::now();
  while (current_step < total_steps) {
    auto t = std::chrono::high_resolution_clock::now();
    auto duration_since_last_step =
        std::chrono::duration_cast<std::chrono::microseconds>(t - last_step)
            .count();
    if (duration_since_last_step >= (timestep_s_ * 1e6) && realtime ||
        !realtime) {
      input_mutex_.lock();
      step();
      updateBuffers();
      time_buffer_.push_back(elapsed_time_ms_ / 1e6);
      last_step = std::chrono::high_resolution_clock::now();
      current_step += 1;
      input_mutex_.unlock();
    }
  }
  sim_is_over_ = true;
}

void PhysicSimulator::run_controller() {
  auto last_input = std::chrono::high_resolution_clock::now();
  while (true) {
    auto t = std::chrono::high_resolution_clock::now();
    auto duration_since_last_input =
        std::chrono::duration_cast<std::chrono::microseconds>(t - last_input)
            .count();
    if (duration_since_last_input >= pid_.get_sampling_period_microsec()) {
      input_mutex_.lock();
      input_ = pid_.compute_input(state_[0]);
      last_input = std::chrono::high_resolution_clock::now();
      input_mutex_.unlock();
    }
    if (sim_is_over_) {
      break;
    }
  }
}

void physics_simulator::PhysicSimulator::initializeStates() {
  for (int i = 0; i < 4; i++) {
    f_.push_back(0);
    state_.push_back(0);
  }
  setCartPos(0);
  setCartVel(0);
  setPendAng(1);
  setPendVel(0);
  input_ = 0;
  mass_cart_ = 1;
  mass_pendulum_ = 1;
  length_ = 1;
  g_ = 9.81;
  inertia_ = mass_pendulum_ * pow(length_, 2) / 12;
}

void PhysicSimulator::step() {
  computeDynamics();
  state_ = solver_ptr_->step(f_, state_);
}

void PhysicSimulator::updateBuffers() {
  cart_pos_buffer_.push_back(state_[0]);
  cart_vel_buffer_.push_back(state_[1]);
  pend_ang_buffer_.push_back(state_[2]);
  pend_vel_buffer_.push_back(state_[3]);
  input_buffer_.push_back(input_);
}

Vf PhysicSimulator::getState() { return state_; }

float PhysicSimulator::getInput() { return input_; }

void PhysicSimulator::applyInput(float v) { input_ = v; }

void PhysicSimulator::setState(Vf state) { state_ = state; }

void PhysicSimulator::setCartPos(float v) { state_[0] = v; };

void PhysicSimulator::setCartVel(float v) { state_[1] = v; };

void PhysicSimulator::setPendAng(float v) { state_[2] = v; };

void PhysicSimulator::setPendVel(float v) { state_[3] = v; };

float PhysicSimulator::getCartPos() { return state_.at(0); };

float PhysicSimulator::getCartVel() { return state_.at(1); };

float PhysicSimulator::getPendAng() { return state_.at(2); };

float PhysicSimulator::getPendVel() { return state_.at(3); };

float PhysicSimulator::getTime() { return elapsed_time_ms_ / 1e6; };

void PhysicSimulator::computeDynamics() {
  f_[0] = state_[1];
  f_[1] = (-pow(mass_pendulum_, 2) * pow(length_, 2) * g_ * cos(state_[2]) *
               sin(state_[2]) +
           (input_ +
            mass_pendulum_ * length_ * pow(state_[3], 2) * sin(state_[2])) *
               (inertia_ + mass_pendulum_ * pow(length_, 2))) /
          ((inertia_ + mass_pendulum_ * pow(length_, 2)) *
               (mass_cart_ + mass_pendulum_) -
           pow(mass_pendulum_, 2) * pow(length_, 2) * pow(cos(state_[2]), 2));
  f_[2] = state_[3];
  f_[3] = ((mass_pendulum_ + mass_cart_) *
               (mass_pendulum_ * g_ * length_ * sin(state_[2])) -
           (input_ +
            mass_pendulum_ * length_ * pow(state_[3], 2) * sin(state_[2])) *
               mass_pendulum_ * length_ * cos(state_[2])) /
          ((inertia_ + mass_pendulum_ * pow(length_, 2)) *
               (mass_cart_ + mass_pendulum_) -
           pow(mass_pendulum_, 2) * pow(length_, 2) * pow(cos(state_[2]), 2));
}

void PhysicSimulator::addNoise(Vf noise) { f_ = f_ + noise; }

void PhysicSimulator::setHorizon(float horizon) { horizon_s_ = horizon; }

bool PhysicSimulator::isRunning() { return !sim_is_over_; }
}  // namespace physics_simulator