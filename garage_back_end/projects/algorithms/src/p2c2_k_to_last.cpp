/*
Return Kth to Last: Implement an algorithm to find the kth to last element of a
singly linked list.
*/
#include "p2c2_k_to_last.h"

int k_to_last(Node *head, int k) {
  Node *fast = head;
  Node *slow = head;
  int steps_fast = 0;
  while (fast->next_ != nullptr) {
    fast = fast->next_;
    steps_fast += 1;
    if (steps_fast > k) {
      slow = slow->next_;
    }
  }
  return slow->data_;
}
