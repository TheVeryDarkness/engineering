/*
 * UTF-8 encoding.
 */
#pragma once
#include <cassert>
#include <cstdint>
#include <iosfwd>
#include <limits>
#include <string>
#include <string_view>
namespace structure {
namespace fundamental {
template <typename Ty> Ty string_to_integer(const char *s) {
  if constexpr (std::is_same_v<Ty, int>)
    return std::stoi(s);
  if constexpr (std::is_same_v<Ty, long>)
    return std::stol(s);
  if constexpr (std::is_same_v<Ty, long long>)
    return std::stoll(s);
  if constexpr (std::is_same_v<Ty, unsigned long>)
    return std::stoul(s);
  if constexpr (std::is_same_v<Ty, unsigned long long>)
    return std::stoull(s);
  if constexpr (std::is_same_v<Ty, unsigned int>) // No matched function
    return std::stoul(s);
  throw;
}
class unsigned_number {
public:
  using valid_number_t = std::uint_fast32_t;
  using digits_t = std::int_fast8_t;
  constexpr static digits_t max_digits10 =
      (std::numeric_limits<valid_number_t>::digits10 - 1) / 2;

private:
  valid_number_t valid_number;
  digits_t tail_pos; // positive for decimal, negative for post-zeros
  digits_t digits;   // valid digits, positive
  constexpr static digits_t literal_1 = 1;
  constexpr static valid_number_t pow10(valid_number_t exp) noexcept {
    valid_number_t p = 1;
    for (valid_number_t i = 0; i < exp; ++i)
      p *= 10;
    return p;
  }
  constexpr static digits_t count_digits(valid_number_t num) {
    digits_t d = 0;
    while (num > 0)
      num /= 10, ++d;
    return d;
  }
  bool digits_legal() const { return digits == count_digits(valid_number); }
  [[nodiscard]] constexpr static std::pair<valid_number_t, valid_number_t>
  builtin_div(valid_number_t de, valid_number_t no) noexcept {
    return {de / no, de % no};
  }
  constexpr static void round_div(valid_number_t &de,
                                  valid_number_t no) noexcept {
    auto [_1, _2] = builtin_div(de + no / 2, no);
    if (no % 2 == 0) { // Only when nominator is even,
      if (_2 == 0 &&   // look right, just half of nominator
          _1 % 2 == 1) // look left, the last digit is odd
        _1 -= 1;
    }
    de = _1;
  }
  valid_number_t as_if_remove_decimal(digits_t d) const {
    valid_number_t valid_number = this->valid_number;
    if (d < 0)
      throw;
    if (d == 0)
      return valid_number;
    if (d > digits)
      return 0;
    auto [_1, _2] = builtin_div(valid_number, pow10(d - literal_1));
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
    if (now < digits)
      digits = now;
    assert(digits_legal());
  }
  void adjust_tail_to(const unsigned_number &that) {
    remove_decimal(tail_pos - that.tail_pos);
    assert(tail_pos == that.tail_pos);
  }
  void adjust_digits_to(const unsigned_number &that) {
    remove_decimal(digits - that.digits);
    assert(count_digits(digits) == that.digits);
  }
  valid_number_t approximate_for_tail(const unsigned_number &that) const {
    assert(that.tail_pos >= tail_pos);
    if (that.tail_pos - tail_pos > that.digits)
      return 0;
    else
      return that.as_if_remove_decimal(that.tail_pos - tail_pos);
  }
  valid_number_t approximate_for_digits(const unsigned_number &that) const {
    assert(that.digits >= digits);
    return that.as_if_remove_decimal(that.digits - digits);
  }

public:
  unsigned_number(valid_number_t vn, digits_t decimal) noexcept
      : valid_number(vn), tail_pos(decimal), digits(count_digits(vn)) {
    assert(digits <= max_digits10);
  }
  explicit unsigned_number(valid_number_t vn) noexcept
      : unsigned_number(vn, 0) {}
  static unsigned_number exact(valid_number_t num) {
    digits_t d = count_digits(num);
    if (d > max_digits10)
      throw;
    num *= pow10(max_digits10 - d);
    return unsigned_number(num, max_digits10 - d);
  }
  unsigned_number(const unsigned_number &) noexcept = default;
  unsigned_number &rounding(digits_t d) {
    assert(d > 0);
    if (d <= 0)
      return *this;
    if (d >= digits)
      throw;
    remove_decimal(d);
    return *this;
  }
  bool operator==(const unsigned_number &that) const noexcept {
    return valid_number == that.valid_number && tail_pos == that.tail_pos;
  }
  bool operator!=(const unsigned_number &that) const noexcept {
    return !(*this == that);
  }
  bool operator<(const unsigned_number &that) const {
    if (that.tail_pos < tail_pos)
      if (digits - tail_pos > that.digits - that.tail_pos)
        return true;
      else if (digits - tail_pos < that.digits - that.tail_pos)
        return false;
      else
        return valid_number < that.valid_number;
    else
      return valid_number < approximate_for_tail(that);
  }
  bool operator>(const unsigned_number &that) const { return that < *this; }
  bool operator<=(const unsigned_number &that) const { return !(that < *this); }
  bool operator>=(const unsigned_number &that) const { return !(*this < that); }
  unsigned_number &operator+=(const unsigned_number &that) {
    if (that.tail_pos >= tail_pos)
      valid_number += approximate_for_tail(that);
    else
      adjust_tail_to(that), valid_number += that.valid_number;
    adjust_valid_digits();
    return *this;
  }
  unsigned_number &operator-=(const unsigned_number &that) {
    assert(*this >= that);
    if (that.tail_pos >= tail_pos)
      valid_number -= approximate_for_tail(that);
    else
      adjust_tail_to(that), valid_number -= that.valid_number;
    adjust_valid_digits();
    return *this;
  }
  unsigned_number &operator*=(const unsigned_number &that) {
    if (that.digits >= digits) {
      valid_number *= approximate_for_digits(that);
      tail_pos += (that.tail_pos - (that.digits - digits));
    } else {
      adjust_digits_to(that);
      valid_number *= that.valid_number;
      tail_pos += that.tail_pos;
    }
    adjust_valid_digits();
    return *this;
  }
  unsigned_number &operator/=(const unsigned_number &that) {
    if (that.digits >= digits) {
      valid_number *= pow10(digits);
      round_div(valid_number, approximate_for_digits(that));
      // tail_pos += digits;
      // tail_pos -= that.tail_pos - (that.digits - digits);
      (tail_pos += that.digits) -= that.tail_pos;
    } else {
      adjust_digits_to(that);
      valid_number *= pow10(that.digits);
      round_div(valid_number, that.valid_number);
      // tail_pos += that.digits;
      // tail_pos -= that.tail_pos;
      (tail_pos += that.digits) -= that.tail_pos;
    }
    adjust_valid_digits();
    return *this;
  }
  unsigned_number operator+(const unsigned_number &that) const & {
    return unsigned_number(*this) += that;
  }
  unsigned_number operator-(const unsigned_number &that) const & {
    return unsigned_number(*this) -= that;
  }
  unsigned_number operator*(const unsigned_number &that) const & {
    return unsigned_number(*this) *= that;
  }
  unsigned_number operator/(const unsigned_number &that) const & {
    return unsigned_number(*this) /= that;
  }
  unsigned_number operator+(const unsigned_number &that) && {
    return *this += that;
  }
  unsigned_number operator-(const unsigned_number &that) && {
    return *this -= that;
  }
  unsigned_number operator*(const unsigned_number &that) && {
    return *this *= that;
  }
  unsigned_number operator/(const unsigned_number &that) && {
    return *this /= that;
  }

