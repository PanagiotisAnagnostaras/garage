#include "systems.h"

namespace systems {
void SystemsBase::setState(Vf state) {
  state_ = state;
}
void SystemsBase::setInput(Vf input) { input_ = input; }
Vf SystemsBase::getState() { return state_; }
Vf SystemsBase::getInput() { return input_; }
Vf SystemsBase::getDerivative() { return derivative_; }
std::string SystemsBase::getName() { return name_; };
uint SystemsBase::getNx() { return nx_; };
uint SystemsBase::getNu() { return nu_; };
void SystemsBase::resetStates() {
  Vf state, input, derivative;
  for (int i = 0; i < nx_; i++) {
    state.push_back(0);
    derivative.push_back(0);
  }
  for (int i = 0; i < nu_; i++) {
    input.push_back(0);
  }
  state_ = state;
  input_ = input;
  derivative_ = derivative;
}

Point2D::Point2D() {
  nx_ = 4;
  nu_ = 2;
  name_ = "Point 2D";
  resetStates();
}
void Point2D::computeDerivative() {
  derivative_[STATE_INDEX_X_POS] = state_[STATE_INDEX_X_VEL];
  derivative_[STATE_INDEX_X_VEL] = input_[INPUT_INDEX_X_FORCE];
  derivative_[STATE_INDEX_Y_POS] = state_[STATE_INDEX_Y_VEL];
  derivative_[STATE_INDEX_Y_VEL] = input_[INPUT_INDEX_Y_FORCE];
}

InvertedPendulum::InvertedPendulum() {
  nx_ = 4;
  nu_ = 1;
  name_ = "Inverted Pendulum";
  resetStates();
}

void InvertedPendulum::computeDerivative() {
  std::cout << "states = " << state_.getInternalVector().size() << std::endl;
  std::cout << "a" << std::endl;
  derivative_[STATE_INDEX_CART_POS] = state_[STATE_INDEX_CART_VEL];
  std::cout << "b" << std::endl;
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
  std::cout << "c" << std::endl;
  derivative_[STATE_INDEX_PEND_ANG] = state_[STATE_INDEX_PEND_VEL];
  std::cout << "d" << std::endl;
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