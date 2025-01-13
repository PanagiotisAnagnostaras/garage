/*
Delete Middle Node: Implement an algorithm to delete a node in the middle (i.e., any node but
the first and last node, not necessarily the exact middle) of a singly linked list, given only access to
that node.
*/
#include "p2c3_delete_middle_node.h"

void delete_node(Node *to_delete){
  to_delete->data_ = to_delete->next_->data_;
  to_delete->next_ = to_delete->next_->next_;
}
