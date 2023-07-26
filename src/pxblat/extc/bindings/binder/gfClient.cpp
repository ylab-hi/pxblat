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
	{ // cppbinding::ClientOption file:gfClient.hpp line:69
		pybind11::class_<cppbinding::ClientOption, std::shared_ptr<cppbinding::ClientOption>> cl(M("cppbinding"), "ClientOption", "");

		cl.def( pybind11::init( [](){ return new cppbinding::ClientOption(); } ) );
		cl.def( pybind11::init( [](cppbinding::ClientOption const &o){ return new cppbinding::ClientOption(o); } ) );
		cl.def_readwrite("hostName", &cppbinding::ClientOption::hostName);
		cl.def_readwrite("portName", &cppbinding::ClientOption::portName);
		cl.def_readwrite("tType", &cppbinding::ClientOption::tType);
		cl.def_readwrite("qType", &cppbinding::ClientOption::qType);
		cl.def_readwrite("dots", &cppbinding::ClientOption::dots);
		cl.def_readwrite("nohead", &cppbinding::ClientOption::nohead);
		cl.def_readwrite("minScore", &cppbinding::ClientOption::minScore);
		cl.def_readwrite("minIdentity", &cppbinding::ClientOption::minIdentity);
		cl.def_readwrite("outputFormat", &cppbinding::ClientOption::outputFormat);
		cl.def_readwrite("maxIntron", &cppbinding::ClientOption::maxIntron);
		cl.def_readwrite("genome", &cppbinding::ClientOption::genome);
		cl.def_readwrite("genomeDataDir", &cppbinding::ClientOption::genomeDataDir);
		cl.def_readwrite("isDynamic", &cppbinding::ClientOption::isDynamic);
		cl.def_readwrite("SeqDir", &cppbinding::ClientOption::SeqDir);
		cl.def_readwrite("inName", &cppbinding::ClientOption::inName);
		cl.def_readwrite("outName", &cppbinding::ClientOption::outName);
		cl.def_readwrite("inSeq", &cppbinding::ClientOption::inSeq);
		cl.def("build", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)()) &cppbinding::ClientOption::build, "C++: cppbinding::ClientOption::build() --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic);
		cl.def("withHost", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withHost, "C++: cppbinding::ClientOption::withHost(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("hostName_"));
		cl.def("withPort", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withPort, "C++: cppbinding::ClientOption::withPort(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("portName_"));
		cl.def("withTType", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withTType, "C++: cppbinding::ClientOption::withTType(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("tType_"));
		cl.def("withQType", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withQType, "C++: cppbinding::ClientOption::withQType(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("qType_"));
		cl.def("withDots", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(int)) &cppbinding::ClientOption::withDots, "C++: cppbinding::ClientOption::withDots(int) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("dots_"));
		cl.def("withNohead", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(bool)) &cppbinding::ClientOption::withNohead, "C++: cppbinding::ClientOption::withNohead(bool) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("nohead_"));
		cl.def("withMinScore", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(int)) &cppbinding::ClientOption::withMinScore, "C++: cppbinding::ClientOption::withMinScore(int) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("minScore_"));
		cl.def("withMinIdentity", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(double)) &cppbinding::ClientOption::withMinIdentity, "C++: cppbinding::ClientOption::withMinIdentity(double) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("minIdentity_"));
		cl.def("withOutputFormat", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withOutputFormat, "C++: cppbinding::ClientOption::withOutputFormat(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("outputFormat_"));
		cl.def("withMaxIntron", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(long)) &cppbinding::ClientOption::withMaxIntron, "C++: cppbinding::ClientOption::withMaxIntron(long) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("maxIntron_"));
		cl.def("withGenome", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withGenome, "C++: cppbinding::ClientOption::withGenome(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("genome_"));
		cl.def("withGenomeDataDir", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withGenomeDataDir, "C++: cppbinding::ClientOption::withGenomeDataDir(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("genomeDataDir_"));
		cl.def("withIsDynamic", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(bool)) &cppbinding::ClientOption::withIsDynamic, "C++: cppbinding::ClientOption::withIsDynamic(bool) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("isDynamic_"));
		cl.def("withSeqDir", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withSeqDir, "C++: cppbinding::ClientOption::withSeqDir(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("SeqDir_"));
		cl.def("withInName", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withInName, "C++: cppbinding::ClientOption::withInName(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("inName_"));
		cl.def("withOutName", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withOutName, "C++: cppbinding::ClientOption::withOutName(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("outName_"));
		cl.def("withInSeq", (struct cppbinding::ClientOption & (cppbinding::ClientOption::*)(const std::string &)) &cppbinding::ClientOption::withInSeq, "C++: cppbinding::ClientOption::withInSeq(const std::string &) --> struct cppbinding::ClientOption &", pybind11::return_value_policy::automatic, pybind11::arg("inseq_"));
		cl.def("to_string", (std::string (cppbinding::ClientOption::*)() const) &cppbinding::ClientOption::to_string, "C++: cppbinding::ClientOption::to_string() const --> std::string");

		cl.def("__str__", [](cppbinding::ClientOption const &o) -> std::string { std::ostringstream s; using namespace cppbinding; s << o; return s.str(); } );
		cl.def("__repr__", [](cppbinding::ClientOption const &o) -> std::string { std::ostringstream s; using namespace cppbinding; s << o; return s.str(); } );

        cl.def(pybind11::pickle([](const cppbinding::ClientOption& p){
               return pybind11::make_tuple(p.hostName, p.portName,p.tType, p.qType, p.dots,
                                           p.nohead, p.minScore, p.minIdentity,
                                           p.outputFormat, p.maxIntron, p.genome,
                                           p.genomeDataDir, p.isDynamic, p.SeqDir,
                                           p.inName, p.outName, p.inSeq); },

                                [](pybind11::tuple t){
                                if (t.size() != 17)
                                    throw std::runtime_error("Invalid state!");
                                cppbinding::ClientOption p{};
                                p.hostName = t[0].cast<std::string>();
                                p.portName = t[1].cast<std::string>();
                                p.tType = t[2].cast<std::string>();
                                p.qType = t[3].cast<std::string>();
                                p.dots = t[4].cast<bool>();
                                p.nohead = t[5].cast<bool>();
                                p.minScore = t[6].cast<long>();
                                p.minIdentity = t[7].cast<long>();
                                p.outputFormat = t[8].cast<std::string>();
                                p.maxIntron = t[9].cast<long>();
                                p.genome = t[10].cast<std::string>();
                                p.genomeDataDir = t[11].cast<std::string>();
                                p.isDynamic = t[12].cast<bool>();
                                p.SeqDir = t[13].cast<std::string>();
                                p.inName = t[14].cast<std::string>();
                                p.outName = t[15].cast<std::string>();
                                p.inSeq = t[16].cast<std::string>();
                                return p;})
               );

	}

	// cppbinding::pygfClient(struct cppbinding::ClientOption &) file:gfClient.hpp line:118
  M("cppbinding").def("pygfClient", [](cppbinding::ClientOption&o) {
    auto ret = cppbinding::pygfClient(o);
    return pybind11::bytes(ret);
  }, "C++: cppbinding::pygfClient(struct cppbinding::ClientOption &) --> std::string", pybind11::arg("option"));

   M("cppbinding").def("pygfClient_no_gil", [](cppbinding::ClientOption o) {
    auto ret = cppbinding::pygfClient_no_gil(o);
    // return pybind11::bytes(ret);
  }, "C++: cppbinding::pygfClient(struct cppbinding::ClientOption &) --> std::string", pybind11::arg("option"));

}
