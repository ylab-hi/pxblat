#include <netdb.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdarg.h>
#include <sys/socket.h>

#include <string>
#include <vector>

#include "common.h"
#include "dnaseq.h"
#include "dnautil.h"
#include "dystring.h"
#include "errAbort.h"
#include "fa.h"
#include "filePath.h"
#include "genoFind.h"
#include "hash.h"
#include "internet.h"
#include "log.h"
#include "memalloc.h"
#include "net.h"
#include "nib.h"
#include "options.h"
#include "portable.h"
#include "trans3.h"
#include "twoBit.h"

constexpr int maxNtSize = 40000;
constexpr int maxAaSize = 8000;

constexpr int minMatch = gfMinMatch; /* Can be overridden from command line. */
constexpr int tileSize = gfTileSize; /* Can be overridden from command line. */
constexpr int stepSize = 0;          /* Can be overridden from command line. */
boolean doTrans = FALSE;             /* Do translation? */
boolean allowOneMismatch = FALSE;
boolean noSimpRepMask = FALSE;
constexpr int repMatch = 1024;    /* Can be overridden from command line. */
constexpr int maxDnaHits = 100;   /* Can be overridden from command line. */
constexpr int maxTransHits = 200; /* Can be overridden from command line. */
constexpr int maxGap = gfMaxGap;
boolean seqLog = FALSE;
boolean ipLog = FALSE;
boolean doMask = FALSE;
boolean canStop = FALSE;
char *indexFile = NULL;
char *genome = NULL;
char *genomeDataDir = NULL;

constexpr int timeout = 90;  // default timeout in seconds

void usage();
void setSendOk();
void errSendString(int sd, char *s);
void errSendLongString(int sd, char *s);
void logGenoFind(struct genoFind *gf);
void logGenoFindIndex(struct genoFindIndex *gfIdx);
void genoFindDirect(char *probeName, int fileCount, char *seqFiles[]);
void genoPcrDirect(char *fPrimer, char *rPrimer, int fileCount, char *seqFiles[]);
int getPortIx(char *portName);

/* Handle a query for DNA/DNA match. */
void dnaQuery(struct genoFind *gf, struct dnaSeq *seq, int connectionHandle, struct hash *perSeqMaxHash);

void transQuery(struct genoFind *transGf[2][3], aaSeq *seq, int connectionHandle);

void transTransQuery(struct genoFind *transGf[2][3], struct dnaSeq *seq, int connectionHandle);

boolean badPcrPrimerSeq(char *s);

/* Load up index and hang out in RAM. */
void startServer(char *hostName, char *portName, int fileCount, char *seqFiles[]);

void startServer(std::string const &hostName, std::string const &portName, int fileCount,
                 std::vector<std::string> const &seqFiles);

void stopServer(char *hostName, char *portName);
void stopServer(std::string const &hostName, std::string const &portName);

int statusServer(char *hostName, char *portName);
int statusServer(std::string const &hostName, std::string const &portName);

void queryServer(char *type, char *hostName, char *portName, char *faName, boolean complex, boolean isProt);
void queryServer(std::string const &type, std::string const &*hostName, std::string const &portName,
                 std::string const &faName, bool complex, bool isProt);

/* Do a PCR query to server daemon. */
void pcrServer(char *hostName, char *portName, char *fPrimer, char *rPrimer, int maxSize);

void pcrServer(std::string const &hostName, std::string const &portName, std::string const &fPrimer,
               std::string const &rPrimer, int maxSize);

void getFileList(char *hostName, char *portName);
void getFileList(std::string const &hostName, std::string const &portName);

"                   -maxDnaHits will be applied to each filename[:seq] "
    "separately: each may\n"
    "                   have at most maxDnaHits/2 hits.  The filename MUST "
    "not include the directory.\n"
    "                   Useful for assemblies with many alternate/patch "
    "sequences.\n"

    struct gfServerOption {
  bool canStop{};              // -canStop      If set, a quit message will actually take down the server.
  std::string log{};           // -log=logFile  Keep a log file that records server requests.
  std::string &logFacility{};  // -logFacility=facility  Log to the specified syslog facility default local0
  bool mask{};                 // -mask   Use masking from .2bit file.
  int maxAaSize{};             //  -maxAaSize=N  Maximum size of protein or translated DNA queries."
  int maxDnaHits{};  //-maxDnaHits=N   Maximum number of hits for a DNA query that are sent from the server"
  int maxGap{};      //-maxGap=N    Number of insertions or deletions allowed between n-mers. Default is 2 for
                     // nucleotides, 0 for proteins"
  int maxNtSize{};   // -maxNtSize=N    Maximum size of untranslated DNA query sequence
  int maxTranshHits{};  //-maxTransHits=N Maximum number of hits for a translated query that are sent from the
                        // server"
  int minMatch{};       //-minMatch=N   Number of n-mer matches that trigger detailed alignment Default
                        // is 2 for nucleotides, 3 for proteins
  int repMatch{};       //-repMatch=N    Number of occurrences of a tile (n-mer) that triggers repeat masking
                        // the  tile
  bool seqLog{};        //-seqLog   Include sequences in log file (not logged with  -syslog)
  bool ipLog{};         //-ipLog    Include user's IP in log file (not logged with -syslog)
  bool debugLog{};      //-debugLog   Include debugging info in log file
  int setpSize{};       //-stepSize=N     Spacing between tiles. Default is tileSize
  int tileSize{};       //-tileSize=N   Size of n-mers to index.  Default is 11 for nucleotides, 4 for
                        // proteins (or translated nucleotides)
  bool trans{};         //-trans      Translate database to protein in 6 frames.  Note: it is best to run
                        // this on RepeatMasked data in this case
  bool syslog{};        //-syslog     Log to syslog.
  std::string
      perSeqMax{};  //-perSeqMax=file File contains one seq filename (possibly with ':seq' suffix) per line
  bool noSimpRepMask{};     // -noSimpRepMask  Suppresses simple repeat masking
  std::string indexFile{};  // -indexFile   Index file create by `gfServer index'. Saving index  can
                            // speed up gfServer startup by two orders of magnitude.
                            // The parameters must  exactly match the parameters when
                            // the file is written or bad things  will happen
  std::string genome{};
  std::string genomeDataDir{};
  int timeout{};  //-timeout=N  Timeout in seconds
}


void gfServer(
    

);
