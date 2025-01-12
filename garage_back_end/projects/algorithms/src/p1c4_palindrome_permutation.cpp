/*
Given a string, write a function to check if it is a permutation of a
palin­drome. A palindrome is a word or phrase that is the same forwards and
backwards. A permutation is a rearrangement of letters. The palindrome does not
need to be limited to just dictionary words. EXAMPLE Input:Tact Coa Output:True
(permutations: "taco cat", "atco eta", etc.)
*/
#include "p1c4_palindrome_permutation.h"

bool palindrome_permutation(std::string str) {
  std::unordered_map<char, int> count_map;
  // O(N)
  for (char letter : str) {
    if (count_map.find(letter) == count_map.end()) {
      count_map[letter] = 1;
    } else {
      count_map[letter] += 1;
    }
  }
  int count_even = 0;
  int count_odd = 0;
  // O(N)
  for (std::pair<char, int> pair : count_map) {
    if (pair.second % 2 == 0) {
      count_even += 1;
    } else {
      count_odd += 1;
    }
  }
  return count_odd <= 1;
}