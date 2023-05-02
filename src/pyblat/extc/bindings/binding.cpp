#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>

#include "faToTwoBit.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

PYBIND11_MODULE(_extc, m) {
  m.doc() = "pybind11 plugin";  // optional module docstring
  m.def("faToTwoBit", &faToTwoBit, py::arg("inFiles"), py::arg("outFile"),
        py::arg("noMask") = false, py::arg("stripVersion") = false,
        py::arg("ignoreDups") = false, py::arg("useLong") = false,
        "A function that converts FASTA files to twoBit files: \n "
        "long:     use 64-bit offsets for index \n"
        "noMask: Ignore lower-case masking in fa file.\n"
        "stripVersion:  Strip off version number after . \n"
        "ignoreDups:    Convert first sequence only if there are duplicate "
        "sequence names.\n");
}
