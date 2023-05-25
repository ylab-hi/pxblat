#include <gfServer.hpp>
#include <iterator>
#include <memory>
#include <pygfServer.hpp>
#include <string>
#include <vector>

#include <functional>
#include <pybind11/pybind11.h>
#include <string>
#include <pybind11/stl.h>
#include <thread>


#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>)
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*)
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>)
#endif


struct IntStruct {
    explicit IntStruct(int v) : value(v){};
    ~IntStruct() { value = -value; }
    IntStruct(const IntStruct &) = default;
    IntStruct &operator=(const IntStruct &) = default;

    int value;
};


void bind_pygfServer(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	// cppbinding::pystartServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::gfServerOption &, struct cppbinding::UsageStats &) file:pygfServer.hpp line:16
	M("cppbinding").def("pystartServer", (int (*)(std::string , std::string , int, class std::vector<std::string > , struct cppbinding::gfServerOption , struct cppbinding::UsageStats )) &cppbinding::pystartServer, "C++: cppbinding::pystartServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::gfServerOption &, struct cppbinding::UsageStats &) --> int", pybind11::arg("hostName"), pybind11::arg("portName"), pybind11::arg("fileCount"), pybind11::arg("seqFiles"), pybind11::arg("options"), pybind11::arg("stats"));
	M("cppbinding").def("pystartServer_no_gil", (int (*)(std::string , std::string , int, class std::vector<std::string > , struct cppbinding::gfServerOption , struct cppbinding::UsageStats )) &cppbinding::pystartServer, "C++: cppbinding::pystartServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::gfServerOption &, struct cppbinding::UsageStats &) --> int", pybind11::arg("hostName"), pybind11::arg("portName"), pybind11::arg("fileCount"), pybind11::arg("seqFiles"), pybind11::arg("options"), pybind11::arg("stats"),  pybind11::call_guard<pybind11::gil_scoped_release>());

	// pybind11::class_<cppbinding::Signal, std::shared_ptr<cppbinding::Signal>> cl(M("cppbinding"), "Signal", "");

{
   namespace py=pybind11;

  pybind11::class_<IntStruct> cl(M("cppbinding"), "IntStruct", "");
  cl.def(pybind11::init([](const int i){return IntStruct(i);}), "");
  py::implicitly_convertible<int, IntStruct>();

  M("cppbinding").def("test", [](int expected, const IntStruct &in) {
        {
            py::gil_scoped_release release;
            std::this_thread::sleep_for(std::chrono::milliseconds(5));
        }

        if (in.value != expected) {
            throw std::runtime_error("Value changed!!");
        }
    });

  M("cppbinding").def(
        "test_no_gil",
        [](int expected, const IntStruct &in) {
            std::this_thread::sleep_for(std::chrono::milliseconds(5));
            if (in.value != expected) {
                throw std::runtime_error("Value changed!!");
            }
        },
        py::call_guard<py::gil_scoped_release>());

  M("cppbinding").def(
        "test_with_gil",
        [](int expected, const IntStruct &in) {
            std::this_thread::sleep_for(std::chrono::milliseconds(5));
            if (in.value != expected) {
                throw std::runtime_error("Value changed!!");
            }
        });
  }

}
