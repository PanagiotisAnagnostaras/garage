#include <linear_algebra.h>

namespace linear_algebra {
float l2_norm_squared(Vf const vector) {
  float res = 0;
  for (const float &el : vector.getInternalVector()) {
    res += pow(el, 2);
  }
  return res;
}

}  // namespace linear_algebra