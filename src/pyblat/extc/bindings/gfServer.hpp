#include <netdb.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdarg.h>
#include <sys/socket.h>

#include <cstring>
#include <ctime>
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

// constexpr int stepSize = 0; /* Can be overridden from command line. */

// boolean doTrans = FALSE; /* Do translation? */
// boolean allowOneMismatch = FALSE;
// boolean noSimpRepMask = FALSE;
// constexpr int repMatch = 1024; /* Can be overridden from command line. */
// constexpr int maxGap = gfMaxGap;
// boolean seqLog = FALSE;
// boolean ipLog = FALSE;
// boolean doMask = FALSE;
// boolean canStop = FALSE;
// char *indexFile = NULL;
// char *genome = NULL;
// char *genomeDataDir = NULL;

// constexpr int timeout = 90;  // default timeout in seconds

// {self.gfserver} -canStop -log={self.log_file_path} -stepSize=5 start "
//             f"localhost {self.port} {os.path.basename(self.ref_2bit)}"

struct gfServerOption {
  using self = gfServerOption;
  bool canStop{false};        //-canStop      If set, a quit message will actually take down the server.
  std::string log{};          //-log=logFile  Keep a log file that records server requests.
  std::string logFacility{};  //-logFacility=facility  Log to the specified syslog facility default local0
  bool mask{};                //-mask   Use masking from .2bit file.
  int maxAaSize{8000};        //-maxAaSize=N  Maximum size of protein or translated DNA queries."
  int maxDnaHits{100};        //-maxDnaHits=N   Maximum number of hits for a DNA query that are sent from the server"
  int maxGap{gfMaxGap};       //-maxGap=N    Number of insertions or deletions allowed between n-mers. Default is 2 for
                              // nucleotides, 0 for proteins"
  int maxNtSize{40000};       //-maxNtSize=N    Maximum size of untranslated DNA query sequence
  int maxTranshHits{200};     //-maxTransHits=N Maximum number of hits for a translated query that are sent from the
                              // server"
  int minMatch{gfMinMatch};   //-minMatch=N   Number of n-mer matches that trigger detailed alignment Default
                              // is 2 for nucleotides, 3 for proteins
  int repMatch{};             //-repMatch=N    Number of occurrences of a tile (n-mer) that triggers repeat masking
                              // the  tile
  bool seqLog{false};         //-seqLog   Include sequences in log file (not logged with  -syslog)
  bool ipLog{false};          //-ipLog    Include user's IP in log file (not logged with -syslog)
  bool debugLog{false};       //-debugLog   Include debugging info in log file

  int tileSize{gfTileSize};   //-tileSize=N   Size of n-mers to index.  Default is 11 for nucleotides, 4 for
  int setpSize{tileSize};     //-stepSize=N     Spacing between tiles. Default is tileSize
                              // proteins (or translated nucleotides)
  bool trans{false};          //-trans      Translate database to protein in 6 frames.  Note: it is best to run
                              // this on RepeatMasked data in this case
  bool syslog{};              //-syslog     Log to syslog.
  std::string perSeqMax{};    //-perSeqMax=file File contains one seq filename (possibly with ':seq' suffix) per line
  bool noSimpRepMask{false};  //-noSimpRepMask  Suppresses simple repeat masking
  std::string indexFile{};    //-indexFile   Index file create by `gfServer index'. Saving index  can
                              // speed up gfServer startup by two orders of magnitude.
                              // The parameters must  exactly match the parameters when
                              // the file is written or bad things  will happen
  int timeout{90};            //-timeout=N  Timeout in seconds
  std::string genome{};
  std::string genomeDataDir{};

  bool allowOneMismatch{false};

  gfServerOption() = default;

  self &build();
};

void gfServer();
bool boolean2bool(boolean b);
boolean bool2boolean(bool b);
void usage();
void setSendOk();
void errSendString(int sd, char *s);
void errSendLongString(int sd, char *s);
void logGenoFind(struct genoFind *gf);
void logGenoFindIndex(struct genoFindIndex *gfIdx);

// void genoFindDirect(char *probeName, int fileCount, char *seqFiles[]);
void genoFindDirect(std::string &probeName, int fileCount, std::vector<std::string> &seqFiles,
                    gfServerOption const &options);

// void genoPcrDirect(char *fPrimer, char *rPrimer, int fileCount, char *seqFiles[]);
void genoPcrDirect(std::string &fPrimer, std::string &rPrimer, int fileCount, std::vector<std::string> &seqFiles,
                   gfServerOption const &options);

int getPortIx(char *portName);

/* Handle a query for DNA/DNA match. */
void dnaQuery(struct genoFind *gf, struct dnaSeq *seq, int connectionHandle, struct hash *perSeqMaxHash);

void transQuery(struct genoFind *transGf[2][3], aaSeq *seq, int connectionHandle);

void transTransQuery(struct genoFind *transGf[2][3], struct dnaSeq *seq, int connectionHandle);

boolean badPcrPrimerSeq(char *s);

/* Load up index and hang out in RAM. */
// void startServer(char *hostName, char *portName, int fileCount, char *seqFiles[]);
void startServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
                 gfServerOption &options);

void stopServer(char *hostName, char *portName);
void stopServer(std::string const &hostName, std::string const &portName);

int statusServer(char *hostName, char *portName);
int statusServer(std::string const &hostName, std::string const &portName);

void queryServer(char *type, char *hostName, char *portName, char *faName, boolean complex, boolean isProt);
void queryServer(std::string const &type, std::string const &hostName, std::string const &portName,
                 std::string const &faName, bool complex, bool isProt);

/* Do a PCR query to server daemon. */
void pcrServer(char *hostName, char *portName, char *fPrimer, char *rPrimer, int maxSize);

void pcrServer(std::string const &hostName, std::string const &portName, std::string const &fPrimer,
               std::string const &rPrimer, int maxSize);

void getFileList(char *hostName, char *portName);
void getFileList(std::string const &hostName, std::string const &portName);
