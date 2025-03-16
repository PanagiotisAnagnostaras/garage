#include "systems.h"

namespace systems {
void SystemsBase::setState(Vf state) { state_ = state; }
void SystemsBase::setInput(Vf input) { input_ = input; }
Vf SystemsBase::getState() { return state_; }
Vf SystemsBase::getInput() { return input_; }
Vf SystemsBase::getDerivative() { return derivative_; }

void Point2D::computeDerivative() {
  derivative_[STATE_INDEX_X_POS] = state_[STATE_INDEX_X_VEL];
  derivative_[STATE_INDEX_X_VEL] = input_[INPUT_INDEX_X_FORCE];
  derivative_[STATE_INDEX_Y_POS] = state_[STATE_INDEX_Y_VEL];
  derivative_[STATE_INDEX_Y_VEL] = input_[INPUT_INDEX_Y_FORCE];
}
void InvertedPendulum::computeDerivative() {
  derivative_[STATE_INDEX_CART_POS] = state_[STATE_INDEX_CART_VEL];
  derivative_[STATE_INDEX_CART_VEL] =
      (-pow(mass_pendulum_, 2) * pow(length_, 2) * g_ *
           cos(state_[STATE_INDEX_PEND_ANG]) *
           sin(state_[STATE_INDEX_PEND_ANG]) +
       (input_[0] + mass_pendulum_ * length_ *
                        pow(state_[STATE_INDEX_PEND_VEL], 2) *
                        sin(state_[STATE_INDEX_PEND_ANG])) *
           (inertia_ + mass_pendulum_ * pow(length_, 2))) /
      ((inertia_ + mass_pendulum_ * pow(length_, 2)) *
           (mass_cart_ + mass_pendulum_) -
       pow(mass_pendulum_, 2) * pow(length_, 2) *
           pow(cos(state_[STATE_INDEX_PEND_ANG]), 2));
  derivative_[STATE_INDEX_PEND_ANG] = state_[STATE_INDEX_PEND_VEL];
  derivative_[STATE_INDEX_PEND_VEL] =
      ((mass_pendulum_ + mass_cart_) *
           (mass_pendulum_ * g_ * length_ * sin(state_[STATE_INDEX_PEND_ANG])) -
       (input_[0] + mass_pendulum_ * length_ *
                        pow(state_[STATE_INDEX_PEND_VEL], 2) *
                        sin(state_[STATE_INDEX_PEND_ANG])) *
           mass_pendulum_ * length_ * cos(state_[STATE_INDEX_PEND_ANG])) /
      ((inertia_ + mass_pendulum_ * pow(length_, 2)) *
           (mass_cart_ + mass_pendulum_) -
       pow(mass_pendulum_, 2) * pow(length_, 2) *
           pow(cos(state_[STATE_INDEX_PEND_ANG]), 2));
}
}  // namespace systems