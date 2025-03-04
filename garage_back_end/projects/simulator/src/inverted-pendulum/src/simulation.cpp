#include "simulation.h"
namespace simulation {
Simulation::Simulation() {};

Simulation::~Simulation() {};

void Simulation::run(float horizon, bool realtime) {
  Guard guard(mutex);
  physicSimulator_.setHorizon(horizon);
  std::thread thread_simulation(
      [this, realtime]() { this->physicSimulator_.simulate(realtime); });
  std::thread thread_controller(
      [this]() { this->physicSimulator_.run_controller(); });
  thread_simulation.join();
  thread_controller.join();
}

void Simulation::applyInput(float input) {
  Guard guard(mutex);
  physicSimulator_.applyInput(input);
}

void Simulation::setCartPos(float val) {
  Guard guard(mutex);
  physicSimulator_.setCartPos(val);
}

void Simulation::setCartVel(float val) {
  Guard guard(mutex);
  physicSimulator_.setCartVel(val);
}

void Simulation::setPendAng(float val) {
  Guard guard(mutex);
  physicSimulator_.setPendAng(val);
}

void Simulation::setPendVel(float val) {
  Guard guard(mutex);
  physicSimulator_.setPendVel(val);
}

float Simulation::getCartPos() {
  Guard guard(mutex);
  return physicSimulator_.getCartPos();
}

float Simulation::getCartVel() {
  Guard guard(mutex);
  return physicSimulator_.getCartVel();
}

float Simulation::getPendAng() {
  Guard guard(mutex);
  return physicSimulator_.getPendAng();
}

float Simulation::getPendVel() {
  Guard guard(mutex);
  return physicSimulator_.getPendVel();
}

float Simulation::getInput() {
  Guard guard(mutex);
  return physicSimulator_.getInput();
}

float Simulation::getTime() {
  Guard guard(mutex);
  return physicSimulator_.getTime();
}

bool Simulation::isRunning() {
  Guard guard(mutex);
  return physicSimulator_.isRunning();
}

}  // namespace simulation
