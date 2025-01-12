// Given two strings, write a method to determine if a one is a permutation of the other.
#include "check_permutations.h"

// O(NlogN)
bool check_permutations_1(std::string str1, std::string str2){
  if (str1.length()!=str2.length()){
    return false;
  }
  // O(NlogN)
  std::sort(str1.begin(), str1.end());
  std::sort(str2.begin(), str2.end());
  std::string::const_iterator c2 = str2.begin();
  // O(N)
  return str1==str2;
}