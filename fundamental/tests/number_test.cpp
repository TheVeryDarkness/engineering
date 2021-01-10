#include "../number.hpp"
#include <iostream>
using std::cout, std::endl;
using structure::fundamental::unsigned_number,
    structure::fundamental::operator""_num;
void add_test(unsigned_number a, unsigned_number b) {
  cout << a << " + " << b << " = " << a + b << endl;
}
void minus_test(unsigned_number a, unsigned_number b) {
  cout << a << " - " << b << " = " << a - b << endl;
}
void mul_test(unsigned_number a, unsigned_number b) {
  cout << a << " * " << b << " = " << a * b << endl;
}
void div_test(unsigned_number a, unsigned_number b) {
  cout << a << " / " << b << " = " << a / b << endl;
}
int main() noexcept {
  // basic tests
  {
    add_test("0.001"_num, "0.001"_num);
    add_test("0.001"_num, "0.0001"_num);
    add_test("0.0001"_num, "0.001"_num);
    add_test("0.006"_num, "0.006"_num);
    add_test("0.006"_num, "0.0006"_num);
    add_test("0.0006"_num, "0.006"_num);

    minus_test("0.001"_num, "0.001"_num);
    minus_test("0.001"_num, "0.0001"_num);
    minus_test("0.004"_num, "0.0036"_num);
    minus_test("0.0040"_num, "0.0036"_num);
    minus_test("0.037"_num, "0.036"_num);

    mul_test("0.001"_num, "0.001"_num);
    mul_test("0.001"_num, "0.0001"_num);
    mul_test("0.0001"_num, "0.001"_num);
    mul_test("0.004"_num, "0.004"_num);
    mul_test("0.004"_num, "0.0004"_num);
    mul_test("0.0004"_num, "0.004"_num);

    div_test("0.001"_num, "0.001"_num);
    div_test("0.001"_num, "0.0001"_num);
    div_test("0.0001"_num, "0.001"_num);
    div_test("0.004"_num, "0.004"_num);
    div_test("0.004"_num, "0.0004"_num);
    div_test("0.0004"_num, "0.004"_num);
  }
  {
    mul_test(152_num, 152_num);
    auto x = "1.97"_num;
    cout << x << " * ";
    auto y = 2.31e4_num;
    cout << y << " * ";
    auto z = unsigned_number::exact(1) + 8.17_num * 0.0123_num;
    cout << z << " = ";
    cout << x * y * z << endl;
  }
  {
    auto a = unsigned_number(10, 3), b = "0.010"_num, c = "1.0e-2"_num;

    assert(a == b);
    assert(a == c);
    assert(b == c);
  }
}