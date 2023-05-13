#ifndef EPYGF_SERVER_HPP
#define EPYGF_SERVER_HPP

#include "bs_thread_pool.hpp"
#include "gfServer.hpp"
using namespace cppbinding;

namespace ecppbinding2 {

int pystartServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
                  gfServerOption &options, UsageStats &stats, Signal &signal);

}

#endif
