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

class Pickleable {
public:
    Pickleable(const std::string &value) : m_value(value) { }
    const std::string &value() const { return m_value; }

    void setExtra(int extra) { m_extra = extra; }
    int extra() const { return m_extra; }
private:
    std::string m_value;
    int m_extra = 0;
};


void bind_pygfServer(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	// cppbinding::pystartServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::ServerOption &, struct cppbinding::UsageStats &) file:pygfServer.hpp line:16
	M("cppbinding").def("pystartServer", (int (*)(std::string , std::string , int, class std::vector<std::string > , struct cppbinding::ServerOption , struct cppbinding::UsageStats )) &cppbinding::pystartServer, "C++: cppbinding::pystartServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::ServerOption &, struct cppbinding::UsageStats &) --> int", pybind11::arg("hostName"), pybind11::arg("portName"), pybind11::arg("fileCount"), pybind11::arg("seqFiles"), pybind11::arg("options"), pybind11::arg("stats"));
	M("cppbinding").def("pystartServer_no_gil", (int (*)(std::string , std::string , int, class std::vector<std::string > , struct cppbinding::ServerOption , struct cppbinding::UsageStats )) &cppbinding::pystartServer, "C++: cppbinding::pystartServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::ServerOption &, struct cppbinding::UsageStats &) --> int", pybind11::arg("hostName"), pybind11::arg("portName"), pybind11::arg("fileCount"), pybind11::arg("seqFiles"), pybind11::arg("options"), pybind11::arg("stats"),  pybind11::call_guard<pybind11::gil_scoped_release>());


    {
        pybind11::class_<IntStruct> cl(M("cppbinding"), "IntStruct", "");
        cl.def(pybind11::init([](const int i){return IntStruct(i);}), "");
        pybind11::implicitly_convertible<int, IntStruct>();

        M("cppbinding").def("test", [](int expected, const IntStruct &in) {
            {
                pybind11::gil_scoped_release release;
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
            pybind11::call_guard<pybind11::gil_scoped_release>());

        M("cppbinding").def(
            "test_with_gil",
            [](int expected, const IntStruct &in) {
                std::this_thread::sleep_for(std::chrono::milliseconds(5));
                if (in.value != expected) {
                    throw std::runtime_error("Value changed!!");
                }
            });

        pybind11::class_<Pickleable> cp(M("cppbinding"), "Pickleable", "");
        cp.def(pybind11::init<std::string>());
        cp.def("value", &Pickleable::value);
        cp.def("extra", &Pickleable::extra);
        cp.def("setExtra", &Pickleable::setExtra);
        cp.def(pybind11::pickle(
          [](const Pickleable &p) { // __getstate__
              /* Return a tuple that fully encodes the state of the object */
              return pybind11::make_tuple(p.value(), p.extra());
          },
          [](pybind11::tuple t) { // __setstate__
              if (t.size() != 2)
                  throw std::runtime_error("Invalid state!");

              /* Create a new C++ instance */
              Pickleable p(t[0].cast<std::string>());

              /* Assign any additional state */
              p.setExtra(t[1].cast<int>());

              return p;
          }
        ));

    }

}
