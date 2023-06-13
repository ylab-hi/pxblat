#ifndef PYGF_SERVER_HPP
#define PYGF_SERVER_HPP

#include "gfServer.hpp"

namespace cppbinding {

void pyerrorSafeQuery(boolean doTrans, boolean queryIsProt, struct dnaSeq *seq, struct genoFindIndex *gfIdx,
                      int connectionHandle, char *buf, struct hash *perSeqMaxHash, ServerOption const &options,
                      UsageStats &stats, boolean &sendOk);

boolean pynetSendString(int sd, char *s);

void pyerrSendString(int sd, char *s, boolean &sendOk);

void handle_client(int connectionHandle, std::string hostName, std::string portName, int fileCount,
                   std::vector<std::string> const &seqFiles, hash *perSeqMaxHash, genoFindIndex *gfIdx,
                   ServerOption const &option);

int pystartServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
                  ServerOption &options, UsageStats &stats);

}  // namespace cppbinding

#endif  // !#ifndef PYGF_SERVER_HPP
