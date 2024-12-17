#include <integrator.h>

namespace integrator {
Vf ExplicitEuler::step(const Vf &f, const Vf &x) const {
  return x + f * timestep_s_;
}

}  // namespace integrator