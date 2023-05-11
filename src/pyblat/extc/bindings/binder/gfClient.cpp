#include <gfClient.hpp>
#include <ios>
#include <iterator>
#include <locale>
#include <memory>
#include <ostream>
#include <sstream> // __str__
#include <streambuf>
#include <string>

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

void bind_gfClient(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // cppbinding::gfClientOption file:gfClient.hpp line:69
		pybind11::class_<cppbinding::gfClientOption, std::shared_ptr<cppbinding::gfClientOption>> cl(M("cppbinding"), "gfClientOption", "");
		cl.def( pybind11::init( [](){ return new cppbinding::gfClientOption(); } ) );
		cl.def( pybind11::init( [](cppbinding::gfClientOption const &o){ return new cppbinding::gfClientOption(o); } ) );
		cl.def_readwrite("hostName", &cppbinding::gfClientOption::hostName);
		cl.def_readwrite("portName", &cppbinding::gfClientOption::portName);
		cl.def_readwrite("tType", &cppbinding::gfClientOption::tType);
		cl.def_readwrite("qType", &cppbinding::gfClientOption::qType);
		cl.def_readwrite("dots", &cppbinding::gfClientOption::dots);
		cl.def_readwrite("nohead", &cppbinding::gfClientOption::nohead);
		cl.def_readwrite("minScore", &cppbinding::gfClientOption::minScore);
		cl.def_readwrite("minIdentity", &cppbinding::gfClientOption::minIdentity);
		cl.def_readwrite("outputFormat", &cppbinding::gfClientOption::outputFormat);
		cl.def_readwrite("maxIntron", &cppbinding::gfClientOption::maxIntron);
		cl.def_readwrite("genome", &cppbinding::gfClientOption::genome);
		cl.def_readwrite("genomeDataDir", &cppbinding::gfClientOption::genomeDataDir);
		cl.def_readwrite("isDynamic", &cppbinding::gfClientOption::isDynamic);
		cl.def_readwrite("tSeqDir", &cppbinding::gfClientOption::tSeqDir);
		cl.def_readwrite("inName", &cppbinding::gfClientOption::inName);
		cl.def_readwrite("outName", &cppbinding::gfClientOption::outName);
		cl.def("build", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)()) &cppbinding::gfClientOption::build, "C++: cppbinding::gfClientOption::build() --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic);
		cl.def("withHost", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(const std::string &)) &cppbinding::gfClientOption::withHost, "C++: cppbinding::gfClientOption::withHost(const std::string &) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("hostName_"));
		cl.def("withPort", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(const std::string &)) &cppbinding::gfClientOption::withPort, "C++: cppbinding::gfClientOption::withPort(const std::string &) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("portName_"));
		cl.def("withTType", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(const std::string &)) &cppbinding::gfClientOption::withTType, "C++: cppbinding::gfClientOption::withTType(const std::string &) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("tType_"));
		cl.def("withQType", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(const std::string &)) &cppbinding::gfClientOption::withQType, "C++: cppbinding::gfClientOption::withQType(const std::string &) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("qType_"));
		cl.def("withDots", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(int)) &cppbinding::gfClientOption::withDots, "C++: cppbinding::gfClientOption::withDots(int) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("dots_"));
		cl.def("withNohead", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(bool)) &cppbinding::gfClientOption::withNohead, "C++: cppbinding::gfClientOption::withNohead(bool) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("nohead_"));
		cl.def("withMinScore", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(int)) &cppbinding::gfClientOption::withMinScore, "C++: cppbinding::gfClientOption::withMinScore(int) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("minScore_"));
		cl.def("withMinIdentity", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(double)) &cppbinding::gfClientOption::withMinIdentity, "C++: cppbinding::gfClientOption::withMinIdentity(double) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("minIdentity_"));
		cl.def("withOutputFormat", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(const std::string &)) &cppbinding::gfClientOption::withOutputFormat, "C++: cppbinding::gfClientOption::withOutputFormat(const std::string &) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("outputFormat_"));
		cl.def("withMaxIntron", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(long)) &cppbinding::gfClientOption::withMaxIntron, "C++: cppbinding::gfClientOption::withMaxIntron(long) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("maxIntron_"));
		cl.def("withGenome", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(const std::string &)) &cppbinding::gfClientOption::withGenome, "C++: cppbinding::gfClientOption::withGenome(const std::string &) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("genome_"));
		cl.def("withGenomeDataDir", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(const std::string &)) &cppbinding::gfClientOption::withGenomeDataDir, "C++: cppbinding::gfClientOption::withGenomeDataDir(const std::string &) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("genomeDataDir_"));
		cl.def("withIsDynamic", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(bool)) &cppbinding::gfClientOption::withIsDynamic, "C++: cppbinding::gfClientOption::withIsDynamic(bool) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("isDynamic_"));
		cl.def("withTSeqDir", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(const std::string &)) &cppbinding::gfClientOption::withTSeqDir, "C++: cppbinding::gfClientOption::withTSeqDir(const std::string &) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("tSeqDir_"));
		cl.def("withInName", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(const std::string &)) &cppbinding::gfClientOption::withInName, "C++: cppbinding::gfClientOption::withInName(const std::string &) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("inName_"));
		cl.def("withOutName", (struct cppbinding::gfClientOption & (cppbinding::gfClientOption::*)(const std::string &)) &cppbinding::gfClientOption::withOutName, "C++: cppbinding::gfClientOption::withOutName(const std::string &) --> struct cppbinding::gfClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("outName_"));
		cl.def("to_string", (std::string (cppbinding::gfClientOption::*)() const) &cppbinding::gfClientOption::to_string, "C++: cppbinding::gfClientOption::to_string() const --> std::string");

		cl.def("__str__", [](cppbinding::gfClientOption const &o) -> std::string { std::ostringstream s; using namespace cppbinding; s << o; return s.str(); } );
	}
	// cppbinding::pygfClient(struct cppbinding::gfClientOption &) file:gfClient.hpp line:115
	M("cppbinding").def("pygfClient", (std::string (*)(struct cppbinding::gfClientOption &)) &cppbinding::pygfClient, "C++: cppbinding::pygfClient(struct cppbinding::gfClientOption &) --> std::string", pybind11::arg("option"));

}
