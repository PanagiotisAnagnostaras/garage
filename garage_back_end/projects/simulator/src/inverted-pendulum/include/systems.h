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

 protected:
  Vf state_;
  Vf input_;
  Vf derivative_;
};

class Point2D : public SystemsBase {
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
  static constexpr uint STATE_INDEX_CART_POS = 0;
  static constexpr uint STATE_INDEX_CART_VEL = 1;
  static constexpr uint STATE_INDEX_PEND_ANG = 2;
  static constexpr uint STATE_INDEX_PEND_VEL = 3;
  void computeDerivative();

 private:
  float mass_cart_, mass_pendulum_, length_, g_, inertia_;
};
}  // namespace systems