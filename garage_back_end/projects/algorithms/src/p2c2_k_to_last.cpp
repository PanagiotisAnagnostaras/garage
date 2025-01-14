/*
Return Kth to Last: Implement an algorithm to find the kth to last element of a
singly linked list.
*/
#include "p2c2_k_to_last.h"

template <typename T>
int k_to_last(LinkedListNode<T> *head, int k) {
  LinkedListNode<T> *fast = head;
  LinkedListNode<T> *slow = head;
  int steps_fast = 0;
  while (fast->next != nullptr) {
    fast = fast->next;
    steps_fast += 1;
    if (steps_fast > k) {
      slow = slow->next;
    }
  }
  return slow->data;
}

template int k_to_last<int>(LinkedListNode<int>*, int);
