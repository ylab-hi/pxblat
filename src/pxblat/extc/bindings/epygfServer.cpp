#pragma GCC diagnostic ignored "-Wwrite-strings"
#include "epygfServer.hpp"

namespace ecppbinding2 {

boolean pynetSendString(int sd, char *s)
/* Send a string down a socket - length byte first. */
{
  int length = strlen(s);
  UBYTE len;

  if (length > 255)
    // errAbort("Trying to send a string longer than 255 bytes (%d bytes)", length);
    throw std::runtime_error("Trying to send a string longer than 255 bytes");
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

void py_server_status(int connectionHandle, char const *hostName, char const *portName, boolean doTrans, int minMatch,
                      int stepSize, int tileSize, UsageStats const &stats) {
  char buf[256];
  boolean sendOk = TRUE;

  sprintf(buf, "version %s", gfVersion);
  pyerrSendString(connectionHandle, buf, sendOk);
  pyerrSendString(connectionHandle, "serverType static", sendOk);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "type %s", (doTrans ? "translated" : "nucleotide"));
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "host %s", hostName);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "port %s", portName);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "tileSize %d", tileSize);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "stepSize %d", stepSize);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "minMatch %d", minMatch);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "pcr requests %ld", stats.pcrCount);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "blat requests %ld", stats.blatCount);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "bases %ld", stats.baseCount);
  pyerrSendString(connectionHandle, buf, sendOk);
  if (doTrans) {
    sprintf(buf, "aa %ld", stats.aaCount);
    pyerrSendString(connectionHandle, buf, sendOk);
  }
  sprintf(buf, "misses %d", stats.missCount);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "noSig %d", stats.noSigCount);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "trimmed %d", stats.trimCount);
  pyerrSendString(connectionHandle, buf, sendOk);
  sprintf(buf, "warnings %d", stats.warnCount);
  pyerrSendString(connectionHandle, buf, sendOk);
  pyerrSendString(connectionHandle, "end", sendOk);
}

void py_server_query(int connectionHandle, int seq_size, hash *perSeqMaxHash, genoFindIndex *gfIdx, boolean queryIsProt,
                     gfServerOption &options, boolean sendOk) {
  UsageStats stats{};
  auto maxAaSize = options.maxAaSize;
  auto maxNtSize = options.maxNtSize;

  boolean doTrans = bool2boolean(options.trans);

  struct dnaSeq seq;
  ZeroVar(&seq);

  char buf[4];
  buf[0] = 'Y';

  if (write(connectionHandle, buf, 1) == 1) {
    seq.size = seq_size;
    seq.name = NULL;
    if (seq.size > 0) {
      ++stats.blatCount;
      seq.dna = (char *)needLargeMem(seq.size + 1);
      if (gfReadMulti(connectionHandle, seq.dna, seq.size) != seq.size) {
        warn("Didn't sockRecieveString all %d bytes of query sequence", seq.size);
        ++stats.warnCount;
      } else {
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

        errorSafeQuery(doTrans, queryIsProt, &seq, gfIdx, connectionHandle, buf, perSeqMaxHash, options, stats, sendOk);
        if (perSeqMaxHash) hashZeroVals(perSeqMaxHash);
      }
      freez(&seq.dna);
    }
    errSendString(connectionHandle, "end", sendOk);
  }
}

/* error code
 * -1 errAbort("Fatal Error: Unable to open listening socket on port %d.", port)
  -2 errAbort( "100 continuous connection failures, no point in filling up "
            "the log in an infinite loop.");
 */
int pystartServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
                  gfServerOption &options, UsageStats &stats, Signal &signal)
