#include <faToTwoBit.hpp>
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

void bind_faToTwoBit(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	// cppbinding::faToTwoBit(class std::vector<std::string > &, std::string &, bool, bool, bool, bool) file:faToTwoBit.hpp line:34
	M("cppbinding").def("faToTwoBit", [](class std::vector<std::string > & a0, std::string & a1) -> int { return cppbinding::faToTwoBit(a0, a1); }, "", pybind11::arg("inFiles"), pybind11::arg("outFile"));
	M("cppbinding").def("faToTwoBit", [](class std::vector<std::string > & a0, std::string & a1, bool const & a2) -> int { return cppbinding::faToTwoBit(a0, a1, a2); }, "", pybind11::arg("inFiles"), pybind11::arg("outFile"), pybind11::arg("noMask"));
	M("cppbinding").def("faToTwoBit", [](class std::vector<std::string > & a0, std::string & a1, bool const & a2, bool const & a3) -> int { return cppbinding::faToTwoBit(a0, a1, a2, a3); }, "", pybind11::arg("inFiles"), pybind11::arg("outFile"), pybind11::arg("noMask"), pybind11::arg("stripVersion"));
	M("cppbinding").def("faToTwoBit", [](class std::vector<std::string > & a0, std::string & a1, bool const & a2, bool const & a3, bool const & a4) -> int { return cppbinding::faToTwoBit(a0, a1, a2, a3, a4); }, "", pybind11::arg("inFiles"), pybind11::arg("outFile"), pybind11::arg("noMask"), pybind11::arg("stripVersion"), pybind11::arg("ignoreDups"));
	M("cppbinding").def("faToTwoBit", (int (*)(class std::vector<std::string > &, std::string &, bool, bool, bool, bool)) &cppbinding::faToTwoBit, "C++: cppbinding::faToTwoBit(class std::vector<std::string > &, std::string &, bool, bool, bool, bool) --> int", pybind11::arg("inFiles"), pybind11::arg("outFile"), pybind11::arg("noMask"), pybind11::arg("stripVersion"), pybind11::arg("ignoreDups"), pybind11::arg("useLong"));

}
