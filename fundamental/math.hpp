/*
 * UTF-8 encoding
 */
#pragma once
#include "number.hpp"
namespace structure {
namespace fundamental {
constexpr static inline auto str_pi = "3.141592653";
const static inline unsigned_number pi = operator""_num(str_pi, unsigned_number::max_digits10 + 1);
const static inline unsigned_number pi_4 = pi / unsigned_number::exact(4);
} // namespace fundamental
} // namespace structure