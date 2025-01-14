/*
Remove Dups: Write code to remove duplicates from an unsorted linked list.
*/
#include "p2c1_remove_dups.h"

template <typename T>
void remove_dups(LinkedListNode<T>* head) {
  std::unordered_map<T, int> count_map;

  LinkedListNode<T>* current = head;
  LinkedListNode<T>* previous = nullptr;
  while (current != nullptr) {
    if (count_map.find(current->data) == count_map.end()) {
      // not present
      count_map[current->data] = 1;
      previous = current;
    } else {
      // present
      previous->next = current->next;
      delete current;
    }
    
    current = previous->next;
  }
  
}

template void remove_dups<int>(LinkedListNode<int>*);
