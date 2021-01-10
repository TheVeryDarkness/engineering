#pragma once
#include <cassert>
#include <cstdint>
#include <limits>
#include <string>
#include <string_view>
namespace structure {
namespace fundamental {
// 有效数字需要足够宽，以防止乘法上溢
template <                                    //
    typename valid_number_t = std::uintmax_t, // 有效数值的类型
    typename digits_t = std::int_fast8_t,     // 小数点位数的类型
    digits_t max_valid_digits = 4             // 有效位数，必须为正
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
  static_assert(max_valid_digits > 0, "Not a number.");
  static digits_t count_digits(valid_number_t num) {
    digits_t d = 0;
    while (num > 0)
      num /= 10, ++d;
    return d;
  }
  // 由于暂无四舍六入五凑偶的优雅实现，
  // 暂时使用四舍五入。
  constexpr static void round_div(valid_number_t &de,
                                  valid_number_t no) noexcept {
    (de += no / 2) /= no;
  }
  // digits应该大于0
  void div_10_for(digits_t digits) {
    assert(digits > 0);
    round_div(valid_number, pow10(digits));
  }
  void adjust_valid_digits() {
    digits_t over = max_valid_digits - count_digits(valid_number);
    if (over > 0) {
      div_10_for(over);
      decimal_digits -= over;
    }
  }
  valid_number_t approximate(const unsigned_number &that) noexcept {
    assert(that.decimal_digits >= decimal_digits);
    valid_number_t res = that.valid_number;
    round_div(res, pow10(that.decimal_digits - decimal_digits));
    return res;
  }

public:
  unsigned_number(valid_number_t vn, digits_t dd) noexcept
      : valid_number(vn), decimal_digits(dd), digits(count_digits(vn)) {}
  unsigned_number(const unsigned_number &) noexcept = default;
  unsigned_number &operator+=(const unsigned_number &that) {
    valid_number += approximate(that);
    adjust_valid_digits();
    return *this;
  }
  unsigned_number &operator-=(const unsigned_number &that) {
    valid_number -= approximate(that);
    adjust_valid_digits();
    return *this;
  }
  unsigned_number &operator*=(const unsigned_number &that) {
    valid_number *= that.valid_number;
    decimal_digits += that.decimal_digits;
    adjust_valid_digits();
    return *this;
  }
  unsigned_number &operator/=(const unsigned_number &that) {
    valid_number *= pow10(that.digits);
    round_div(valid_number, that.valid_number);
    (decimal_digits += that.digits) -= that.decimal_digits;
    adjust_valid_digits();
    return *this;
  }
  std::string to_string() const {
    std::string s = std::to_string(valid_number);
    s.insert(s.cbegin() + 1, '.');
    s.push_back('e');
    s += std::to_string(digits - decimal_digits - 1);
    return s;
  }
};
} // namespace fundamental
} // namespace structure