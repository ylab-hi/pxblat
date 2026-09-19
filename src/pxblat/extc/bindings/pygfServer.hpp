#ifndef PYGF_SERVER_HPP
#define PYGF_SERVER_HPP

#include <atomic>

#include "gfServer.hpp"

namespace cppbinding {

struct ServerStopControl
/* Shared between pystartServer()'s accept loop (main thread) and
 * handle_client() (a BS::thread_pool worker thread) so a "quit" command
 * can ask the accept loop to stop gracefully instead of aborting the process.
 * listenSocket doubles as a single-owner flag: whichever side atomically
 * exchanges it to -1 is responsible for close()-ing it, so the listening
 * socket is closed exactly once no matter which side gets there first. */
{
  std::atomic<bool> requested{false};
  std::atomic<int> listenSocket{-1};
};

void pyerrorSafeQuery(boolean doTrans, boolean queryIsProt, struct dnaSeq *seq, struct genoFindIndex *gfIdx,
                      int connectionHandle, char *buf, struct hash *perSeqMaxHash, ServerOption const &options,
                      UsageStats &stats, boolean &sendOk);

boolean pynetSendString(int sd, char *s);

void pyerrSendString(int sd, char *s, boolean &sendOk);

void handle_client(int connectionHandle, std::string hostName, std::string portName, int fileCount,
                   std::vector<std::string> const &seqFiles, hash *perSeqMaxHash, genoFindIndex *gfIdx,
                   ServerOption const &option, ServerStopControl *stopControl);

int pystartServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
                  ServerOption &options, UsageStats &stats);

}  // namespace cppbinding

#endif  // !#ifndef PYGF_SERVER_HPP