  std::string to_string() const {
    std::string s = std::to_string(valid_number);
    s.insert(s.cbegin() + 1, '.');
    s.push_back('e');
    s += std::to_string(digits - tail_pos - literal_1);
    return s;
  }
};
static inline unsigned_number operator""_e_1(unsigned long long num) {
  using vn_t = unsigned_number::valid_number_t;
  assert(num <= std ::numeric_limits<vn_t>::max());
  return unsigned_number(static_cast<vn_t>(num), 1);
}
static inline unsigned_number::valid_number_t operator""_num(char c) {
  if (c < '0' || c > '9')
    throw;
  return c - '0';
}
// Support formar:
// xxx.xxx
// xxx
// xxxey
// xxxEy
static inline unsigned_number operator""_num(const char *s) {
  using vn_t = unsigned_number::valid_number_t;
  vn_t vn = 0;
  bool find_dot = false;
  unsigned_number::digits_t dec = 0;
  while (*s) {
    auto c = *s;
    ++s;
    if ('0' <= c && c <= '9')
      (vn *= 10) += operator""_num(c);
    else if (c == '.') {
      find_dot = true;
      continue;
    } else if (c == 'e' || c == 'E') {
      if (*s) {
        auto n = string_to_integer<vn_t>(s);
        dec -= n;
      }
      return unsigned_number(vn, dec);
    }
    if (find_dot)
      ++dec;
  }
  return unsigned_number(vn, dec);
}
static inline unsigned_number operator""_num(const char *s, std::size_t) {
  return operator""_num(s);
}
std::ostream &operator<<(std::ostream &o, const unsigned_number &n) {
  return o << n.to_string();
}
} // namespace fundamental
} // namespace structure