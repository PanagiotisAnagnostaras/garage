class Node {
 public:
  Node(int data);
  Node(int data, Node* next);
  static void printMe(Node *head);
  int data_;
  Node* next_;
};

void printLinkedList(Node *head);

Node* createLinkedList();