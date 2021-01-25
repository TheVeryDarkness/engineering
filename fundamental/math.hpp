/*
 * UTF-8 encoding
 */
#pragma once
#include "./number.hpp"
#include <vector>
namespace engineering {
constexpr static inline auto str_pi = "3.141592653";
constexpr static inline auto pi = fundamental::unsigned_number::to_number(str_pi);
constexpr static inline auto pi_4 = pi / fundamental::unsigned_number::exact(4);
namespace fundamental {
} // namespace fundamental
} // namespace engineering