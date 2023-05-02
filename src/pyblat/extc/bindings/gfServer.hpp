#include <netdb.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdarg.h>
#include <sys/socket.h>

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
void genoPcrDirect(char *fPrimer, char *rPrimer, int fileCount,
                   char *seqFiles[]);
int getPortIx(char *portName);

/* Handle a query for DNA/DNA match. */
void dnaQuery(struct genoFind *gf, struct dnaSeq *seq, int connectionHandle,
              struct hash *perSeqMaxHash);

void transQuery(struct genoFind *transGf[2][3], aaSeq *seq,
                int connectionHandle);

void transTransQuery(struct genoFind *transGf[2][3], struct dnaSeq *seq,
                     int connectionHandle);

boolean badPcrPrimerSeq(char *s);

/* Load up index and hang out in RAM. */
void startServer(char *hostName, char *portName, int fileCount,
                 char *seqFiles[]);

void stopServer(char *hostName, char *portName);
int statusServer(char *hostName, char *portName);

void queryServer(char *type, char *hostName, char *portName, char *faName,
                 boolean complex, boolean isProt);

/* Do a PCR query to server daemon. */
void pcrServer(char *hostName, char *portName, char *fPrimer, char *rPrimer,
               int maxSize);

void getFileList(char *hostName, char *portName);

void gfServer();
