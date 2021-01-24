#include "../concrete.hpp"
#include <iostream>
int main() {
  using std::cout, std::endl;
  using namespace engineering::structure::concrete;
  using namespace engineering::fundamental;
  //
  concrete c("2.51e4"_num, "30.8"_num, "1.97"_num);
  steel s("2.05e5"_num, 376_num, {}, 681_num);
  rebar b(19.0_num);
  rectangle r(152_num, 152_num, b.As());
  longitudinal_rebar_rectangle_section example(b, r, c, s);
  // Ex. 4-1
  cout << "Ntcr = " << example.Ntcr() << endl;
  cout << "Ntu = " << example.Ntu() << endl;
}