#include <integrator.h>

namespace integrator {
I_NumericalIntegrator::I_NumericalIntegrator(float timestep_s_)
    : timestep_s_(timestep_s_) {};

ExplicitEuler::ExplicitEuler(float timestep_s_)
    : I_NumericalIntegrator(timestep_s_) {};

Vf ExplicitEuler::step(const Vf &f, const Vf &x) const {
  return x + f * timestep_s_;
}

}  // namespace integrator