/*
 * UTF-8 encoding.
 */
#pragma once
#include "../fundamental/math.hpp"
#include "../fundamental/number.hpp"
#include <optional>
namespace structure {
namespace concrete {
using num = typename fundamental::unsigned_number;
using opt = std::optional<num>;
template <typename callback> static inline num fetch_opt(opt &o, callback cb) {
  return o.has_value() ? o.value() : (o = cb(), o.value());
}
class concrete {
protected:
  // p.22 2-4
  static num fcuk_to_fck(num::valid_number_t fcuk) {
    using namespace fundamental;
    num alpah1 = fcuk <= 50 ? "0.76"_num                                // 0.76
                            : fcuk >= 80 ? "0.82"_num                   // 0.82
                                         : num(fcuk - 50) * "0.002"_num // (0.82 - 0.76) / (80 - 50)
        ;
    num alpha2 = fcuk <= 40 ? "1.00"_num              // 1.00
                            : fcuk >= 80 ? "0.87"_num // 0.87
                                         : num(100 - 87, 2) / num(80 - 40, 2) * num(fcuk - 40);
    return num(88, 2) * alpah1 * alpha2 * num(fcuk);
  }
  // p.22
  static num fck_to_fc(num fck) { return fck / num(14, 1); }

  num Ec, fc, ft, epsilon_0, epsilon_cu;

public:
  concrete(num Ec, num fc, num ft, num epsilon_0 = num(2, 3), num epsilon_cu = num(3, 4))
      : Ec(Ec), fc(fc), ft(ft), epsilon_0(epsilon_0), epsilon_cu(epsilon_cu) {}
};
class steel {
protected:
  num Es, fy;
  opt fy_, fsu;

public:
  steel(num Es, num fy, opt fy_ = {}, opt fsu = {}) : Es(Es), fy(fy), fy_(fy_), fsu(fsu) {}
};

class rebar {
  num d, _As;

public:
  rebar(num d) : d(d), _As(fundamental::pi_4 * d * d) {}
  num As() const { return _As; }
};

// "Virtual" Base
class section {
protected:
  section() = default;
  static num CalcA(num A, num As) {
    if (As > A * num(3, 2) /*0.03*/)
      A -= As;
    return A;
  }
};
class rectangle : section {
  num b, h, _A;

protected:
  static num CalcA(num b, num h, num As) { return section::CalcA(b * h, As); }

public:
  rectangle(num b, num h, num As) : b(b), h(h), _A(CalcA(b, h, As)) {}
  num A() const { return _A; }
};

class longitudinal_rebar_rectangle_section : public concrete, rebar, rectangle, steel {
  mutable opt _alphaE, _rho;

public:
  longitudinal_rebar_rectangle_section(rebar r, rectangle rs, concrete c, steel s)
      : concrete(c), rebar(r), rectangle(rs), steel(s) {}
  const concrete &c() const { return *this; }
  const steel &r() const { return *this; }
  num alphaE() const {
    return fetch_opt(_alphaE, [this] { return Es / Ec; });
  }
  num rho() const {
    return fetch_opt(_rho, [this] { return As() / A(); });
  }
  // p.49 4-5
  num Ntcr() const { return ft * A() * (num::exact(1) + alphaE() * rho()); }
  // p.49 4-7
  num Ntu() const { return fy * As(); }
  // p.53 4-20
  num Ncu() const { return fc * A() + fy_.value() * As(); }
  // p.53 4-25
  num sigma_s2(num Nc, num nu, num Ct) {
    return Nc * (num::exact(1) + Ct) / (num::exact(1) + nu / alphaE() / rho()) / As();
  }
  // p.54 4-26
  num sigma_c2(num Nc, num nu, num Ct) {
    return Nc / A() *
           (num::exact(1) -
            alphaE() * (num::exact(1) + Ct) * As() / nu / A() / (num::exact(1) + alphaE() / nu * rho()));
  }
};
class longitudinal_rebar_rectangle_column : public longitudinal_rebar_rectangle_section {
  num l;
  using super = longitudinal_rebar_rectangle_section;

public:
  longitudinal_rebar_rectangle_column(num length, longitudinal_rebar_rectangle_section sec) : l(length), super(sec) {}
  static num phi();
  num Ncu() { return phi() * this->super::Ncu(); }
};
class spiral_longitudinal_rebar_rectangle_section : public longitudinal_rebar_rectangle_section {};
} // namespace concrete
} // namespace structure