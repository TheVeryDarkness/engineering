/*
 * UTF-8 encoding
 */
#pragma once
#include "./number.hpp"
#include <vector>
namespace engineering {
namespace fundamental {
constexpr static inline auto str_pi = "3.14159265358979323846";
constexpr static inline auto str_e = "2.718281828459045";
constexpr static inline auto pi = to_number(str_pi);
constexpr static inline auto pi_4 = pi / unsigned_number::exact(4);
constexpr static inline auto e = to_number(str_e);

constexpr inline unsigned_number exp(unsigned_number x) {
  // Maclaurin
  //  e^x = (1 + ... + x^n / n! + ...)
  auto i = x.div_1().as_number();
  if (i > std::numeric_limits<unsigned_number::valid_digits_t>::max())
    throw std ::overflow_error("Exceeds valid_digits_t's limits.");
  unsigned_number res = unsigned_number::exact(1);
  unsigned_number delta = x;
  unsigned_number::digits_t k = 2;

  const auto min = res.minimal() >> 1;
  while (delta >= min) {
    res -= delta;
    unsigned_number K = unsigned_number::exact(k);
    delta /= K;
    delta *= x;
    ++k;
  }
  if (i)
    return std::move(res) * pow(e, unsigned_number::valid_digits_t(i));
  else
    return res;
}
constexpr inline unsigned_number log(unsigned_number x) {
  if (x < unsigned_number::exact(1))
    throw std::underflow_error("Result is not a positive number.");
  unsigned_number::digits_t times = -1 - x.head_pos_in_digits();
  assert(times > 0);
  x >> times; // 1.xxx

  const unsigned_number t = (x - unsigned_number::exact(1)) / (x + unsigned_number::exact(1));
  auto res = t, delta = t;
  unsigned_number::digits_t k = 1;
  while (delta < res.minimal()) {
    (delta *= t) *= t;
    res += delta / unsigned_number::exact(k * 2 + 1);
  }
  return unsigned_number::exact(2) * res;
}
constexpr inline unsigned_number pow(unsigned_number base, unsigned_number expo) {
  // Maclaurin
  // if base <= 1
  //  base^expo = (1 + (base - 1))^expo = (1 + ... + (expo * ... * (expo - k + 1) / k!) * (base - 1)^n + ...)
  // else
  //  base^expo = 1 / (1 / base)^expo
  if (base.head_pos_in_digits() != 0) {
    unsigned_number::digits_t times = base.head_pos_in_digits();
    base <<= times;
    // (base * 10^times / 10^times)^expo = (base * 10^times)^expo / 0.1^expo^times
    return pow(base, expo) / pow(pow(unsigned_number::exact(1) >> 1, expo), -times);
  }
  unsigned_number::rounding_for_digits(base, expo);
  auto i = expo.div_1().as_number();
  if (i > std::numeric_limits<unsigned_number::valid_digits_t>::max())
    throw std ::overflow_error("Exceeds valid_digits_t's limits.");
  unsigned_number res = unsigned_number::exact(1);
  unsigned_number x = unsigned_number::exact(1) - base;
  unsigned_number delta = expo * x;
  unsigned_number::digits_t k = 2;

  const auto min = base.minimal() >> 1;
  while (delta >= min) {
    res -= delta;
    unsigned_number K = unsigned_number::exact(k);
    delta *= (unsigned_number::exact(k - 1) - expo);
    delta /= K;
    delta *= x;
    ++k;
  }
  if (i)
    return std::move(res) * pow(base, unsigned_number::valid_digits_t(i));
  else
    return res;
}
} // namespace fundamental
} // namespace engineering