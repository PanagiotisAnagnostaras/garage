#include "common_headers.h"
#include "p1c1_is_unique.h"
#include "p1c2_check_permutations.h"
#include "p1c3_urlfy.h"
#include "p1c4_palindrome_permutation.h"
#include "p2c1_remove_dups.h"
#include "p2c2_k_to_last.h"
#include "p2c3_delete_middle_node.h"
#include "p2c4_partition.h"

int main() {
  std::cout << std::endl;

  std::cout << "***************" << std::endl;
  std::cout << "Hello from inside algorithms" << std::endl;
  std::cout << "***************" << std::endl;

  // Chapter 1: Arrays and Strings
  // 1.1 is_unique
  std::cout << "--------------------------" << std::endl;
  std::cout << "Running is Unique" << std::endl;
  std::cout << "--------------------------" << std::endl;
  std::cout << "yes: " << is_unique_1("yes") << std::endl;
  std::cout << "yes: " << is_unique_2("yes") << std::endl;
  std::cout << "hello: " << is_unique_1("hello") << std::endl;
  std::cout << "hello: " << is_unique_2("hello") << std::endl;
  // 1.2 check_permutations
  std::cout << "--------------------------" << std::endl;
  std::cout << "Running check permutations" << std::endl;
  std::cout << "--------------------------" << std::endl;
  std::string s1{"asd"}, s2{"sad"}, s3{"cdc"};
  std::cout << s1 << ", " << s2 << ": " << check_permutations_1(s1, s2)
            << std::endl;
  std::cout << s1 << ", " << s3 << ": " << check_permutations_1(s1, s3)
            << std::endl;
  // 1.3 replace spaces
  std::cout << "--------------------------" << std::endl;
  std::cout << "Running replace spaces" << std::endl;
  std::cout << "--------------------------" << std::endl;
  std::string s4{"Mr John Smith    "};
  std::cout << "before: " << s4 << std::endl;
  replace_spaces(s4);
  std::cout << "after: " << s4 << std::endl;
  std::string s5{"M   J      "};
  std::cout << "before: " << s5 << std::endl;
  replace_spaces(s5);
  std::cout << "after: " << s5 << std::endl;
  // 1.4 palindrome permutation
  std::cout << "--------------------------" << std::endl;
  std::cout << "Running palindrome permutation" << std::endl;
  std::cout << "--------------------------" << std::endl;
  std::string s6{"dsasd"};
  std::string s7{"dsasd "};
  std::string s8{"asdsd"};
  std::string s9{"assd"};
  std::string s10{"ss"};
  std::cout << s10 << " is palindrome permutation:" << std::endl;
  std::cout << palindrome_permutation(s10) << std::endl;

  // Chapter 2: Linked Lists
  // Create a singly linked list:
  LinkedListNode<int>* head = createLinkedList();
  std::cout << "Example list:" << std::endl;
  printLinkedList(head);
  // 2.1 remove duplicate linked list
  std::cout << "--------------------------" << std::endl;
  std::cout << "Running remove duplicates linked list" << std::endl;
  std::cout << "--------------------------" << std::endl;
  remove_dups(head);
  printLinkedList(head);
  // 2.2 return kth to last
  std::cout << "--------------------------" << std::endl;
  std::cout << "Return kth to last element linked list" << std::endl;
  std::cout << "--------------------------" << std::endl;
  std::cout << "List " << std::endl;
  printLinkedList(head);
  std::cout << "3 to last = " << k_to_last(head, 3) << std::endl;
  std::cout << "0 to last = " << k_to_last(head, 0) << std::endl;
  // 2.3 delete a node
  std::cout << "--------------------------" << std::endl;
  std::cout << "Delete a LinkedListNode" << std::endl;
  std::cout << "--------------------------" << std::endl;
  std::cout << "List before:" << std::endl;
  printLinkedList(head);
  std::cout << "Delete: " << head->next->next->data << std::endl;
  delete_node(head->next->next);
  std::cout << "List after:" << std::endl;
  printLinkedList(head);
  // 2.4 partition linked list
  std::cout << "--------------------------" << std::endl;
  std::cout << "Partition list" << std::endl;
  std::cout << "--------------------------" << std::endl;
  LinkedListNode<int>* head_2 = createLinkedList();
  std::cout << "List before" << std::endl;
  printLinkedList<int>(head_2);
  std::cout << "Partition at 40" << std::endl;
  head_2 = make_partition<int>(head_2, 40);
  std::cout << "List after" << std::endl;
  printLinkedList<int>(head_2);

  // Chapter 3: Stacks and Queues
  // 3.1
}