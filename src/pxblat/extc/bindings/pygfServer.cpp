#include <stdexcept>
#pragma GCC diagnostic ignored "-Wwrite-strings"

#include "bs_thread_pool.hpp"
#include "dbg.h"
#include "gfServer.hpp"
#include "pygfServer.hpp"

namespace cppbinding {

void pyerrorSafeQuery(boolean doTrans, boolean queryIsProt, struct dnaSeq *seq, struct genoFindIndex *gfIdx,
                      int connectionHandle, char *buf, struct hash *perSeqMaxHash, ServerOption const &options,
                      UsageStats &stats, boolean &sendOk)
/* Wrap error handling code around index query.
 *
 * This used to duplicate errorSafeQuery's body (gfServer.cpp) with its
 * setjmp/longjmp recovery commented out, so a kent abort during a query
 * (e.g. out of memory) fell through to the default abort handler, which
 * terminates the process, killing the whole server instead of just this
 * request. errorSafeQuery already does this safely: it pushes gfAbort as
 * the abort handler and recovers via setjmp/longjmp entirely within kent C
 * code -- transQuery/transTransQuery/dnaQuery and everything they call are
 * plain kent C, not C++, so no C++ destructors sit between the setjmp and a
 * potential longjmp and none are skipped. Its jmp_buf and abort handler
 * (gfRecover/gfAbort) are file-static to gfServer.cpp and not reachable
 * from here, so rather than duplicate that setjmp/longjmp machinery a
 * second time, this simply delegates to it. */
{
  errorSafeQuery(doTrans, queryIsProt, seq, gfIdx, connectionHandle, buf, perSeqMaxHash, options, stats, sendOk);
}

boolean pynetSendString(int sd, char *s)
/* Send a string down a socket - length byte first. */
{
  int length = strlen(s);
  UBYTE len;

  if (length > 255) throw std::runtime_error("Trying to send a string longer than 255 bytes");
  len = length;
  if (write(sd, &len, 1) < 0) {
    warn("Couldn't send string to socket");
    return FALSE;
  }
  if (write(sd, s, length) < 0) {
    warn("Couldn't send string to socket");
    return FALSE;
  }
  return TRUE;
}

void pyerrSendString(int sd, char *s, boolean &sendOk)
// Send string. If not OK, remember we had an error, do not try to write
// anything more on this connection.
{
  if (sendOk) sendOk = pynetSendString(sd, s);
}

void handle_client(int connectionHandle, std::string hostName, std::string portName, int fileCount,
                   std::vector<std::string> const &seqFiles, hash *perSeqMaxHash, genoFindIndex *gfIdx,
                   ServerOption const &option, ServerStopControl *stopControl) {
  /* A failing query (including one of our own throws below) must never
   * escape into BS::thread_pool's worker() -- it invokes tasks as a plain
   * std::function<void()> call with no try/catch of its own, so an
   * uncaught exception here would call std::terminate() and take the whole
   * process down with it. */
  try {
    // dbg("begin func ", connectionHandle, hostName, portName, fileCount, seqFiles, perSeqMaxHash, gfIdx, option);

    // print current thread id

    dbg("thread id: ", std::this_thread::get_id());

    // auto ipLog = option.ipLog;
    auto minMatch = option.minMatch;
    // auto maxGap = option.maxGap;
    auto tileSize = option.tileSize;
    // auto repMatch = option.repMatch;
    auto stepSize = option.stepSize;
    auto timeout = option.timeout;
    auto maxAaSize = option.maxAaSize;
    auto maxNtSize = option.maxNtSize;

    boolean seqLog = bool2boolean(option.seqLog);
    boolean canStop = bool2boolean(option.canStop);
    boolean doTrans = bool2boolean(option.trans);
    // boolean doMask = bool2boolean(option.mask);
    // boolean allowOneMismatch = bool2boolean(option.allowOneMismatch);
    // boolean noSimpRepMask = bool2boolean(option.noSimpRepMask);

    boolean sendOk = TRUE;
    UsageStats stats{};

    char buf[256];
    char *line{nullptr};
    char *command{nullptr};

    setSocketTimeout(connectionHandle, timeout);

    int readSize = read(connectionHandle, buf, sizeof(buf) - 1);

    if (readSize < 0) {
      warn("Error reading from socket: %s", strerror(errno));
      ++stats.warnCount;
      close(connectionHandle);
      return;
    }

    if (readSize == 0) {
      // warn("Zero sized query");
      dbg("Zero sized query");
      ++stats.warnCount;
      close(connectionHandle);
      return;
    }

    buf[readSize] = 0;
    // logDebug("%s", buf);
    if (!startsWith(gfSignature(), buf)) {
      ++stats.noSigCount;
      close(connectionHandle);
      return;
    }

    line = buf + strlen(gfSignature());
    command = nextWord(&line);
    dbg("receive", command);

    if (sameString("quit", command)) {
      /* A quit message only takes the server down if it was started with
       * -canStop (mirrors gfServer.cpp's synchronous startServer()), and
       * even then this must not terminate the process directly: this
       * handler runs on a BS::thread_pool worker thread, and abruptly
       * ending the process from a non-main thread while sibling worker
       * threads may be mid-request risks running global/static destructors
       * concurrently with other threads still using them. Instead, flip a
       * shared flag that pystartServer's accept loop polls, so it stops
       * accepting new connections and returns normally. Also close the
       * listening socket here and now (not just wait for the accept loop's
       * own poll): this makes any new connection attempt fail fast with
       * ECONNREFUSED instead of racing a still-open backlog against this
       * process's eventual exit, which could otherwise get a client
       * connection accepted into the kernel backlog moments before the
       * process dies and the kernel resets it. */
      if (canStop) {
        logInfo("quit command received, stopping server");
        if (stopControl != nullptr) {
          stopControl->requested.store(true, std::memory_order_release);
          int listenFd = stopControl->listenSocket.exchange(-1, std::memory_order_acq_rel);
          if (listenFd >= 0) close(listenFd);
        }
      } else {
        logError("Ignoring quit message");
      }
      close(connectionHandle);
      return;
    }

    if (sameString("status", command) || sameString("transInfo", command) || sameString("untransInfo", command)) {
      // sleep 10 s
      sleep(10);
      snprintf(buf, sizeof(buf), "version %s", gfVersion);
      pyerrSendString(connectionHandle, buf, sendOk);
      pyerrSendString(connectionHandle, "serverType static", sendOk);
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "type %s", (doTrans ? "translated" : "nucleotide"));
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "host %s", hostName.data());
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "port %s", portName.data());
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "tileSize %d", tileSize);
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "stepSize %d", stepSize);
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "minMatch %d", minMatch);
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "pcr requests %ld", stats.pcrCount);
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "blat requests %ld", stats.blatCount);
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "bases %ld", stats.baseCount);
      pyerrSendString(connectionHandle, buf, sendOk);
      if (doTrans) {
        snprintf(buf, sizeof(buf), "aa %ld", stats.aaCount);
        pyerrSendString(connectionHandle, buf, sendOk);
      }
      snprintf(buf, sizeof(buf), "misses %d", stats.missCount);
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "noSig %d", stats.noSigCount);
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "trimmed %d", stats.trimCount);
      pyerrSendString(connectionHandle, buf, sendOk);
      snprintf(buf, sizeof(buf), "warnings %d", stats.warnCount);
      pyerrSendString(connectionHandle, buf, sendOk);
      pyerrSendString(connectionHandle, "end", sendOk);
    } else if (sameString("query", command) || sameString("protQuery", command) || sameString("transQuery", command)) {
      boolean queryIsProt = sameString(command, "protQuery");
      char *s = nextWord(&line);
      if (s == NULL || !isdigit(s[0])) {
        warn("Expecting query size after query command");
        ++stats.warnCount;
      } else {
        struct dnaSeq seq;
        ZeroVar(&seq);

        if (queryIsProt && !doTrans) {
          warn("protein query sent to nucleotide server");
          ++stats.warnCount;
          queryIsProt = FALSE;
        } else {
          buf[0] = 'Y';
          if (write(connectionHandle, buf, 1) == 1) {
            seq.size = atoi(s);
            seq.name = NULL;
            if (seq.size > 0) {
              ++stats.blatCount;
              seq.dna = (char *)needLargeMem(seq.size + 1);
              if (gfReadMulti(connectionHandle, seq.dna, seq.size) != seq.size) {
                warn("Didn't sockRecieveString all %d bytes of query sequence", seq.size);
                ++stats.warnCount;
              } else {
                dbg("query", seq.dna);

                int maxSize = (doTrans ? maxAaSize : maxNtSize);

                seq.dna[seq.size] = 0;
                if (queryIsProt) {
                  seq.size = aaFilteredSize(seq.dna);
                  aaFilter(seq.dna, seq.dna);
                } else {
                  seq.size = dnaFilteredSize(seq.dna);
                  dnaFilter(seq.dna, seq.dna);
                }
                if (seq.size > maxSize) {
                  ++stats.trimCount;
                  seq.size = maxSize;
                  seq.dna[maxSize] = 0;
                }
                if (queryIsProt)
                  stats.aaCount += seq.size;
                else
                  stats.baseCount += seq.size;
                if (seqLog && (logGetFile() != NULL)) {
                  FILE *lf = logGetFile();
                  faWriteNext(lf, "query", seq.dna, seq.size);
                  fflush(lf);
                }
                errorSafeQuery(doTrans, queryIsProt, &seq, gfIdx, connectionHandle, buf, perSeqMaxHash, option, stats,
                               sendOk);
                if (perSeqMaxHash) hashZeroVals(perSeqMaxHash);
              }
              freez(&seq.dna);
            }
            pyerrSendString(connectionHandle, "end", sendOk);
          }
        }
      }
    } else if (sameString("pcr", command)) {
      char *f = nextWord(&line);
      char *r = nextWord(&line);
      char *s = nextWord(&line);
      int maxDistance;
      ++stats.pcrCount;
      if (s == NULL || !isdigit(s[0])) {
        warn("Badly formatted pcr command");
        ++stats.warnCount;
      } else if (doTrans) {
        warn("Can't pcr on translated server");
        ++stats.warnCount;
      } else if (badPcrPrimerSeq(f) || badPcrPrimerSeq(r)) {
        warn("Can only handle ACGT in primer sequences.");
        ++stats.warnCount;
      } else {
        maxDistance = atoi(s);
        errorSafePcr(gfIdx->untransGf, f, r, maxDistance, connectionHandle, sendOk);
      }
    } else if (sameString("files", command)) {
      int i;
      snprintf(buf, sizeof(buf), "%d", fileCount);
      pyerrSendString(connectionHandle, buf, sendOk);
      for (i = 0; i < fileCount; ++i) {
        snprintf(buf, sizeof(buf), "%s", seqFiles[i].data());
        pyerrSendString(connectionHandle, buf, sendOk);
      }
    } else {
      warn("Unknown command %s", command);
      ++stats.warnCount;
    }
    close(connectionHandle);
    // connectionHandle = 0;
  } catch (const std::exception &e) {
    logError("handle_client: unhandled exception: %s", e.what());
    fprintf(stderr, "handle_client: unhandled exception: %s\n", e.what());
    close(connectionHandle);
  } catch (...) {
    logError("handle_client: unhandled unknown exception");
    fprintf(stderr, "handle_client: unhandled unknown exception\n");
    close(connectionHandle);
  }
}

int pystartServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
                  ServerOption &option, UsageStats &stats) {
  std::vector<char *> cseqFiles{};
  cseqFiles.reserve(seqFiles.size());
  for (auto &string : seqFiles) {
    cseqFiles.push_back(string.data());
  }

  struct sockaddr_in6 fromAddr;
  socklen_t fromLen;

  int socketHandle = 0;
  int port = atoi(portName.data());

  hash *perSeqMaxHash = nullptr;
  genoFindIndex *gfIdx = pybuildIndex4Server(hostName, portName, fileCount, cseqFiles.data(), perSeqMaxHash, option);

  /* pybuildIndex4Server() heap-allocates gfIdx (and may populate
   * perSeqMaxHash); neither was ever freed on any exit path. `pool` is
   * declared after this guard on purpose: C++ destroys locals in reverse
   * declaration order, so on every exit from this function -- a normal
   * return or a thrown exception -- `pool`'s destructor (which joins every
   * worker thread) runs first, guaranteeing no handle_client() task is
   * still reading gfIdx/perSeqMaxHash, and only then does this guard free
   * them, exactly once. */
  struct IndexGuard {
    genoFindIndex **gfIdxPtr;
    hash **perSeqMaxHashPtr;
    ~IndexGuard() {
      if (*gfIdxPtr != nullptr) genoFindIndexFree(gfIdxPtr);
      if (*perSeqMaxHashPtr != nullptr) hashFree(perSeqMaxHashPtr);
    }
  } indexGuard{&gfIdx, &perSeqMaxHash};

  ServerStopControl stopControl;
  BS::thread_pool pool(option.threads);

  /* Set up socket.  Get ready to listen to it. */
  socketHandle = netAcceptingSocket(port, 100);
  if (socketHandle < 0)
    throw std::runtime_error("Fatal Error: Unable to open listening socket on port " + portName + ".");
  stopControl.listenSocket.store(socketHandle, std::memory_order_release);

  /* Let accept() time out periodically too, as a fallback: it covers the
   * canStop=false case (no one will ever close listenSocket) and the
   * window before stopControl.listenSocket is published above. The normal
   * stop path closes the listening socket directly from handle_client(),
   * which both unblocks a concurrently-blocked accept() and immediately
   * refuses any new connection instead of leaving it racing shutdown. */
  setSocketTimeout(socketHandle, 1);

  int connectFailCount = 0;
  while (!stopControl.requested.load(std::memory_order_acquire)) {
    ZeroVar(&fromAddr);
    fromLen = sizeof(fromAddr);
    int connectionHandle = accept(socketHandle, (struct sockaddr *)&fromAddr, &fromLen);

    // setSendOk(sendOk);

    if (connectionHandle < 0) {
      if (errno == EAGAIN || errno == EWOULDBLOCK) continue; /* accept() timeout; re-check stopControl.requested */
      warn("Error accepting the connection");
      ++stats.warnCount;
      ++connectFailCount;

      if (connectFailCount >= 100)
        throw std::runtime_error(
            "100 continuous connection failures, no point in filling up the log in an infinite loop.");
      continue;
    } else {
      connectFailCount = 0;
    }

    // dbg("before ", connectionHandle, hostName, portName, fileCount, seqFiles, perSeqMaxHash, gfIdx, option);
    // handle_client(connectionHandle, hostName, portName, fileCount, seqFiles, perSeqMaxHash, gfIdx, option);
    pool.push_task(handle_client, connectionHandle, hostName, portName, fileCount, seqFiles, perSeqMaxHash, gfIdx,
                   option, &stopControl);
  }

  pool.wait_for_tasks();

  int remainingFd = stopControl.listenSocket.exchange(-1, std::memory_order_acq_rel);
  if (remainingFd >= 0) close(remainingFd);
  return 0;
}

}  // namespace cppbinding
