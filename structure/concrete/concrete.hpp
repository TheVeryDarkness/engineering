/*
 * UTF-8 encoding.
 */
#pragma once
#include "math.hpp"
#include "number.hpp"
#include <optional>
namespace engineering {
namespace structure {
namespace concrete {
using num = typename fundamental::unsigned_number;
using opt = std::optional<num>;
template <typename callback> static inline num fetch_opt(opt &o, callback cb) {
  return o.has_value() ? o.value() : (o = cb(), o.value());
}

// properties
class concrete {
protected:
  static num alpha1(num::valid_number_t fcuk) {
    using namespace fundamental;
    return fcuk <= 50   ? num(76, 2)                 // 0.76
           : fcuk >= 80 ? num(82, 2)                 // 0.82
                        : num(fcuk - 50) * num(2, 3) // (0.82 - 0.76) / (80 - 50) = 0.002
        ;
  }
  static num alpha2(num::valid_number_t fcuk) {
    using namespace fundamental;
    return fcuk <= 40   ? "1.00"_num                  // 1.00
           : fcuk >= 80 ? "0.87"_num                  // 0.87
                        : num(fcuk - 40) * num(32, 4) //(1.00 - 0.87) / (80 - 40) = 0.00325 = 0.0032
        ;
  }
  // p.22 2-4
  // GB 50010-2010 4.1.3
  static num fcuk_to_fck(num::valid_number_t fcuk) { return num(88, 2) * alpha1(fcuk) * alpha2(fcuk) * num(fcuk); }
  // p.22
  static num fck_to_fc(num fck) { return fck / num(14, 1); }

  const num Ec, fc, ft, epsilon_0, epsilon_cu;

public:
  concrete(num Ec, num fc, num ft, num epsilon_0 = num(2, 3), num epsilon_cu = num(3, 4))
      : Ec(Ec), fc(fc), ft(ft), epsilon_0(epsilon_0), epsilon_cu(epsilon_cu) {}
  // GB 50010-2010 4.1.5
  num Gc() const { return (num::exact(4) >> 1) /*40%*/ * Ec; }
  // GB 50010-2010 4.1.5
  num nuc() const { return {2, 1}; }
  // GB 50010-2010 4.1.5
  static num fcuk_to_Ec(num::valid_number_t fcuk) {
    return (num::exact(1) << 5) /* exact 1e5 */ / (num(22, 1) + num(347, 1) / num::exact(fcuk));
  }
  // GB 50010-2010 4.1.8
  static num alpha_c() { return num::exact(1) >> 5; }
  // GB 50010-2010 4.1.8
  // kJ/(m*h*K)
  static num lambda() { return {106, 1}; }
  // GB 50010-2010 4.1.8
  // kJ/(kg*K)
  static num c() { return {96, 2}; }
};
//
const static concrete C15 = {num(220, -2), num(72, 1), num(91, 2)};
const static concrete C20 = {num(255, -2), num(96, 1), num(110, 2)};
const static concrete C25 = {num(280, -2), num(119, 1), num(127, 2)};
const static concrete C30 = {num(300, -2), num(143, 1), num(143, 2)};
const static concrete C35 = {num(315, -2), num(167, 1), num(157, 2)};
const static concrete C40 = {num(325, -2), num(191, 1), num(171, 2)};
const static concrete C45 = {num(335, -2), num(211, 1), num(180, 2)};
const static concrete C50 = {num(345, -2), num(231, 1), num(189, 2)};
const static concrete C55 = {num(355, -2), num(253, 1), num(196, 2)};
const static concrete C60 = {num(360, -2), num(275, 1), num(204, 2)};
const static concrete C65 = {num(365, -2), num(297, 1), num(209, 2)};
const static concrete C70 = {num(370, -2), num(318, 1), num(214, 2)};
const static concrete C75 = {num(375, -2), num(338, 1), num(218, 2)};
const static concrete C80 = {num(380, -2), num(359, 1), num(222, 2)};

// properties
class steel {
protected:
  const num Es, fy;
  const opt fy_, fsu;

public:
  steel(num Es, num fy, opt fy_ = {}, opt fsu = {}) : Es(Es), fy(fy), fy_(fy_), fsu(fsu) {}
};
static const steel HPB300 = {{210, -3}, num(270, 0), num(270, 0)};
static const steel HRB335 = {{200, -3}, num(300, 0), num(300, 0)};
static const steel &HRBF335 = HRB335;
static const steel HRB400 = {{200, -3}, num(360, 0), num(360, 0)};
static const steel &HRBF400 = HRB400;
static const steel &RRB400 = HRB400;
static const steel HRB500 = {{200, -3}, num(435, 0), num(435, 0)};
static const steel &HRBF500 = HRB500;

class rebar {
  const num d, _As;

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
  const num b, h, _A;

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
  const num l;
  using super = longitudinal_rebar_rectangle_section;

public:
  longitudinal_rebar_rectangle_column(num length, longitudinal_rebar_rectangle_section sec) : super(sec), l(length) {}
  static num phi();
  num Ncu() { return phi() * this->super::Ncu(); }
};
class spiral_longitudinal_rebar_rectangle_section : public longitudinal_rebar_rectangle_section {};
} // namespace concrete
} // namespace structure
} // namespace engineering