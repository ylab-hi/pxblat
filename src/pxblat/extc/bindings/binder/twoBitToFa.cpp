#include <twoBitToFa.hpp>
#include <iterator>
#include <memory>
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

void bind_twoBitToFa(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
    {
        pybind11::class_<cppbinding::TwoBitToFaOption, std::shared_ptr<cppbinding::TwoBitToFaOption>> cl(M("cppbinding"), "TwoBitToFaOption", "");
        cl.def( pybind11::init( [](){ return new cppbinding::TwoBitToFaOption(); } ) );
        cl.def( pybind11::init( [](cppbinding::TwoBitToFaOption const &o){ return new cppbinding::TwoBitToFaOption(o); } ) );
        cl.def_readwrite("seq", &cppbinding::TwoBitToFaOption::seq);
        cl.def_readwrite("start", &cppbinding::TwoBitToFaOption::start);
        cl.def_readwrite("end", &cppbinding::TwoBitToFaOption::end);
        cl.def_readwrite("seqList", &cppbinding::TwoBitToFaOption::seqList);
        cl.def_readwrite("noMask", &cppbinding::TwoBitToFaOption::noMask);
        cl.def_readwrite("bpt", &cppbinding::TwoBitToFaOption::bpt);
        cl.def_readwrite("bed", &cppbinding::TwoBitToFaOption::bed);
        cl.def_readwrite("bedPos", &cppbinding::TwoBitToFaOption::bedPos);
        cl.def_readwrite("udcDir", &cppbinding::TwoBitToFaOption::udcDir);
        cl.def("build", (struct cppbinding::TwoBitToFaOption& (cppbinding::TwoBitToFaOption::*)()) &cppbinding::TwoBitToFaOption::build, "C++: cppbinding::TwoBitToFaOption::build() --> struct cppbinding::TwoBitToFaOption &", pybind11::return_value_policy::automatic);
        cl.def("withSeq", (struct cppbinding::TwoBitToFaOption& (cppbinding::TwoBitToFaOption::*)(std::string const &)) &cppbinding::TwoBitToFaOption::withSeq, "C++: cppbinding::TwoBitToFaOption::withSeq(std::string const &) --> struct cppbinding::TwoBitToFaOption &", pybind11::arg("seq"));
        cl.def("withStart", (struct cppbinding::TwoBitToFaOption& (cppbinding::TwoBitToFaOption::*)(int)) &cppbinding::TwoBitToFaOption::withStart, "C++: cppbinding::TwoBitToFaOption::withStart(int) --> struct cppbinding::TwoBitToFaOption &", pybind11::arg("start"));
        cl.def("withEnd", (struct cppbinding::TwoBitToFaOption& (cppbinding::TwoBitToFaOption::*)(int)) &cppbinding::TwoBitToFaOption::withEnd, "C++: cppbinding::TwoBitToFaOption::withEnd(int) --> struct cppbinding::TwoBitToFaOption &", pybind11::arg("end"));
        cl.def("withSeqList", (struct cppbinding::TwoBitToFaOption& (cppbinding::TwoBitToFaOption::*)(std::string const &)) &cppbinding::TwoBitToFaOption::withSeqList, "C++: cppbinding::TwoBitToFaOption::withSeqList(std::string const &) --> struct cppbinding::TwoBitToFaOption &", pybind11::arg("seqList"));
        cl.def("withNoMask", (struct cppbinding::TwoBitToFaOption& (cppbinding::TwoBitToFaOption::*)(bool)) &cppbinding::TwoBitToFaOption::withNoMask, "C++: cppbinding::TwoBitToFaOption::withNoMask(bool) --> struct cppbinding::TwoBitToFaOption &", pybind11::arg("noMask"));
        cl.def("withBpt", (struct cppbinding::TwoBitToFaOption& (cppbinding::TwoBitToFaOption::*)(std::string const &)) &cppbinding::TwoBitToFaOption::withBpt, "C++: cppbinding::TwoBitToFaOption::withBpt(std::string const &) --> struct cppbinding::TwoBitToFaOption &", pybind11::arg("bpt"));
        cl.def("withBed", (struct cppbinding::TwoBitToFaOption& (cppbinding::TwoBitToFaOption::*)(std::string const &)) &cppbinding::TwoBitToFaOption::withBed, "C++: cppbinding::TwoBitToFaOption::withBed(std::string const &) --> struct cppbinding::TwoBitToFaOption &", pybind11::arg("bed"));
        cl.def("withBedPos", (struct cppbinding::TwoBitToFaOption& (cppbinding::TwoBitToFaOption::*)(bool)) &cppbinding::TwoBitToFaOption::withBedPos, "C++: cppbinding::TwoBitToFaOption::withBedPos(bool) --> struct cppbinding::TwoBitToFaOption &", pybind11::arg("bedPos"));
        cl.def("withUdcDir", (struct cppbinding::TwoBitToFaOption& (cppbinding::TwoBitToFaOption::*)(std::string const &)) &cppbinding::TwoBitToFaOption::withUdcDir, "C++: cppbinding::TwoBitToFaOption::withUdcDir(std::string const &) --> struct cppbinding::TwoBitToFaOption &", pybind11::arg("udcDir"));
        cl.def("to_string", (std::string (cppbinding::TwoBitToFaOption::*)() const) &cppbinding::TwoBitToFaOption::to_string, "C++: cppbinding::TwoBitToFaOption::to_string() --> std::string");
        cl.def("__str__", [](cppbinding::TwoBitToFaOption const &o) -> std::string { return o.to_string(); } );
        cl.def(pybind11::pickle(
            [](const cppbinding::TwoBitToFaOption& p){
                return pybind11::make_tuple(
                    p.seq, p.start, p.end, p.seqList, p.noMask, p.bpt, p.bed, p.bedPos, p.udcDir);
            },
            [](pybind11::tuple t){
                if (t.size() != 9)
                    throw std::runtime_error("Invalid state!");

                cppbinding::TwoBitToFaOption p{};

                p.seq = t[0].cast<std::string>();
                p.start = t[1].cast<int>();
                p.end = t[2].cast<int>();
                p.seqList = t[3].cast<std::string>();
                p.noMask = t[4].cast<bool>();
                p.bpt = t[5].cast<std::string>();
                p.bed = t[6].cast<std::string>();
                p.bedPos = t[7].cast<bool>();
                p.udcDir = t[8].cast<std::string>();
                return p;}));
    }

    // void twoBitToFa(std::string cppinName, std::string cppoutName, TwoBitToFaOption option);
    M("cppbinding").def("twoBitToFa", &cppbinding::twoBitToFa, "C++ cppbinding::twoBitToFa(std::string cppinName, std::string cppoutName, TwoBitToFaOption option)", pybind11::arg("inName"), pybind11::arg("outName"), pybind11::arg("option"));


}
