#include "data_structures.h"

Node::Node(int data) : data_(data) { next_ = nullptr; };
Node::Node(int data, Node* next) : data_(data), next_(next) {};