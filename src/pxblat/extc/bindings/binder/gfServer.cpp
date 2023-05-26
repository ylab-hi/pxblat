#include <gfServer.hpp>
#include <ios>
#include <iterator>
#include <locale>
#include <memory>
#include <ostream>
#include <sstream> // __str__
#include <streambuf>
#include <string>
#include <vector>

#include <functional>
#include <pybind11/pybind11.h>
#include <string>
#include <pybind11/stl.h>


#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>)
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*)
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>)
#endif

void bind_gfServer(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // cppbinding::Signal file:gfServer.hpp line:39
		pybind11::class_<cppbinding::Signal, std::shared_ptr<cppbinding::Signal>> cl(M("cppbinding"), "Signal", "");
		cl.def( pybind11::init( [](){ return new cppbinding::Signal(); } ) );
		cl.def_readwrite("isReady", &cppbinding::Signal::isReady);

		cl.def("__str__", [](cppbinding::Signal const &o) -> std::string { std::ostringstream s; using namespace cppbinding; s << o; return s.str(); } );
	}
	{ // cppbinding::UsageStats file:gfServer.hpp line:45
		pybind11::class_<cppbinding::UsageStats, std::shared_ptr<cppbinding::UsageStats>> cl(M("cppbinding"), "UsageStats", "");
		cl.def( pybind11::init( [](){ return new cppbinding::UsageStats(); } ) );
		cl.def_readwrite("baseCount", &cppbinding::UsageStats::baseCount);
		cl.def_readwrite("blatCount", &cppbinding::UsageStats::blatCount);
		cl.def_readwrite("aaCount", &cppbinding::UsageStats::aaCount);
		cl.def_readwrite("pcrCount", &cppbinding::UsageStats::pcrCount);
		cl.def_readwrite("warnCount", &cppbinding::UsageStats::warnCount);
		cl.def_readwrite("noSigCount", &cppbinding::UsageStats::noSigCount);
		cl.def_readwrite("missCount", &cppbinding::UsageStats::missCount);
		cl.def_readwrite("trimCount", &cppbinding::UsageStats::trimCount);

		cl.def("__str__", [](cppbinding::UsageStats const &o) -> std::string { std::ostringstream s; using namespace cppbinding; s << o; return s.str(); } );

        cl.def(pybind11::pickle([](const cppbinding::UsageStats &p) { // __getstate__
            return pybind11::make_tuple(p.baseCount, p.blatCount, p.aaCount, p.pcrCount, p.warnCount
                                                            , p.noSigCount, p.missCount, p.trimCount);

             },
            [](pybind11::tuple t) { // __setstate__
                    if (t.size() != 8)
                        throw std::runtime_error("Invalid state!");

                    cppbinding::UsageStats p{};
                    p.baseCount = t[0].cast<int>();
                    p.blatCount = t[1].cast<int>();
                    p.aaCount = t[2].cast<int>();
                    p.pcrCount = t[3].cast<int>();
                    p.warnCount = t[4].cast<int>();
                    p.noSigCount = t[5].cast<int>();
                    p.missCount = t[6].cast<int>();
                    p.trimCount = t[7].cast<int>();
                    return p;
                }));
	}
	{ // cppbinding::gfServerOption file:gfServer.hpp line:74
		pybind11::class_<cppbinding::gfServerOption, std::shared_ptr<cppbinding::gfServerOption>> cl(M("cppbinding"), "gfServerOption", "");
		cl.def( pybind11::init( [](){ return new cppbinding::gfServerOption(); } ) );
		cl.def( pybind11::init( [](cppbinding::gfServerOption const &o){ return new cppbinding::gfServerOption(o); } ) );
		cl.def_readwrite("canStop", &cppbinding::gfServerOption::canStop);
		cl.def_readwrite("log", &cppbinding::gfServerOption::log);
		cl.def_readwrite("logFacility", &cppbinding::gfServerOption::logFacility);
		cl.def_readwrite("mask", &cppbinding::gfServerOption::mask);
		cl.def_readwrite("maxAaSize", &cppbinding::gfServerOption::maxAaSize);
		cl.def_readwrite("maxDnaHits", &cppbinding::gfServerOption::maxDnaHits);
		cl.def_readwrite("maxGap", &cppbinding::gfServerOption::maxGap);
		cl.def_readwrite("maxNtSize", &cppbinding::gfServerOption::maxNtSize);
		cl.def_readwrite("maxTransHits", &cppbinding::gfServerOption::maxTransHits);
		cl.def_readwrite("minMatch", &cppbinding::gfServerOption::minMatch);
		cl.def_readwrite("repMatch", &cppbinding::gfServerOption::repMatch);
		cl.def_readwrite("seqLog", &cppbinding::gfServerOption::seqLog);
		cl.def_readwrite("ipLog", &cppbinding::gfServerOption::ipLog);
		cl.def_readwrite("debugLog", &cppbinding::gfServerOption::debugLog);
		cl.def_readwrite("tileSize", &cppbinding::gfServerOption::tileSize);
		cl.def_readwrite("stepSize", &cppbinding::gfServerOption::stepSize);
		cl.def_readwrite("trans", &cppbinding::gfServerOption::trans);
		cl.def_readwrite("syslog", &cppbinding::gfServerOption::syslog);
		cl.def_readwrite("perSeqMax", &cppbinding::gfServerOption::perSeqMax);
		cl.def_readwrite("noSimpRepMask", &cppbinding::gfServerOption::noSimpRepMask);
		cl.def_readwrite("indexFile", &cppbinding::gfServerOption::indexFile);
		cl.def_readwrite("timeout", &cppbinding::gfServerOption::timeout);
		cl.def_readwrite("genome", &cppbinding::gfServerOption::genome);
		cl.def_readwrite("genomeDataDir", &cppbinding::gfServerOption::genomeDataDir);
		cl.def_readwrite("threads", &cppbinding::gfServerOption::threads);
		cl.def_readwrite("allowOneMismatch", &cppbinding::gfServerOption::allowOneMismatch);
		cl.def("build", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)()) &cppbinding::gfServerOption::build, "C++: cppbinding::gfServerOption::build() --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic);
		cl.def("to_string", (std::string (cppbinding::gfServerOption::*)() const) &cppbinding::gfServerOption::to_string, "C++: cppbinding::gfServerOption::to_string() const --> std::string");
		cl.def("withCanStop", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(bool)) &cppbinding::gfServerOption::withCanStop, "C++: cppbinding::gfServerOption::withCanStop(bool) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("canStop_"));
		cl.def("withLogFacility", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(std::string)) &cppbinding::gfServerOption::withLogFacility, "C++: cppbinding::gfServerOption::withLogFacility(std::string) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("logFacility_"));
		cl.def("withLog", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(std::string)) &cppbinding::gfServerOption::withLog, "C++: cppbinding::gfServerOption::withLog(std::string) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("log_"));
		cl.def("withMask", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(bool)) &cppbinding::gfServerOption::withMask, "C++: cppbinding::gfServerOption::withMask(bool) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("mask_"));
		cl.def("withMaxAaSize", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withMaxAaSize, "C++: cppbinding::gfServerOption::withMaxAaSize(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("maxAaSize_"));
		cl.def("withMaxDnaHits", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withMaxDnaHits, "C++: cppbinding::gfServerOption::withMaxDnaHits(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("maxDnaHits_"));
		cl.def("withMaxGap", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withMaxGap, "C++: cppbinding::gfServerOption::withMaxGap(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("maxGap_"));
		cl.def("withMaxNtSize", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withMaxNtSize, "C++: cppbinding::gfServerOption::withMaxNtSize(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("maxNtSize_"));
		cl.def("withMaxTransHits", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withMaxTransHits, "C++: cppbinding::gfServerOption::withMaxTransHits(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("maxTransHits_"));
		cl.def("withMinMatch", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withMinMatch, "C++: cppbinding::gfServerOption::withMinMatch(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("minMatch_"));
		cl.def("withRepMatch", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withRepMatch, "C++: cppbinding::gfServerOption::withRepMatch(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("repMatch_"));
		cl.def("withSeqLog", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(bool)) &cppbinding::gfServerOption::withSeqLog, "C++: cppbinding::gfServerOption::withSeqLog(bool) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("seqLog_"));
		cl.def("withIpLog", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(bool)) &cppbinding::gfServerOption::withIpLog, "C++: cppbinding::gfServerOption::withIpLog(bool) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("ipLog_"));
		cl.def("withDebugLog", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(bool)) &cppbinding::gfServerOption::withDebugLog, "C++: cppbinding::gfServerOption::withDebugLog(bool) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("debugLog_"));
		cl.def("withTileSize", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withTileSize, "C++: cppbinding::gfServerOption::withTileSize(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("tileSize_"));
		cl.def("withStepSize", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withStepSize, "C++: cppbinding::gfServerOption::withStepSize(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("stepSize_"));
		cl.def("withTrans", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(bool)) &cppbinding::gfServerOption::withTrans, "C++: cppbinding::gfServerOption::withTrans(bool) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("trans_"));
		cl.def("withSyslog", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(bool)) &cppbinding::gfServerOption::withSyslog, "C++: cppbinding::gfServerOption::withSyslog(bool) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("syslog_"));
		cl.def("withPerSeqMax", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(std::string)) &cppbinding::gfServerOption::withPerSeqMax, "C++: cppbinding::gfServerOption::withPerSeqMax(std::string) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("perSeqMax_"));
		cl.def("withNoSimpRepMask", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(bool)) &cppbinding::gfServerOption::withNoSimpRepMask, "C++: cppbinding::gfServerOption::withNoSimpRepMask(bool) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("noSimpRepMask_"));
		cl.def("withIndexFile", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(std::string)) &cppbinding::gfServerOption::withIndexFile, "C++: cppbinding::gfServerOption::withIndexFile(std::string) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("indexFile_"));
		cl.def("withTimeout", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withTimeout, "C++: cppbinding::gfServerOption::withTimeout(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("timeout_"));
		cl.def("withThreads", (struct cppbinding::gfServerOption & (cppbinding::gfServerOption::*)(int)) &cppbinding::gfServerOption::withThreads, "C++: cppbinding::gfServerOption::withThreads(int) --> struct cppbinding::gfServerOption &", pybind11::return_value_policy::automatic, pybind11::arg("threads_"));

		cl.def("__str__", [](cppbinding::gfServerOption const &o) -> std::string { std::ostringstream s; using namespace cppbinding; s << o; return s.str(); } );

        cl.def(pybind11::pickle(
            [](const cppbinding::gfServerOption &p) { // __getstate__

                return pybind11::make_tuple(p.canStop,p.log,p.logFacility, p.mask, p.maxAaSize, p.maxDnaHits,
                                            p.maxGap, p.maxNtSize, p.maxTransHits, p.minMatch, p.repMatch,
                                            p.seqLog, p.ipLog, p.debugLog, p.tileSize, p.stepSize,p.trans,
                                            p.syslog, p.perSeqMax, p.noSimpRepMask, p.indexFile, p.timeout,
                                            p.genome, p.genomeDataDir,p.threads,p.allowOneMismatch);

                 },
                [](pybind11::tuple t) { // __setstate__
                  if (t.size() != 26)
                      throw std::runtime_error("Invalid state!");
                    cppbinding::gfServerOption p{};
                    p.withCanStop(t[0].cast<bool>());
                    p.withLog(t[1].cast<std::string>());
                    p.withLogFacility(t[2].cast<std::string>());
                    p.withMask(t[3].cast<bool>());
                    p.withMaxAaSize(t[4].cast<int>());
                    p.withMaxDnaHits(t[5].cast<int>());
                    p.withMaxGap(t[6].cast<int>());
                    p.withMaxNtSize(t[7].cast<int>());
                    p.withMaxTransHits(t[8].cast<int>());
                    p.withMinMatch(t[9].cast<int>());
                    p.withRepMatch(t[10].cast<int>());
                    p.withSeqLog(t[11].cast<bool>());
                    p.withIpLog(t[12].cast<bool>());
                    p.withDebugLog(t[13].cast<bool>());
                    p.withTileSize(t[14].cast<int>());
                    p.withStepSize(t[15].cast<int>());
                    p.withTrans(t[16].cast<bool>());
                    p.withSyslog(t[17].cast<bool>());
                    p.withPerSeqMax(t[18].cast<std::string>());
                    p.withNoSimpRepMask(t[19].cast<bool>());
                    p.withIndexFile(t[20].cast<std::string>());
                    p.withTimeout(t[21].cast<int>());

                    p.genome = t[22].cast<std::string>();
                    p.genomeDataDir = t[23].cast<std::string>();
                    p.withThreads(t[24].cast<int>());
                    p.allowOneMismatch = t[25].cast<bool>();
                    return p;
            }));
	}
	// cppbinding::gfServer(struct cppbinding::gfServerOption &) file:gfServer.hpp line:146
	M("cppbinding").def("gfServer", (void (*)(struct cppbinding::gfServerOption &)) &cppbinding::gfServer, "C++: cppbinding::gfServer(struct cppbinding::gfServerOption &) --> void", pybind11::arg("options"));

	// cppbinding::genoFindDirect(std::string &, int, class std::vector<std::string > &, const struct cppbinding::gfServerOption &) file:gfServer.hpp line:158
	M("cppbinding").def("genoFindDirect", (void (*)(std::string &, int, class std::vector<std::string > &, const struct cppbinding::gfServerOption &)) &cppbinding::genoFindDirect, "C++: cppbinding::genoFindDirect(std::string &, int, class std::vector<std::string > &, const struct cppbinding::gfServerOption &) --> void", pybind11::arg("probeName"), pybind11::arg("fileCount"), pybind11::arg("seqFiles"), pybind11::arg("options"));

	// cppbinding::genoPcrDirect(std::string &, std::string &, int, class std::vector<std::string > &, const struct cppbinding::gfServerOption &) file:gfServer.hpp line:162
	M("cppbinding").def("genoPcrDirect", (void (*)(std::string &, std::string &, int, class std::vector<std::string > &, const struct cppbinding::gfServerOption &)) &cppbinding::genoPcrDirect, "C++: cppbinding::genoPcrDirect(std::string &, std::string &, int, class std::vector<std::string > &, const struct cppbinding::gfServerOption &) --> void", pybind11::arg("fPrimer"), pybind11::arg("rPrimer"), pybind11::arg("fileCount"), pybind11::arg("seqFiles"), pybind11::arg("options"));

	// cppbinding::startServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::gfServerOption &, struct cppbinding::UsageStats &) file:gfServer.hpp line:167
	M("cppbinding").def("startServer", (void (*)(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::gfServerOption &, struct cppbinding::UsageStats &)) &cppbinding::startServer, "C++: cppbinding::startServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::gfServerOption &, struct cppbinding::UsageStats &) --> void", pybind11::arg("hostName"), pybind11::arg("portName"), pybind11::arg("fileCount"), pybind11::arg("seqFiles"), pybind11::arg("options"), pybind11::arg("stats"));

	// cppbinding::stopServer(std::string &, std::string &) file:gfServer.hpp line:171
	M("cppbinding").def("stopServer", (void (*)(std::string &, std::string &)) &cppbinding::stopServer, "C++: cppbinding::stopServer(std::string &, std::string &) --> void", pybind11::arg("hostName"), pybind11::arg("portName"));

	// cppbinding::queryServer(std::string &, std::string &, std::string &, std::string &, bool, bool) file:gfServer.hpp line:174
	M("cppbinding").def("queryServer", (void (*)(std::string &, std::string &, std::string &, std::string &, bool, bool)) &cppbinding::queryServer, "C++: cppbinding::queryServer(std::string &, std::string &, std::string &, std::string &, bool, bool) --> void", pybind11::arg("type"), pybind11::arg("hostName"), pybind11::arg("portName"), pybind11::arg("faName"), pybind11::arg("complex"), pybind11::arg("isProt"));

	// cppbinding::pcrServer(std::string &, std::string &, std::string &, std::string &, int) file:gfServer.hpp line:179
	M("cppbinding").def("pcrServer", (void (*)(std::string &, std::string &, std::string &, std::string &, int)) &cppbinding::pcrServer, "C++: cppbinding::pcrServer(std::string &, std::string &, std::string &, std::string &, int) --> void", pybind11::arg("hostName"), pybind11::arg("portName"), pybind11::arg("fPrimer"), pybind11::arg("rPrimer"), pybind11::arg("maxSize"));

	// cppbinding::statusServer(std::string &, std::string &, struct cppbinding::gfServerOption &) file:gfServer.hpp line:182
	M("cppbinding").def("statusServer", (int (*)(std::string &, std::string &, struct cppbinding::gfServerOption &)) &cppbinding::statusServer, "C++: cppbinding::statusServer(std::string &, std::string &, struct cppbinding::gfServerOption &) --> int", pybind11::arg("hostName"), pybind11::arg("portName"), pybind11::arg("options"));

	// cppbinding::getFileList(std::string &, std::string &) file:gfServer.hpp line:185
	M("cppbinding").def("getFileList", (void (*)(std::string &, std::string &)) &cppbinding::getFileList, "C++: cppbinding::getFileList(std::string &, std::string &) --> void", pybind11::arg("hostName"), pybind11::arg("portName"));

	// cppbinding::buildIndex(std::string &, int, class std::vector<std::string >, const struct cppbinding::gfServerOption &) file:gfServer.hpp line:189
	M("cppbinding").def("buildIndex", (void (*)(std::string &, int, class std::vector<std::string >, const struct cppbinding::gfServerOption &)) &cppbinding::buildIndex, "C++: cppbinding::buildIndex(std::string &, int, class std::vector<std::string >, const struct cppbinding::gfServerOption &) --> void", pybind11::arg("gfxFile"), pybind11::arg("fileCount"), pybind11::arg("seqFiles"), pybind11::arg("options"));

	// cppbinding::getPortIx(char *) file:gfServer.hpp line:191
	M("cppbinding").def("getPortIx", (int (*)(char *)) &cppbinding::getPortIx, "C++: cppbinding::getPortIx(char *) --> int", pybind11::arg("portName"));

}
