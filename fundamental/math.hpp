/*
 * UTF-8 encoding
 */
#pragma once
#include "./number.hpp"
#include <vector>
namespace engineering {
namespace fundamental {
constexpr static inline auto str_pi = "3.141592653";
constexpr static inline unsigned_number pi = unsigned_number::to_number(str_pi);
constexpr static inline unsigned_number pi_4 = pi / unsigned_number::exact(4);
#ifdef __cpp_lib_constexpr_vector
constexpr
#endif // __cpp_lib_constexpr_vector
    static inline unsigned_number
    pow(const unsigned_number base, unsigned_number::digits_t expo) {
  if (expo == 0)
    return base / base // unsigned_number(1)
        ;
  bool pos = expo > 0;
  if (!pos)
    expo = -expo;

  // base^(2^0) base^(2^1) ... base^(2^(n-1))
  std::vector<unsigned_number> dynamic = {base};
  while ((1 << dynamic.size()) // pow(2, dynamic.size())
         <= expo)
    dynamic.push_back(dynamic.back() * dynamic.back());
  unsigned_number res = dynamic.back();
  dynamic.pop_back();
  while (!dynamic.empty()) {
    auto ex = 1 << (dynamic.size() - 1) // pow(2, dynamic.size() - 1)
        ;
    if (ex & expo) // ex <= expo
      res *= dynamic.back(), expo -= ex;
    dynamic.pop_back();
  }

  return pos ? res : unsigned_number::exact(1) / res;
}
/*constexpr */ static inline unsigned_number pow(unsigned_number base, unsigned_number expo) {
  // Maclaurin
  // if base <= 1
  //  base^expo = (1 + (base - 1))^expo = (1 + ... + (expo * ... * (expo - k + 1) / k!) * (base - 1)^n + ...)
  // else
  //  base^expo = 1 / (1 / base)^expo
  if (base > unsigned_number::exact(1)) {
    return unsigned_number::exact(1) / pow(unsigned_number::exact(1) / base, expo);
  }
  unsigned_number::rounding_for_digits(base, expo);
  auto i = expo.div_1().as_number();
  unsigned_number res = unsigned_number::exact(1);
  unsigned_number x = unsigned_number::exact(1) - base;
  unsigned_number delta = expo * x;
  unsigned_number::valid_digits_t k = 2;

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
    return std::move(res) * pow(base, i);
  else
    return res;
}
} // namespace fundamental
} // namespace engineering