/* Load up index and hang out in RAM. */
{
  BS::thread_pool pool{4};

  auto indexFile = options.indexFile.empty() ? NULL : options.indexFile.data();

  auto ipLog = options.ipLog;
  auto minMatch = options.minMatch;
  auto maxGap = options.maxGap;
  auto tileSize = options.tileSize;
  auto repMatch = options.repMatch;
  auto stepSize = options.stepSize;
  auto timeout = options.timeout;
  auto maxAaSize = options.maxAaSize;
  auto maxNtSize = options.maxNtSize;

  boolean seqLog = bool2boolean(options.seqLog);
  boolean canStop = bool2boolean(options.canStop);
  boolean doTrans = bool2boolean(options.trans);
  boolean doMask = bool2boolean(options.mask);
  boolean allowOneMismatch = bool2boolean(options.allowOneMismatch);
  boolean noSimpRepMask = bool2boolean(options.noSimpRepMask);

  boolean sendOk = TRUE;

  printf("optons: %s, %s, %d, %zu, %d, %d, %d, %d, %d, %d, %d, %d\n", hostName.data(), portName.data(), fileCount,
         seqFiles.size(), minMatch, maxGap, tileSize, repMatch, stepSize, timeout, maxAaSize, maxNtSize);

  std::vector<char *> cseqFiles{};
  cseqFiles.reserve(seqFiles.size());
  for (auto &string : seqFiles) {
    cseqFiles.push_back(string.data());
  }

  char buf[256];
  char *line, *command;

  struct sockaddr_in6 fromAddr;
  socklen_t fromLen;
  int readSize;
  int socketHandle = 0, connectionHandle = 0;
  int port = atoi(portName.data());

  struct hash *perSeqMaxHash;
  genoFindIndex *gfIdx = pybuildIndex4Server(hostName, portName, fileCount, cseqFiles.data(), perSeqMaxHash, options);

  /* Set up socket.  Get ready to listen to it. */
  socketHandle = netAcceptingSocket(port, 100);
  if (socketHandle < 0) return -1;

  signal.isReady = true;
  // logInfo("Server ready for queries!");
  // printf("Server ready for queries!\n");

  int connectFailCount = 0;
  for (;;) {
    ZeroVar(&fromAddr);
    fromLen = sizeof(fromAddr);
    connectionHandle = accept(socketHandle, (struct sockaddr *)&fromAddr, &fromLen);
    setSendOk(sendOk);

    if (connectionHandle < 0) {
      warn("Error accepting the connection");
      ++stats.warnCount;
      ++connectFailCount;
      if (connectFailCount >= 100) return -2;
      continue;
    } else {
      connectFailCount = 0;
    }
    setSocketTimeout(connectionHandle, timeout);

    readSize = read(connectionHandle, buf, sizeof(buf) - 1);
    if (readSize < 0) {
      warn("Error reading from socket: %s", strerror(errno));
      ++stats.warnCount;
      close(connectionHandle);
      continue;
    }

    if (readSize == 0) {
      warn("Zero sized query");
      ++stats.warnCount;
      close(connectionHandle);
      continue;
    }

    buf[readSize] = 0;
    logDebug("%s", buf);
    if (!startsWith(gfSignature(), buf)) {
      ++stats.noSigCount;
      close(connectionHandle);
      continue;
    }

    line = buf + strlen(gfSignature());
    command = nextWord(&line);

    if (sameString("quit", command)) {
      if (canStop)
        break;
      else
        logError("Ignoring quit message");

    } else if (sameString("status", command) || sameString("transInfo", command) ||
               sameString("untransInfo", command)) {
      pool.push_task(py_server_status, connectionHandle, hostName.data(), portName.data(), doTrans, minMatch, stepSize,
                     tileSize, stats);
      // py_server_status(connectionHandle, hostName.data(), portName.data(), doTrans, minMatch, stepSize, tileSize,
      // stats);
    } else if (sameString("query", command) || sameString("protQuery", command) || sameString("transQuery", command)) {
      char *s = nextWord(&line);
      if (s == NULL || !isdigit(s[0])) {
        warn("Expecting query size after query command");
        // ++stats.warnCount;
        continue;
      }

      int seqSize = atoi(s);
      boolean queryIsProt = sameString(command, "protQuery");
      if (queryIsProt && !doTrans) {
        warn("protein query sent to nucleotide server");
        ++stats.warnCount;
        queryIsProt = FALSE;
        continue;
      }

      py_server_query(connectionHandle, seqSize, perSeqMaxHash, gfIdx, queryIsProt, options, sendOk);

    } else if (sameString("pcr", command)) {
      char *f = nextWord(&line);
      char *r = nextWord(&line);
      char *s = nextWord(&line);
      // int maxDistance;

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
        int maxDistance = atoi(s);
        errorSafePcr(gfIdx->untransGf, f, r, maxDistance, connectionHandle, sendOk);
      }

    } else if (sameString("files", command)) {
      int i;
      sprintf(buf, "%d", fileCount);
      errSendString(connectionHandle, buf, sendOk);
      for (i = 0; i < fileCount; ++i) {
        sprintf(buf, "%s", seqFiles[i].data());
        errSendString(connectionHandle, buf, sendOk);
      }
    } else {
      warn("Unknown command %s", command);
      ++stats.warnCount;
    }
    close(connectionHandle);
    connectionHandle = 0;
  }
  close(socketHandle);

  pool.wait_for_tasks();
  return 0;
}

}  // namespace ecppbinding2
