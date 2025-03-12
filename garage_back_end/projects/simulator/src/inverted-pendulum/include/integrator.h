#pragma once

#include <linear_algebra.h>
#include <math.h>
#include <types.h>

#include <functional>
#include <iostream>
#include <memory>

namespace integrator {
enum solverType { EXPLICIT_EULER = 0 };

class I_NumericalIntegrator {
 public:
  I_NumericalIntegrator(float timestep_s_);
  [[nodiscard]] virtual Vf step(const Vf &f, const Vf &x) const = 0;

 protected:
  float timestep_s_;
};

class ExplicitEuler : public I_NumericalIntegrator {
 public:
  ExplicitEuler(float timestep_s_);
  Vf step(const Vf &f, const Vf &x) const override;
};

}  // namespace integrator