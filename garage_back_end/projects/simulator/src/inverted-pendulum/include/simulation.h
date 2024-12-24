#include <thread>

#include "physics_sim.h"

namespace simulation {

class Simulation {
 public:
  Simulation();
  ~Simulation();
  void run(float horizon);
  float getTime();
  float getCartPos();
  float getCartVel();
  float getPendAng();
  float getPendVel();
  float getInput();
  
  bool isRunning();

 private:
  physics_simulator::PhysicSimulator physicSimulator_;
  float horizon_;
};

}  // namespace simulation