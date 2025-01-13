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

Node* make_partition(Node *header, int partition_value) {
  Node *less_head = nullptr;
  Node *less_tail = nullptr;
  Node *more_head = nullptr;
  Node *more_tail = nullptr;
  Node *current = header;
  while (current != nullptr) {
    Node *node = new Node(current->data_);
    if (node->data_ < partition_value) {
      if (less_head == nullptr) {
        less_head = node;
        less_tail = node;
      } else {
        less_tail->next_ = node;
        less_tail = node;
      }
    } else {
      if (more_head == nullptr) {
        more_head = node;
        more_tail = node;
      } else {
        more_tail->next_ = node;
        more_tail = node;
      }
    }
    printLinkedList(more_head);
    printLinkedList(less_head );
    current = current->next_;
  }
  less_tail->next_=more_head;
  return less_head;
}
