/*
 * UTF-8 encoding.
 */
#pragma once
#include <cassert>
#include <cstdint>
#include <limits>
#include <string>
#include <string_view>
namespace structure {
namespace fundamental {
// 有效数字需要足够宽，以防止乘法上溢
class unsigned_number {
public:
  using valid_number_t = std::uint_fast32_t; // 有效数值的类型
  using digits_t = std::int_fast8_t;         // 小数点位数的类型
private:
  valid_number_t valid_number;
  digits_t tail_pos; // 正表示小数，负表示后缀0
  digits_t digits;   // 有效位数，为正。仅用于加速。
  constexpr static digits_t literal_1 = 1;
  constexpr static digits_t max_digits10 =
      (std::numeric_limits<valid_number_t>::digits10 - 1) / 2;
  template <typename Ty> constexpr static Ty pow10(Ty exp) noexcept {
    Ty p = 1;
    for (Ty i = 1; i < exp; ++i)
      p *= 10;
    return p;
  }
  constexpr static digits_t count_digits(valid_number_t num) {
    digits_t d = 0;
    while (num > 0)
      num /= 10, ++d;
    return d;
  }
  [[nodiscard]] constexpr static std::pair<valid_number_t, valid_number_t>
  builtin_div(valid_number_t de, valid_number_t no) noexcept {
    return {de / no, de % no};
  }
  constexpr static void round_div(valid_number_t &de,
                                  valid_number_t no) noexcept {
    if (no % 2 == 0) { // 除数是偶数才可能出现余数为除数一半的情况
      auto [_1, _2] = builtin_div(de + no / 2, no);
      if (_2 == 0 &&   // 看右，余数恰为除数一半
          _1 % 2 == 1) // 看左，最后一位为奇数，进位无效。
        _1 -= 1;
    }
  }
  valid_number_t as_if_remove_decimal(digits_t d) const {
    valid_number_t valid_number = this->valid_number;
    if (d <= 0 || d > digits)
      throw;
    auto [_1, _2] = builtin_div(valid_number, pow10<digits_t>(d - literal_1));
    valid_number = _1 / 10;
    if (_1 % 10 > 5 || (_1 % 10 == 5 && _2))
      valid_number += 1;
    return valid_number;
  }
  void remove_decimal(digits_t d) {
    valid_number = as_if_remove_decimal(d);
    tail_pos -= d;
  }
  void adjust_valid_digits() {
    auto now = count_digits(valid_number);
    if (now > digits)
      remove_decimal(now - digits);
  }

public:
  unsigned_number(valid_number_t vn, digits_t decimal) noexcept
      : valid_number(vn), tail_pos(decimal), digits(count_digits(vn)) {
    assert(digits < max_digits10);
  }
  // 假定全为有效数字且无小数
  explicit unsigned_number(valid_number_t vn) noexcept
      : unsigned_number(vn, 0) {}
  unsigned_number(const unsigned_number &) noexcept = default;
  valid_number_t approximate(const unsigned_number &that) noexcept {
    assert(that.tail_pos >= tail_pos);
    if (that.tail_pos - tail_pos > that.digits)
      return 0;
    else
      return as_if_remove_decimal(that.tail_pos - tail_pos);
  }
  // 舍入位数，为正，不能超过有效位数
  unsigned_number &rounding(digits_t d) {
    assert(d > 0);
    if (d <= 0)
      return *this;
    if (d >= digits)
      throw;
    remove_decimal(d);
    return *this;
  }
  bool operator<(const unsigned_number &that) {
    if (that.tail_pos < tail_pos)
      if (digits - tail_pos > that.digits - that.tail_pos)
        return true;
      else if (digits - tail_pos < that.digits - that.tail_pos)
        return false;
      else
        return valid_number < that.valid_number;
    else
      return valid_number < approximate(that);
  }
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
    tail_pos += that.tail_pos;
    adjust_valid_digits();
    return *this;
  }
  unsigned_number &operator/=(const unsigned_number &that) {
    valid_number *= pow10(that.digits);
    round_div(valid_number, that.valid_number);
    (tail_pos += that.digits) -= that.tail_pos;
    adjust_valid_digits();
    return *this;
  }
  unsigned_number operator+(const unsigned_number &that) const {
    return unsigned_number(*this) += that;
  }
  unsigned_number operator-(const unsigned_number &that) const {
    return unsigned_number(*this) -= that;
  }
  unsigned_number operator*(const unsigned_number &that) const {
    return unsigned_number(*this) *= that;
  }
  unsigned_number operator/(const unsigned_number &that) const {
    return unsigned_number(*this) /= that;
  }
  std::string to_string() const {
    std::string s = std::to_string(valid_number);
    s.insert(s.cbegin() + 1, '.');
    s.push_back('e');
    s += std::to_string(digits - tail_pos - literal_1);
    return s;
  }
};
} // namespace fundamental
} // namespace structure