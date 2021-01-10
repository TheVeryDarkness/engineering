#include "../concrete.hpp"
#include <iostream>
int main() {
  using std::cout, std::endl;
  using namespace structure::concrete;
  using namespace structure::fundamental;
  concrete c("2.51e4"_num, "30.8"_num, "1.97"_num);
  rebar s("2.05e5"_num, 376_num, {}, 681_num);
  single_rebar_rectangle_section example(152_num, 152_num, 284_num, c, s);
  cout << "Ntcr = " << example.Ntcr() << endl;
  cout << "Ntu = " << example.Ntu() << endl;
}