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
  // p.22 2-4
  static num fcuk_to_fck(num::valid_number_t fcuk) {
    using namespace fundamental;
    num alpah1 = fcuk <= 50
                     ? "0.76"_num              // 0.76
                     : fcuk >= 80 ? "0.82"_num // 0.82
                                  : num(fcuk - 50) *
                                        "0.002"_num // (0.82 - 0.76) / (80 - 50)
        ;
    num alpha2 = fcuk <= 40 ? "1.00"_num              // 1.00
                            : fcuk >= 80 ? "0.87"_num // 0.87
                                         : num(100 - 87, 2) / num(80 - 40, 2) *
                                               num(fcuk - 40);
    return num(88, 2) * alpah1 * alpha2 * num(fcuk);
  }
  // p.22
  static num fck_to_fc(num fck) { return fck / num(14, 1); }

  num Ec, fc, ft, epsilon_0, epsilon_cu;

public:
  concrete(num Ec, num fc, num ft, num epsilon_0 = num(2, 3),
           num epsilon_cu = num(3, 4))
      : Ec(Ec), fc(fc), ft(ft), epsilon_0(epsilon_0), epsilon_cu(epsilon_cu) {}
};
class rebar {
protected:
  using num = typename fundamental::unsigned_number;
  num Es, fy, fsu;

public:
  rebar(num Es, num fy, num fsu) : Es(Es), fy(fy), fsu(fsu) {}
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
    return this->concrete::ft * A * (num::exact(1) + alphaE() * rho());
  }
};
} // namespace concrete
} // namespace structure