#include "p8c1_triple_step.h"

/*
Triple Step: A child is running up a staircase with n steps and can hop either 1
step, 2 steps, or 3 steps at a time. Implement a method to count how many
possible ways the child can run up the stairs.
*/

// O(3^n)
int count_ways_1(int steps) {
  if (steps == 0) {
    return 1;
  }
  if (steps < 0) {
    return 0;
  }
  return count_ways_1(steps - 1) + count_ways_1(steps - 2) +
         count_ways_1(steps - 3);
}

int count_ways_2(int steps) {
  std::unordered_map<int, int> step_map;  // key: steps, value: ways
  step_map[0] = 1;

  return recurse_2(step_map, steps);
}

int recurse_2(std::unordered_map<int, int> &step_map, int steps) {
  if (steps < 0) {
    return 0;
  }
  if (steps == 0) {
    return 1;
  }
  if (step_map.find(steps) != step_map.end()) {
    return step_map[steps];
  } else {
    step_map[steps] = recurse_2(step_map, steps - 1) +
                      recurse_2(step_map, steps - 2) +
                      recurse_2(step_map, steps - 3);
  }
  return step_map[steps];  // why do I need this here?
}