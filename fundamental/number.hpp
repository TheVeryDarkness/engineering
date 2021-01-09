#pragma once
#include <cassert>
#include <cstdint>
#include <limits>
#include <string>
#include <string_view>
namespace structure {
namespace fundamental {
// 有效数字需要足够宽，以防止乘法上溢
template <                                   //
    typename valid_number_t = std::intmax_t, // 有效数值的类型
    typename digits_t = std::int_fast8_t,    // 小数点位数的类型
    digits_t max_valid_digits = 4            // 有效位数
    >
class unsigned_number {
  valid_number_t valid_number;
  digits_t decimal_digits, digits;
  constexpr static digits_t max_digits10 =
      std::numeric_limits<valid_number_t>::digits10;
  template <typename Ty, Ty exp> constexpr static Ty pow10() noexcept {
    Ty p = 1;
    for (Ty i = 1; i < exp; ++i)
      p *= 10;
    return p;
  }
  template <typename Ty> constexpr static Ty pow10(Ty exp) noexcept {
    Ty p = 1;
    for (Ty i = 1; i < exp; ++i)
      p *= 10;
    return p;
  }
  constexpr static valid_number_t max() noexcept {
    return pow10<digits_t, max_valid_digits>();
  }
  static_assert(max_valid_digits <= max_digits10 / 2, "Unsafe. May Overflow.");
  static digits_t count_digits(valid_number_t num) {
    digits_t d = 0;
    while (num > 0)
      num /= 10, ++d;
    return d;
  }
  // digits应该大于0
  void div_10_for(digits_t digits) {
    assert(digits > 0);
    valid_number /= pow10(digits);
  }
  void adjust_valid_digits() {
    digits_t over = max_valid_digits - count_digits(valid_number);
    if (over > 0) {
      div_10_for(over);
      decimal_digits -= over;
    }
  }

public:
  unsigned_number(valid_number_t vn, digits_t dd) noexcept
      : valid_number(vn), decimal_digits(dd), digits(count_digits(vn)) {}
  unsigned_number &operator*=(const unsigned_number &that) {
    valid_number *= that.valid_number;
    decimal_digits += that.decimal_digits;
    adjust_valid_digits();
    return *this;
  }
  unsigned_number &operator/=(const unsigned_number &that) {
    valid_number *= pow10(that.digits);
    valid_number /= that.valid_number;
    decimal_digits -= that.decimal_digits;
    adjust_valid_digits();
    return *this;
  }
  std::string to_string() const {
    std::string s = std::to_string(valid_number);
    if (digits <= decimal_digits) {
      using namespace std::literals;
      std::string_view pre = "0."sv;
      s.insert(s.cbegin(), pre.begin(), pre.end());
      auto dif = decimal_digits - digits;
      s.insert(s.cbegin() + 2, dif, '0');
    } else if (0 < decimal_digits) {
      s.insert(s.cbegin() + (digits - decimal_digits), '.');
    } else {
      s.insert(s.cbegin() + 1, '.');
      s.push_back('e');
      s += std::to_string(digits - decimal_digits - 1);
    }
    return s;
  }
};
} // namespace fundamental
} // namespace structure