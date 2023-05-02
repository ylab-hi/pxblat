#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>

#include "cfaToTwoBit.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

PYBIND11_MODULE(_extc, m) {
  m.doc() = "pybind11 example plugin";  // optional module docstring
  m.def("faToTwoBit", &faToTwoBit, "A function to convert fasta to twobit");
}
