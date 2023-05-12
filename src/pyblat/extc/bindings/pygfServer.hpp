#ifndef PYGF_SERVER_HPP
#define PYGF_SERVER_HPP

#include "gfServer.hpp"
namespace cppbinding {

int pystartServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
                  gfServerOption &options, UsageStats &stats, Signal &signal);
}

#endif
