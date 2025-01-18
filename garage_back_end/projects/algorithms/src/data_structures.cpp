#include "data_structures.h"

#include <iostream>

template <typename T>
LinkedListNode<T>::LinkedListNode(T data) : data(data) { next = nullptr; };

template <typename T>
LinkedListNode<T>::LinkedListNode(T data, LinkedListNode *next) : data(data), next(next) {};

template <typename T>
void printLinkedList(LinkedListNode<T> *head) {
  LinkedListNode<T> *curr = head;
  while (curr != nullptr) {
    std::cout << curr->data << " ";
    curr = curr->next;
  }
  std::cout << std::endl;
}

LinkedListNode<int> *createLinkedList() {
  // 12 -> 11 -> 12 -> 21 -> 41 -> 43 -> 21
  LinkedListNode<int> *head = new LinkedListNode(12);
  head->next = new LinkedListNode(11);
  head->next->next = new LinkedListNode(12);
  head->next->next->next = new LinkedListNode(21);
  head->next->next->next->next = new LinkedListNode(41);
  head->next->next->next->next->next = new LinkedListNode(43);
  head->next->next->next->next->next->next = new LinkedListNode(21);
  return head;
}

template void printLinkedList<int>(LinkedListNode<int>*);


// template <typename T>
// Stack<T>::Stack(LinkedListNode<T> top) : top(top){};

// template <typename T>
// bool Stack<T>::isEmpty(){return top==nullptr;}

// template <typename T>
// T Stack<T>::peek(return top->)