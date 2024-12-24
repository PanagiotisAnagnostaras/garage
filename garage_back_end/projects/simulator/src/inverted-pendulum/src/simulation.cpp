#include "simulation.h"
namespace simulation{
Simulation::Simulation() {};

Simulation::~Simulation() {};

void Simulation::run(float horizon) {
  physicSimulator_.setHorizon(horizon);
  std::thread thread_simulation([this]() { this->physicSimulator_.simulate(); });
  std::thread thread_controller([this]() { this->physicSimulator_.run_controller(); });
  thread_simulation.join();
  thread_controller.join();
}

float Simulation::getCartPos(){ 
  return physicSimulator_.getCartPos();
}

float Simulation::getCartVel(){ 
  return physicSimulator_.getCartVel();
}

float Simulation::getPendAng(){ 
  return physicSimulator_.getPendAng();
}

float Simulation::getPendVel(){ 
  return physicSimulator_.getPendVel();
}

float Simulation::getInput(){ 
  return physicSimulator_.getInput();
}

float Simulation::getTime() {
  return physicSimulator_.getTime();
}
bool Simulation::isRunning() {
  return physicSimulator_.isRunning();
}
}
