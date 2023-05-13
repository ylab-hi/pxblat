#ifndef PYGF_SERVER_HPP
#define PYGF_SERVER_HPP

#include "gfServer.hpp"

namespace cppbinding {

boolean pynetSendString(int sd, char *s);

void pyerrSendString(int sd, char *s, boolean &sendOk);

void handle_client(int connectionHandle, std::string hostName, std::string portName, int fileCount,
                   std::vector<std::string> const &seqFiles, hash *perSeqMaxHash, genoFindIndex *gfIdx,
                   gfServerOption const &option);

int pystartServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
                  gfServerOption &options, UsageStats &stats, Signal &signal);

}  // namespace cppbinding

#endif  // !#ifndef PYGF_SERVER_HPP
