#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>

#include "faToTwoBit.hpp"
#include "gfServer.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

PYBIND11_MODULE(_extc, m) {
  m.doc() = "pybind11 plugin";  // optional module docstring
  m.def("faToTwoBit", &faToTwoBit, py::arg("inFiles"), py::arg("outFile"), py::arg("noMask") = false,
        py::arg("stripVersion") = false, py::arg("ignoreDups") = false, py::arg("useLong") = false,
        "A function that converts FASTA files to twoBit files: \n "
        "long:     use 64-bit offsets for index \n"
        "noMask: Ignore lower-case masking in fa file.\n"
        "stripVersion:  Strip off version number after . \n"
        "ignoreDups:    Convert first sequence only if there are duplicate "
        "sequence names.\n");

  py::class_<gfServerOption>(m, "gfServerOption")
      .def(py::init<>())
      .def_readwrite("can_stop", &gfServerOption::canStop)
      .def_readwrite("log", &gfServerOption::log)
      .def_readwrite("log_facility", &gfServerOption::logFacility)
      .def_readwrite("mask", &gfServerOption::mask)
      .def_readwrite("max_aa_size", &gfServerOption::maxAaSize)
      .def_readwrite("max_dna_hits", &gfServerOption::maxDnaHits)
      .def_readwrite("max_gap", &gfServerOption::maxGap)
      .def_readwrite("max_nt_size", &gfServerOption::maxNtSize)
      .def_readwrite("max_trans_hits", &gfServerOption::maxTransHits)
      .def_readwrite("min_match", &gfServerOption::minMatch)
      .def_readwrite("rep_match", &gfServerOption::repMatch)
      .def_readwrite("seq_log", &gfServerOption::seqLog)
      .def_readwrite("ip_log", &gfServerOption::ipLog)
      .def_readwrite("debug_log", &gfServerOption::debugLog)
      .def_readwrite("tile_size", &gfServerOption::tileSize)
      .def_readwrite("step_size", &gfServerOption::stepSize)
      .def_readwrite("trans", &gfServerOption::trans)
      .def_readwrite("syslog", &gfServerOption::syslog)
      .def_readwrite("per_seq_max", &gfServerOption::perSeqMax)
      .def_readwrite("no_simp_rep_mask", &gfServerOption::noSimpRepMask)
      .def_readwrite("index_file", &gfServerOption::indexFile)
      .def_readwrite("timeout", &gfServerOption::timeout)
      .def_readwrite("genome", &gfServerOption::genome)
      .def_readwrite("genome_data_dir", &gfServerOption::genomeDataDir)
      .def_readwrite("allow_one_mismatch", &gfServerOption::allowOneMismatch);
}
