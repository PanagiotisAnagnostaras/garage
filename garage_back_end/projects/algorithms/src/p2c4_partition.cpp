/*
Partition: Write code to partition a linked list around a value x, such that all
nodes less than x come before all nodes greater than or equal to x. If x is
contained within the list, the values of x only need to be after the elements
less than x (see below). The partition element x can appear anywhere in the
"right partition"; it does not need to appear between the left and right
partitions. EXAMPLE Input:3 -> 5 -> 8 -> 5 -> 10 -> 2 -> 1 [partition= 5]
Output:3 -> 1 -> 2 -> 10 -> 5 -> 5 -> 8
*/
#include "p2c4_partition.h"

template <typename T>
LinkedListNode<T>* make_partition(LinkedListNode<T> *header, T partition_value) {
  LinkedListNode<T> *less_head = nullptr;
  LinkedListNode<T> *less_tail = nullptr;
  LinkedListNode<T> *more_head = nullptr;
  LinkedListNode<T> *more_tail = nullptr;
  LinkedListNode<T> *current = header;
  while (current != nullptr) {
    LinkedListNode<T> *node = new LinkedListNode(current->data);
    if (node->data < partition_value) {
      if (less_head == nullptr) {
        less_head = node;
        less_tail = node;
      } else {
        less_tail->next = node;
        less_tail = node;
      }
    } else {
      if (more_head == nullptr) {
        more_head = node;
        more_tail = node;
      } else {
        more_tail->next = node;
        more_tail = node;
      }
    }
    current = current->next;
  }
  less_tail->next=more_head;
  return less_head;
}

template LinkedListNode<int>* make_partition<int>(LinkedListNode<int>*, int);
