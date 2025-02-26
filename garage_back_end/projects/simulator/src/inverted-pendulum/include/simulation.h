#include <thread>

#include "physics_sim.h"

namespace simulation {

class Simulation {
 public:
  Simulation();
  ~Simulation();
  void run(float horizon, bool realtime);
  void applyInput(float input);
  float getTime();
  void setCartPos(float val);
  void setCartVel(float val);
  void setPendAng(float val);
  void setPendVel(float val);
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