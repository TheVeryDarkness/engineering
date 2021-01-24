add_executable("number_test" "tests/number_test.cpp")
add_executable("math_test" "tests/math_test.cpp")
add_test(NAME "number_test" COMMAND "number_test")
add_test(NAME "math_test" COMMAND "math_test")