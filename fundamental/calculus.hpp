/*
 *UTF-8 encoding
 */
#pragma once
#include <map>
#include <set>
#include <string>
#include <vector>
namespace engineering {
namespace fundamental {
using name_t = std::string;
struct _module {
  std::map<name_t, nullptr_t> functions;
};
static inline std::set<_module> being_used;
class node {
  name_t name;
  std::vector<node> parameters;
};
class item {
  std::set<node> product;
};
class expression {
  std::set<item> sum;
};
} // namespace fundamental
} // namespace engineering