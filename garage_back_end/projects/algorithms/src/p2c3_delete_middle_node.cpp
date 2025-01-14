/*
Delete Middle LinkedListNode: Implement an algorithm to delete a node in the middle (i.e., any node but
the first and last node, not necessarily the exact middle) of a singly linked list, given only access to
that node.
*/
#include "p2c3_delete_middle_node.h"

template <typename T>
void delete_node(LinkedListNode<T> *to_delete){
  to_delete->data = to_delete->next->data;
  to_delete->next = to_delete->next->next;
}

template void delete_node<int>(LinkedListNode<int>*);
