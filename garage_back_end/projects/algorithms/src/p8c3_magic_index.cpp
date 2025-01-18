#include "p8c3_magic_index.h"

/*
Magic Index: A magic index in an array A[ 1.•.n-1] is defined to be an index
such that A[ i] i. Given a sorted array of distinct integers, write a method to
find a magic index, if one exists, in array A. FOLLOW UP What if the values are
not distinct?
*/

int find_magic_index_1(std::vector<int> vec) {
  for (int i = 0; i < vec.size(); i++) {
    if (vec[i] == i) {
      return i;
    }
  }
  return -1;
}

// -1 0 2 10 12 15
//  0 1 2 3  4  5
int find_magic_index_2(std::vector<int> vec) {
  std::vector<int>::iterator front = vec.begin();
  std::vector<int>::iterator back = vec.end() - 1;
  int mid = (back - front) / 2;
  while (back - front > 1) {
    if (*(front + mid) == mid) {
      return mid;
    } else if (*(front + mid) > mid) {
      back = front + mid;
      mid = (back - front) / 2;
    } else {
      front = front + mid;
      mid = (back - front) / 2;
    }
  }
  return -1;
}