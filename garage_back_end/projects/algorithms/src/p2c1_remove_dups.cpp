/*
Remove Dups: Write code to remove duplicates from an unsorted linked list.
*/
#include "p2c1_remove_dups.h"

void remove_dups(Node* head) {
  std::unordered_map<int, int> count_map;

  Node* current = head;
  Node* previous = nullptr;
  while (current != nullptr) {
    if (count_map.find(current->data_) == count_map.end()) {
      // not present
      count_map[current->data_] = 1;
      previous = current;
    } else {
      // present
      previous->next_ = current->next_;
      delete current;
    }
    
    current = previous->next_;
  }
  
}
