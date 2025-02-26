#include "simulation.h"
namespace simulation {
Simulation::Simulation() {};

Simulation::~Simulation() {};

void Simulation::run(float horizon, bool realtime) {
  physicSimulator_.setHorizon(horizon);
  std::thread thread_simulation(
      [this, realtime]() { this->physicSimulator_.simulate(realtime); });
  std::thread thread_controller(
      [this]() { this->physicSimulator_.run_controller(); });
  thread_simulation.join();
  thread_controller.join();
}

void Simulation::applyInput(float input) { physicSimulator_.applyInput(input); }

void Simulation::setCartPos(float val) { physicSimulator_.setCartPos(val); }

void Simulation::setCartVel(float val) { physicSimulator_.setCartVel(val); }

void Simulation::setPendAng(float val) { physicSimulator_.setPendAng(val); }

void Simulation::setPendVel(float val) { physicSimulator_.setPendVel(val); }

float Simulation::getCartPos() { return physicSimulator_.getCartPos(); }

float Simulation::getCartVel() { return physicSimulator_.getCartVel(); }

float Simulation::getPendAng() { return physicSimulator_.getPendAng(); }

float Simulation::getPendVel() { return physicSimulator_.getPendVel(); }

float Simulation::getInput() { return physicSimulator_.getInput(); }

float Simulation::getTime() { return physicSimulator_.getTime(); }

bool Simulation::isRunning() { return physicSimulator_.isRunning(); }

}  // namespace simulation
