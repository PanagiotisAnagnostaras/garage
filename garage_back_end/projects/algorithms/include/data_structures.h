template<typename T>
class LinkedListNode {
 public:
  LinkedListNode(T data);
  LinkedListNode(T data, LinkedListNode* next);
  static void printMe(LinkedListNode *head);
  T data;
  LinkedListNode* next;
};
template <typename T>
void printLinkedList(LinkedListNode<T> *head);

LinkedListNode<int>* createLinkedList();
