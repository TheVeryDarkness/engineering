#include "../number.hpp"
#include <iostream>
int main() noexcept {
  using structure::fundamental::unsigned_number;
  unsigned_number<> a(10, 3), b(10, 3);
  using std::cout, std::endl;
  cout << "a = " << a.to_string() << "\nb = " << b.to_string() << endl;
  a *= b;
  cout << "a *= b" << endl;
  cout << "a = " << a.to_string() << endl;
  a /= b;
  cout << "a /= b" << endl;
  cout << "a = " << a.to_string() << endl;
}