/*
 * UTF-8 encoding
 */
#include "../unsigned/math.hpp"
#include <iostream>
int main() {
  using std::cout, std::endl;
  using namespace engineering::fundamental;
  using namespace engineering;

#define POW_TEST_INT(b, e)                                                                                             \
  {                                                                                                                    \
    cout << #b "^" #e " = " << pow(b##_num, e) << endl                                                                 \
         << #b "^" #e " = " << pow(b##_num, e##_num) << endl                                                           \
         << #b "^" #e " = " << std::pow(b, e) << endl;                                                                 \
  }

#define POW_TEST_DEC(b, e)                                                                                             \
  {                                                                                                                    \
    const auto right = std::pow(b, e);                                                                                 \
    const unsigned_number calculated = pow(b##_num, e##_num);                                                          \
    const auto calculated_as_float = calculated.as_float<double>();                                                    \
    cout << #b "^" #e " = " << calculated << endl << #b "^" #e " = " << right << endl;                                 \
    assert(std::abs(calculated_as_float - right) / right < 0.01);                                                      \
  }

  cout << "pi = " << pi << endl;
  cout << "pi / 4 = " << pi_4 << endl;
  cout << "pi ^ 2 = " << pow(pi, 2) << endl;

  POW_TEST_INT(0.3, 4);
  POW_TEST_INT(0.30, 4);
  POW_TEST_INT(0.30, 6);
  POW_TEST_INT(0.8, 64);
  POW_TEST_INT(0.9, 64);
  POW_TEST_INT(0.90, 64);
  POW_TEST_INT(0.900, 64);
  POW_TEST_INT(0.9000, 64);
  POW_TEST_INT(5, 4);
  POW_TEST_DEC(5.0, 4.0);
  POW_TEST_DEC(5.00, 4.0);
  POW_TEST_DEC(5.10, 4.00);
  POW_TEST_DEC(5.134, 4.000);

  POW_TEST_DEC(0.1340, 0.5);
  POW_TEST_DEC(0.1340, 0.50);
  POW_TEST_DEC(0.1340, 0.500);
  POW_TEST_DEC(0.1340, 0.5000);
  POW_TEST_DEC(0.001340, 0.5000);
  POW_TEST_DEC(0.1000, 0.5000);
  POW_TEST_DEC(0.10000, 0.50000);
  POW_TEST_DEC(0.100000, 0.500000);
  POW_TEST_DEC(0.1000000, 0.5000000);
  POW_TEST_DEC(0.01000, 0.5000);
  POW_TEST_DEC(0.1340, 2.50000);
  POW_TEST_DEC(0.1340, 13);
  POW_TEST_DEC(0.0134000, 0.500000);
  POW_TEST_DEC(0.01340000, 0.5000000);
}