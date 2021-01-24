/*
 * UTF-8 encoding
 */
#include "../math.hpp"
#include <iostream>
#define POW_TEST_INT(b, e)                                                                                             \
  cout << #b "^" #e " = " << pow(b##_num, e) << endl                                                                   \
       << #b "^" #e " = " << pow(b##_num, e##_num) << endl                                                             \
       << #b "^" #e " = " << pow(b, e) << endl
#define POW_TEST_DEC(b, e)                                                                                             \
  cout << #b "^" #e " = " << pow(b##_num, e##_num) << endl << #b "^" #e " = " << pow(b, e) << endl
int main() {
  using std::cout, std::endl;
  using namespace engineering::fundamental;
  cout << "pi = " << pi << endl;
  cout << "pi / 4 = " << pi_4 << endl;
  cout << "pi ^ 2 = " << pow(pi, 2) << endl;

  POW_TEST_INT(0.3, 4);
  POW_TEST_INT(0.30, 4);
  POW_TEST_INT(0.30, 6);
  POW_TEST_INT(0.9, 64);
  POW_TEST_INT(0.90, 64);
  POW_TEST_INT(0.900, 64);
  POW_TEST_INT(0.9000, 64);
  POW_TEST_INT(5, 4);
  POW_TEST_INT(5.0, 4);
  POW_TEST_INT(5.10, 4);
  POW_TEST_INT(5.134, 4);

  POW_TEST_DEC(0.134, 0.5);
  POW_TEST_DEC(0.134, 0.50);
  POW_TEST_DEC(0.134, 0.500);
  POW_TEST_DEC(0.134, 0.5000);
  POW_TEST_DEC(0.134, 2.5);
}