// Implement an algorithm to determine if a string has all unique characters.
// What if you cannot use additional data structures.
#include "is_unique.h"

// O(n^2)
bool is_unique_n_squared(std::string str) {
  std::string unique_elements = "";
  for (char letter : str) {
    if (unique_elements.find(letter) == std::string::npos) {
      unique_elements.append(1, letter);
    }
  }
  return unique_elements.length() == str.length();
}

bool is_unique(std::string str) {
  std::sort(str.begin(), str.end());
  for (auto letter = str.begin(); letter < str.end() - 1; letter++) {
    if (*letter == *(letter + 1)) {
      return false;
    }
  }
  return true;
}