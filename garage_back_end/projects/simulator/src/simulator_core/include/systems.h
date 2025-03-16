#include <cmath>

#include "types.h"

namespace systems {
enum SystemType { POINT_2D = 0, INVERTED_PENDULUM = 1 };

class SystemsBase {
 public:
  SystemsBase() = default;
  ~SystemsBase() = default;
  void setState(Vf state);
  void setInput(Vf input);
  Vf getState();
  Vf getInput();
  virtual void computeDerivative() = 0;
  Vf getDerivative();
  uint getNx();
  uint getNu();
  std::string getName();
  void resetStates();

 protected:
  Vf state_;
  Vf input_;
  Vf derivative_;
  uint nx_, nu_;
  std::string name_;
};

class Point2D : public SystemsBase {
 public:
  Point2D();
  static constexpr uint STATE_INDEX_X_POS = 0;
  static constexpr uint STATE_INDEX_X_VEL = 1;
  static constexpr uint STATE_INDEX_Y_POS = 2;
  static constexpr uint STATE_INDEX_Y_VEL = 3;
  static constexpr uint INPUT_INDEX_X_FORCE = 0;
  static constexpr uint INPUT_INDEX_Y_FORCE = 1;
  void computeDerivative();
};

class InvertedPendulum : public SystemsBase {
 public:
  InvertedPendulum();
  static constexpr uint STATE_INDEX_CART_POS = 0;
  static constexpr uint STATE_INDEX_CART_VEL = 1;
  static constexpr uint STATE_INDEX_PEND_ANG = 2;
  static constexpr uint STATE_INDEX_PEND_VEL = 3;
  void computeDerivative();

 private:
  const float mass_cart_{1}, mass_pendulum_{1}, length_{1}, g_{9.81},
      inertia_{1};
};
}  // namespace systems