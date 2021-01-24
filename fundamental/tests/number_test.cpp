#include "../number.hpp"
#include <iostream>
using engineering::fundamental::unsigned_number, engineering::fundamental::operator""_num;
using std::cout, std::endl;
void add_test(unsigned_number a, unsigned_number b) { cout << a << " + " << b << " = " << a + b << endl; }
void minus_test(unsigned_number a, unsigned_number b) { cout << a << " - " << b << " = " << a - b << endl; }
void mul_test(unsigned_number a, unsigned_number b) { cout << a << " * " << b << " = " << a * b << endl; }
void div_test(unsigned_number a, unsigned_number b) { cout << a << " / " << b << " = " << a / b << endl; }
int main() noexcept {
  // basic tests
  {
    auto a = 0.001_num;
    assert(0.001_num.to_string() == "1.e-3");
    assert("0.001"_num.to_string() == "1.e-3");
  }
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
    unsigned_number a = 0.196_num;
    unsigned_number _1 = unsigned_number::exact(1);
    auto b = _1 - a;
    cout << "1 - 0.196 = " << _1 << " - " << a << " = " << b << endl;
  }
  {
    auto a = unsigned_number(10, 3), b = "0.010"_num, c = "1.0e-2"_num;

    assert(a == b);
    assert(a == c);
    assert(b == c);
  }
}