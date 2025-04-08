#include <pybind11/pybind11.h>

namespace py = pybind11;

#include <iostream>

int adder(int num1, int num2) {
    int sum = num1 + num2;
    return sum;
}
PYBIND11_MODULE(example, m) {
    m.def("add", &adder, "A function that adds two numbers");
}

