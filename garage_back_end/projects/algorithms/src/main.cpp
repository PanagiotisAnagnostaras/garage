#include "check_permutations.h"
#include "common_headers.h"
#include "is_unique.h"
#include "urlfy.h"

int main() {
  std::cout << "Hello from inside algorithms" << std::endl;
  // is_unique
  std::cout << "--------------------------" << std::endl;
  std::cout << "Running is Unique" << std::endl;
  std::cout << "--------------------------" << std::endl;
  std::cout << "yes: " << is_unique_1("yes") << std::endl;
  std::cout << "yes: " << is_unique_2("yes") << std::endl;
  std::cout << "hello: " << is_unique_1("hello") << std::endl;
  std::cout << "hello: " << is_unique_2("hello") << std::endl;
  // check_permutations
  std::cout << "--------------------------" << std::endl;
  std::cout << "Running check permutations" << std::endl;
  std::cout << "--------------------------" << std::endl;
  std::string s1{"asd"}, s2{"sad"}, s3{"cdc"};
  std::cout << s1 << ", " << s2 << ": " << check_permutations_1(s1, s2)
            << std::endl;
  std::cout << s1 << ", " << s3 << ": " << check_permutations_1(s1, s3)
            << std::endl;
  // replace spaces
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
}