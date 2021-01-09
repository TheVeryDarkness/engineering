#include "../number.hpp"
#include <iostream>
int main() noexcept {
  using structure::fundamental::unsigned_number;
  unsigned_number<> a(10, 3), b(10, 3);
  a *= b;
  a /= b;
  using std::cout, std::endl;
  cout << a.to_string() << endl;
}