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


// template<typename T>
// class Stack{
//   public:
//     Stack(LinkedListNode<T> top);
//     LinkedListNode<T> top;
//     void pop();
//     void push(LinkedListNode<T> new_top);
//     T peek();
//     bool isEmpty();
// };