class Node {
 public:
  Node(int data);
  Node(int data, Node* next);
  int data_;
  Node* next_;
};