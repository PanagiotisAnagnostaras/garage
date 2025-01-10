#include "common_headers.h"
#include "is_unique.h"

int main() {
  std::cout << "Hello from inside algorithms" << std::endl;
  std::cout << "Running is Unique" << std::endl;
  std::cout << "yes: " << is_unique_1("yes") << std::endl;
  std::cout << "yes: " << is_unique_2("yes") << std::endl;
  std::cout << "hello: " << is_unique_1("hello") << std::endl;
  std::cout << "hello: " << is_unique_2("hello") << std::endl;
}