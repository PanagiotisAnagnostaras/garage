#include "data_structures.h"

#include <iostream>

Node::Node(int data) : data_(data) { next_ = nullptr; };

Node::Node(int data, Node *next) : data_(data), next_(next) {};

void printLinkedList(Node *head) {
  Node *curr = head;
  while (curr != nullptr) {
    std::cout << curr->data_ << " ";
    curr = curr->next_;
  }
  std::cout << std::endl;
}

Node *createLinkedList() {
  // 12 -> 11 -> 12 -> 21 -> 41 -> 43 -> 21
  Node *head = new Node(12);
  head->next_ = new Node(11);
  head->next_->next_ = new Node(12);
  head->next_->next_->next_ = new Node(21);
  head->next_->next_->next_->next_ = new Node(41);
  head->next_->next_->next_->next_->next_ = new Node(43);
  head->next_->next_->next_->next_->next_->next_ = new Node(21);
  return head;
}