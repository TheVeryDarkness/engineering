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
constexpr static inline auto e = to_number(str_e);

constexpr static inline auto ln2 = to_number("0.693147180559945");
constexpr static inline auto ln10 = to_number("2.302585092994046");

constexpr static inline auto pi_4 = pi / unsigned_number::exact(4);

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
    res += delta;
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
  const unsigned_number _1 = unsigned_number::exact(1);
  const unsigned_number _2 = unsigned_number::exact(2);
  unsigned_number::digits_t times = 0;
  // Convert x to (0.5, 1]
  while (x > _1) {
    x /= _2;
    ++times;
  }

  const unsigned_number t = unsigned_number::exact(1) - x;
  auto res = t, delta = t;
  unsigned_number::digits_t k = 2;
  while (delta >= res.minimal()) {
    delta *= t;
    res += delta / unsigned_number::exact(k);
    ++k;
  }
  return unsigned_number::exact(times) * ln2 - res;
}
constexpr inline unsigned_number pow(unsigned_number base, unsigned_number expo) {
  auto i = expo.div_1().as_number();
  if (i > std::numeric_limits<unsigned_number::valid_digits_t>::max())
    throw std ::overflow_error("Exceeds valid_digits_t's limits.");
  // Maclaurin
  // if base <= 1
  //  base^expo = (1 + (base - 1))^expo = (1 + ... + (expo * ... * (expo - k + 1) / k!) * (base - 1)^n + ...)
  // else
  //  base^expo = 1 / (1 / base)^expo
  auto small = [&base, &expo]() {
    if (base < unsigned_number::exact(1)) {
      auto &&inv_base = unsigned_number::exact(1) / base;
      auto &&log_inv_base = log(inv_base);
      auto &&new_expo = std::move(log_inv_base) * expo;
      auto &&inv_res = exp(new_expo);
      return unsigned_number::exact(1) / std::move(inv_res);
    } else
      return exp(log(base) * expo);
  }();
  return small * pow(base, unsigned_number::valid_digits_t(i));
}
} // namespace fundamental
} // namespace engineering