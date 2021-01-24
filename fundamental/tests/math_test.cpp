/*
 * UTF-8 encoding
 */
#include "../math.hpp"
#include <iostream>
int main() {
  using std::cout, std::endl;
  using namespace engineering::fundamental;
  cout << "pi = " << pi << endl;
  cout << "pi / 4 = " << pi_4 << endl;
  cout << "pi ^ 2 = " << pow(pi, 2) << endl;

  cout << "5 ^ 4 = " << pow(5_num, 4) << endl;
  cout << "5 ^ 4 = " << pow(5_num, 4_num) << endl;
  cout << "5 ^ 4 = " << pow(5, 4) << endl;

  cout << "5.0 ^ 4 = " << pow(5.0_num, 4) << endl;
  cout << "5.0 ^ 4 = " << pow(5.0_num, 4_num) << endl;
  cout << "5.0 ^ 4 = " << pow(5.0, 4) << endl;

  cout << "5.10 ^ 4 = " << pow(5.10_num, 4) << endl;
  cout << "5.10 ^ 4 = " << pow(5.10_num, 4_num) << endl;
  cout << "5.10 ^ 4 = " << pow(5.10, 4) << endl;

  cout << "5.134 ^ 4 = " << pow(5.134_num, 4) << endl;
  cout << "5.134 ^ 4 = " << pow(5.134_num, 4_num) << endl;
  cout << "5.134 ^ 4 = " << pow(5.134, 4) << endl;
}