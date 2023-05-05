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

  py::class_<gfServerOption, std::shared_ptr<gfServerOption>>(m, "gfServerOption")
      .def(py::init<>([]() { return new gfServerOption(); }))
      .def(py::init([](gfServerOption &o) { return new gfServerOption(o); }))
      .def_readwrite("canStop", &gfServerOption::canStop)
      .def_readwrite("log", &gfServerOption::log)
      .def_readwrite("logFacility", &gfServerOption::logFacility)
      .def_readwrite("mask", &gfServerOption::mask)
      .def_readwrite("maxAaSize", &gfServerOption::maxAaSize)
      .def_readwrite("maxDnaHits", &gfServerOption::maxDnaHits)
      .def_readwrite("maxGap", &gfServerOption::maxGap)
      .def_readwrite("maxNtSize", &gfServerOption::maxNtSize)
      .def_readwrite("maxTransHits", &gfServerOption::maxTransHits)
      .def_readwrite("minMatch", &gfServerOption::minMatch)
      .def_readwrite("repMatch", &gfServerOption::repMatch)
      .def_readwrite("seqLog", &gfServerOption::seqLog)
      .def_readwrite("ipLog", &gfServerOption::ipLog)
      .def_readwrite("debugLog", &gfServerOption::debugLog)
      .def_readwrite("tileSize", &gfServerOption::tileSize)
      .def_readwrite("stepSize", &gfServerOption::stepSize)
      .def_readwrite("trans", &gfServerOption::trans)
      .def_readwrite("syslog", &gfServerOption::syslog)
      .def_readwrite("perSeqMax", &gfServerOption::perSeqMax)
      .def_readwrite("noSimpRepMask", &gfServerOption::noSimpRepMask)
      .def_readwrite("indexFile", &gfServerOption::indexFile)
      .def_readwrite("timeout", &gfServerOption::timeout)
      .def_readwrite("genome", &gfServerOption::genome)
      .def_readwrite("genomeDataDir", &gfServerOption::genomeDataDir)
      .def_readwrite("allowOneMismatch", &gfServerOption::allowOneMismatch)
      .def("withCanStop", &gfServerOption::withCanStop, py::arg("withCanStop"))
      .def("withLog", &gfServerOption::withLog, py::arg("withLog"))
      .def("withLogFacility", &gfServerOption::withLogFacility, py::arg("withLogFacility"))
      .def("withMask", &gfServerOption::withMask, py::arg("withMask"))
      .def("withMaxAaSize", &gfServerOption::withMaxAaSize, py::arg("withMaxAaSize"))
      .def("withMaxDnaHits", &gfServerOption::withMaxDnaHits, py::arg("withMaxDnaHits"))
      .def("withMaxGap", &gfServerOption::withMaxGap, py::arg("withMaxGap"))
      .def("withMaxNtSize", &gfServerOption::withMaxNtSize, py::arg("withMaxNtSize"))
      .def("withMaxTransHits", &gfServerOption::withMaxTransHits, py::arg("withMaxTransHits"))
      .def("withMinMatch", &gfServerOption::withMinMatch, py::arg("withMinMatch"))
      .def("withRepMatch", &gfServerOption::withRepMatch, py::arg("withRepMatch"))
      .def("withSeqLog", &gfServerOption::withSeqLog, py::arg("withSeqLog"))
      .def("withIpLog", &gfServerOption::withIpLog, py::arg("withIpLog"))
      .def("withDebugLog", &gfServerOption::withDebugLog, py::arg("withDebugLog"))
      .def("withTileSize", &gfServerOption::withTileSize, py::arg("withTileSize"))
      .def("withStepSize", &gfServerOption::withStepSize, py::arg("withStepSize"))
      .def("withTrans", &gfServerOption::withTrans, py::arg("withTrans"))
      .def("withSyslog", &gfServerOption::withSyslog, py::arg("withSyslog"))
      .def("withPerSeqMax", &gfServerOption::withPerSeqMax, py::arg("withPerSeqMax"))
      .def("withNoSimpRepMask", &gfServerOption::withNoSimpRepMask, py::arg("withNoSimpRepMask"))
      .def("withIndexFile", &gfServerOption::withIndexFile, py::arg("withIndexFile"))
      .def("withTimeout", &gfServerOption::withTimeout, py::arg("withTimeout"))
      .def("build", &gfServerOption::build)
      .def("__str__", &gfServerOption::to_string);

  // gfserver -canStop -log={self.log_file_path} -stepSize=5 start localhost self.port self.ref_2bit
  // void startServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
  // gfServerOption &options)
  m.def("startServer", &startServer, py::arg("hostName"), py::arg("portName"), py::arg("fileCount"),
        py::arg("seqFiles"), py::arg("options"), "startServer");

  // void genoFindDirect(std::string &probeName, int fileCount, std::vector<std::string> &seqFiles, gfServerOption const
  // &options)
  m.def("genoFindDirect", &genoFindDirect, py::arg("probeName"), py::arg("fileCount"), py::arg("seqFiles"),
        py::arg("options"), "genoFindDirect");

  // void genoPcrDirect(std::string &fPrimer, std::string &rPrimer, int fileCount, std::vector<std::string> &seqFiles,
  // gfServerOption const &options)
  m.def("genoPcrDirect", &genoPcrDirect, py::arg("fPrimer"), py::arg("rPrimer"), py::arg("fileCount"),
        py::arg("seqFiles"), py::arg("options"), "A function that performs PCR on genomic sequences");

  // void stopServer(std::string &hostName, std::string &portName)
  m.def("stopServer", &stopServer, py::arg("hostName"), py::arg("portName"), "stop sever");

  // void queryServer(std::string &type, std::string &hostName, std::string &portName, std::string &faName, bool
  // complex, bool isProt)
  m.def("queryServer", &queryServer, py::arg("type"), py::arg("hostName"), py::arg("portName"), py::arg("faName"),
        py::arg("complex"), py::arg("isProt"), "queryServer");

  // void pcrServer(std::string &hostName, std::string &portName, std::string &fPrimer, std::string &rPrimer, int
  // maxSize)
  m.def("pcrServer", &pcrServer, py::arg("hostName"), py::arg("portName"), py::arg("fPrimer"), py::arg("rPrimer"),
        py::arg("maxSize"));

  // int statusServer(std::string &hostName, std::string &portName, gfServerOption &options)
  m.def("statusServer", &statusServer, py::arg("hostName"), py::arg("portName"), py::arg("options"));

  // void getFileList(std::string &hostName, std::string &portName)
  m.def("getFileList", &getFileList, py::arg("hostName"), py::arg());

  // void buildIndex(std::string &gfxFile, int fileCount, std::vector<std::string> seqFiles, gfServerOption const
  // &options)
  m.def("buildIndex", &buildIndex, py::arg("gfxFile"), py::arg("fileCount"), py::arg("seqFiles"), py::arg("options"));
}
