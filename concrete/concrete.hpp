/*
 * UTF-8 encoding.
 */
#pragma once
#include "../fundamental/number.hpp"
namespace structure {
namespace concrete {
class concrete {
protected:
  using num = typename fundamental::unsigned_number;
  // 抗压强度标准值即强度等级，为整数。
  static num fcuk_to_fck(num::valid_number_t fcuk) {
    num alpah1 = fcuk <= 50 ? num(76, 2) // 0.76
                 : fcuk >= 80
                     ? num(82, 2)                 // 0.82
                     : num(fcuk - 50) * num(2, 3) // (0.82 - 0.76) / (80 - 50)
        ;
    num alpha2 = fcuk <= 40 ? num(100, 2) // 1.00
                 : fcuk >= 80
                     ? num(87, 2) // 0.87
                     : num(100 - 87, 2) / num(80 - 40, 2) * num(fcuk - 40);
    return num(88, 2) * alpah1 * alpha2 * num(fcuk);
  }
  static num fck_to_fc(num fck) { return fck / num(14, 1); }

  num Ec, epsilon_0, epsilon_cu;

public:
};
class rebar {
protected:
  using num = typename fundamental::unsigned_number;
  num Es;

public:
};
class single_rebar_rectangle_section : public concrete, rebar {
  using num = typename fundamental::unsigned_number;
  num As, A;
  static num CalcA(num b, num h, num As) {
    num A = b * h;
    if (As > A * num(3, 2))
      A -= As;
    return A;
  }

public:
  single_rebar_rectangle_section(num b, num h, num As, concrete c, rebar s)
      : As(As), A(CalcA(b, h, As)), concrete(c), rebar(s) {}
  num alphaE() const { return this->rebar::Es / this->concrete::Ec; }
  num rho() const { return As / A; }
  num Ntcr() const {
    return this->concrete::Ec * A * (num::exact(1) + alphaE() * rho());
  }
};
} // namespace concrete
} // namespace structure