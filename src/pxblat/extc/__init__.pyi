"""Bindings for ::cppbinding namespace"""
from __future__ import annotations
import pxblat._extc.cppbinding
import typing

__all__ = [
    "IntStruct",
    "TwoBitToFaOption",
    "UsageStats",
    "buildIndex",
    "faToTwoBit",
    "genoFindDirect",
    "genoPcrDirect",
    "getFileList",
    "getPortIx",
    "ClientOption",
    "gfServer",
    "ServerOption",
    "pcrServer",
    "pygetFileList",
    "pygfClient",
    "pygfClient2",
    "pygfClient_no_gil",
    "pyqueryServer",
    "pystartServer",
    "pystartServer_no_gil",
    "pystatusServer",
    "queryServer",
    "startServer",
    "statusServer",
    "stopServer",
    "test",
    "test_add",
    "test_exception",
    "test_no_gil",
    "test_stat",
    "test_stdout",
    "test_with_gil",
    "twoBitToFa",
]

class IntStruct:
    def __init__(self, arg0: int) -> None: ...
    pass

class TwoBitToFaOption:
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: TwoBitToFaOption) -> None: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self) -> str: ...
    def build(self) -> TwoBitToFaOption:
        """
        C++: cppbinding::TwoBitToFaOption::build() --> struct cppbinding::TwoBitToFaOption &
        """
    def to_string(self) -> str:
        """
        C++: cppbinding::TwoBitToFaOption::to_string() --> std::string
        """
    def withBed(self, bed: str) -> TwoBitToFaOption:
        """
        C++: cppbinding::TwoBitToFaOption::withBed(std::string const &) --> struct cppbinding::TwoBitToFaOption &
        """
    def withBedPos(self, bedPos: bool) -> TwoBitToFaOption:
        """
        C++: cppbinding::TwoBitToFaOption::withBedPos(bool) --> struct cppbinding::TwoBitToFaOption &
        """
    def withBpt(self, bpt: str) -> TwoBitToFaOption:
        """
        C++: cppbinding::TwoBitToFaOption::withBpt(std::string const &) --> struct cppbinding::TwoBitToFaOption &
        """
    def withEnd(self, end: int) -> TwoBitToFaOption:
        """
        C++: cppbinding::TwoBitToFaOption::withEnd(int) --> struct cppbinding::TwoBitToFaOption &
        """
    def withNoMask(self, noMask: bool) -> TwoBitToFaOption:
        """
        C++: cppbinding::TwoBitToFaOption::withNoMask(bool) --> struct cppbinding::TwoBitToFaOption &
        """
    def withSeq(self, seq: str) -> TwoBitToFaOption:
        """
        C++: cppbinding::TwoBitToFaOption::withSeq(std::string const &) --> struct cppbinding::TwoBitToFaOption &
        """
    def withSeqList(self, seqList: str) -> TwoBitToFaOption:
        """
        C++: cppbinding::TwoBitToFaOption::withSeqList(std::string const &) --> struct cppbinding::TwoBitToFaOption &
        """
    def withStart(self, start: int) -> TwoBitToFaOption:
        """
        C++: cppbinding::TwoBitToFaOption::withStart(int) --> struct cppbinding::TwoBitToFaOption &
        """
    def withUdcDir(self, udcDir: str) -> TwoBitToFaOption:
        """
        C++: cppbinding::TwoBitToFaOption::withUdcDir(std::string const &) --> struct cppbinding::TwoBitToFaOption &
        """
    @property
    def bed(self) -> str:
        """
        :type: str
        """
    @bed.setter
    def bed(self, arg0: str) -> None:
        pass
    @property
    def bedPos(self) -> bool:
        """
        :type: bool
        """
    @bedPos.setter
    def bedPos(self, arg0: bool) -> None:
        pass
    @property
    def bpt(self) -> str:
        """
        :type: str
        """
    @bpt.setter
    def bpt(self, arg0: str) -> None:
        pass
    @property
    def end(self) -> int:
        """
        :type: int
        """
    @end.setter
    def end(self, arg0: int) -> None:
        pass
    @property
    def noMask(self) -> bool:
        """
        :type: bool
        """
    @noMask.setter
    def noMask(self, arg0: bool) -> None:
        pass
    @property
    def seq(self) -> str:
        """
        :type: str
        """
    @seq.setter
    def seq(self, arg0: str) -> None:
        pass
    @property
    def seqList(self) -> str:
        """
        :type: str
        """
    @seqList.setter
    def seqList(self, arg0: str) -> None:
        pass
    @property
    def start(self) -> int:
        """
        :type: int
        """
    @start.setter
    def start(self, arg0: int) -> None:
        pass
    @property
    def udcDir(self) -> str:
        """
        :type: str
        """
    @udcDir.setter
    def udcDir(self, arg0: str) -> None:
        pass
    pass

class UsageStats:
    def __getstate__(self) -> tuple: ...
    def __init__(self) -> None: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self) -> str: ...
    @property
    def aaCount(self) -> int:
        """
        :type: int
        """
    @aaCount.setter
    def aaCount(self, arg0: int) -> None:
        pass
    @property
    def baseCount(self) -> int:
        """
        :type: int
        """
    @baseCount.setter
    def baseCount(self, arg0: int) -> None:
        pass
    @property
    def blatCount(self) -> int:
        """
        :type: int
        """
    @blatCount.setter
    def blatCount(self, arg0: int) -> None:
        pass
    @property
    def missCount(self) -> int:
        """
        :type: int
        """
    @missCount.setter
    def missCount(self, arg0: int) -> None:
        pass
    @property
    def noSigCount(self) -> int:
        """
        :type: int
        """
    @noSigCount.setter
    def noSigCount(self, arg0: int) -> None:
        pass
    @property
    def pcrCount(self) -> int:
        """
        :type: int
        """
    @pcrCount.setter
    def pcrCount(self, arg0: int) -> None:
        pass
    @property
    def trimCount(self) -> int:
        """
        :type: int
        """
    @trimCount.setter
    def trimCount(self, arg0: int) -> None:
        pass
    @property
    def warnCount(self) -> int:
        """
        :type: int
        """
    @warnCount.setter
    def warnCount(self, arg0: int) -> None:
        pass
    pass

class ClientOption:
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: ClientOption) -> None: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self) -> str: ...
    def build(self) -> ClientOption:
        """
        C++: cppbinding::ClientOption::build() --> struct cppbinding::ClientOption &
        """
    def to_string(self) -> str:
        """
        C++: cppbinding::ClientOption::to_string() const --> std::string
        """
    def withDots(self, dots_: int) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withDots(int) --> struct cppbinding::ClientOption &
        """
    def withGenome(self, genome_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withGenome(const std::string &) --> struct cppbinding::ClientOption &
        """
    def withGenomeDataDir(self, genomeDataDir_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withGenomeDataDir(const std::string &) --> struct cppbinding::ClientOption &
        """
    def withHost(self, hostName_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withHost(const std::string &) --> struct cppbinding::ClientOption &
        """
    def withInName(self, inName_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withInName(const std::string &) --> struct cppbinding::ClientOption &
        """
    def withInSeq(self, inseq_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withInSeq(const std::string &) --> struct cppbinding::ClientOption &
        """
    def withIsDynamic(self, isDynamic_: bool) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withIsDynamic(bool) --> struct cppbinding::ClientOption &
        """
    def withMaxIntron(self, maxIntron_: int) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withMaxIntron(long) --> struct cppbinding::ClientOption &
        """
    def withMinIdentity(self, minIdentity_: float) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withMinIdentity(double) --> struct cppbinding::ClientOption &
        """
    def withMinScore(self, minScore_: int) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withMinScore(int) --> struct cppbinding::ClientOption &
        """
    def withNohead(self, nohead_: bool) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withNohead(bool) --> struct cppbinding::ClientOption &
        """
    def withOutName(self, outName_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withOutName(const std::string &) --> struct cppbinding::ClientOption &
        """
    def withOutputFormat(self, outputFormat_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withOutputFormat(const std::string &) --> struct cppbinding::ClientOption &
        """
    def withPort(self, portName_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withPort(const std::string &) --> struct cppbinding::ClientOption &
        """
    def withQType(self, qType_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withQType(const std::string &) --> struct cppbinding::ClientOption &
        """
    def withSeqDir(self, SeqDir_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withSeqDir(const std::string &) --> struct cppbinding::ClientOption &
        """
    def withTType(self, tType_: str) -> ClientOption:
        """
        C++: cppbinding::ClientOption::withTType(const std::string &) --> struct cppbinding::ClientOption &
        """
    @property
    def SeqDir(self) -> str:
        """
        :type: str
        """
    @SeqDir.setter
    def SeqDir(self, arg0: str) -> None:
        pass
    @property
    def dots(self) -> int:
        """
        :type: int
        """
    @dots.setter
    def dots(self, arg0: int) -> None:
        pass
    @property
    def genome(self) -> str:
        """
        :type: str
        """
    @genome.setter
    def genome(self, arg0: str) -> None:
        pass
    @property
    def genomeDataDir(self) -> str:
        """
        :type: str
        """
    @genomeDataDir.setter
    def genomeDataDir(self, arg0: str) -> None:
        pass
    @property
    def hostName(self) -> str:
        """
        :type: str
        """
    @hostName.setter
    def hostName(self, arg0: str) -> None:
        pass
    @property
    def inName(self) -> str:
        """
        :type: str
        """
    @inName.setter
    def inName(self, arg0: str) -> None:
        pass
    @property
    def inSeq(self) -> str:
        """
        :type: str
        """
    @inSeq.setter
    def inSeq(self, arg0: str) -> None:
        pass
    @property
    def isDynamic(self) -> bool:
        """
        :type: bool
        """
    @isDynamic.setter
    def isDynamic(self, arg0: bool) -> None:
        pass
    @property
    def maxIntron(self) -> int:
        """
        :type: int
        """
    @maxIntron.setter
    def maxIntron(self, arg0: int) -> None:
        pass
    @property
    def minIdentity(self) -> float:
        """
        :type: float
        """
    @minIdentity.setter
    def minIdentity(self, arg0: float) -> None:
        pass
    @property
    def minScore(self) -> int:
        """
        :type: int
        """
    @minScore.setter
    def minScore(self, arg0: int) -> None:
        pass
    @property
    def nohead(self) -> bool:
        """
        :type: bool
        """
    @nohead.setter
    def nohead(self, arg0: bool) -> None:
        pass
    @property
    def outName(self) -> str:
        """
        :type: str
        """
    @outName.setter
    def outName(self, arg0: str) -> None:
        pass
    @property
    def outputFormat(self) -> str:
        """
        :type: str
        """
    @outputFormat.setter
    def outputFormat(self, arg0: str) -> None:
        pass
    @property
    def portName(self) -> str:
        """
        :type: str
        """
    @portName.setter
    def portName(self, arg0: str) -> None:
        pass
    @property
    def qType(self) -> str:
        """
        :type: str
        """
    @qType.setter
    def qType(self, arg0: str) -> None:
        pass
    @property
    def tType(self) -> str:
        """
        :type: str
        """
    @tType.setter
    def tType(self, arg0: str) -> None:
        pass
    pass

class ServerOption:
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: ServerOption) -> None: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self) -> str: ...
    def build(self) -> ServerOption:
        """
        C++: cppbinding::ServerOption::build() --> struct cppbinding::ServerOption &
        """
    def to_string(self) -> str:
        """
        C++: cppbinding::ServerOption::to_string() const --> std::string
        """
    def withCanStop(self, canStop_: bool) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withCanStop(bool) --> struct cppbinding::ServerOption &
        """
    def withDebugLog(self, debugLog_: bool) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withDebugLog(bool) --> struct cppbinding::ServerOption &
        """
    def withIndexFile(self, indexFile_: str) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withIndexFile(std::string) --> struct cppbinding::ServerOption &
        """
    def withIpLog(self, ipLog_: bool) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withIpLog(bool) --> struct cppbinding::ServerOption &
        """
    def withLog(self, log_: str) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withLog(std::string) --> struct cppbinding::ServerOption &
        """
    def withLogFacility(self, logFacility_: str) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withLogFacility(std::string) --> struct cppbinding::ServerOption &
        """
    def withMask(self, mask_: bool) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withMask(bool) --> struct cppbinding::ServerOption &
        """
    def withMaxAaSize(self, maxAaSize_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withMaxAaSize(int) --> struct cppbinding::ServerOption &
        """
    def withMaxDnaHits(self, maxDnaHits_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withMaxDnaHits(int) --> struct cppbinding::ServerOption &
        """
    def withMaxGap(self, maxGap_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withMaxGap(int) --> struct cppbinding::ServerOption &
        """
    def withMaxNtSize(self, maxNtSize_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withMaxNtSize(int) --> struct cppbinding::ServerOption &
        """
    def withMaxTransHits(self, maxTransHits_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withMaxTransHits(int) --> struct cppbinding::ServerOption &
        """
    def withMinMatch(self, minMatch_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withMinMatch(int) --> struct cppbinding::ServerOption &
        """
    def withNoSimpRepMask(self, noSimpRepMask_: bool) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withNoSimpRepMask(bool) --> struct cppbinding::ServerOption &
        """
    def withPerSeqMax(self, perSeqMax_: str) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withPerSeqMax(std::string) --> struct cppbinding::ServerOption &
        """
    def withRepMatch(self, repMatch_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withRepMatch(int) --> struct cppbinding::ServerOption &
        """
    def withSeqLog(self, seqLog_: bool) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withSeqLog(bool) --> struct cppbinding::ServerOption &
        """
    def withStepSize(self, stepSize_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withStepSize(int) --> struct cppbinding::ServerOption &
        """
    def withSyslog(self, syslog_: bool) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withSyslog(bool) --> struct cppbinding::ServerOption &
        """
    def withThreads(self, threads_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withThreads(int) --> struct cppbinding::ServerOption &
        """
    def withTileSize(self, tileSize_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withTileSize(int) --> struct cppbinding::ServerOption &
        """
    def withTimeout(self, timeout_: int) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withTimeout(int) --> struct cppbinding::ServerOption &
        """
    def withTrans(self, trans_: bool) -> ServerOption:
        """
        C++: cppbinding::ServerOption::withTrans(bool) --> struct cppbinding::ServerOption &
        """
    @property
    def allowOneMismatch(self) -> bool:
        """
        :type: bool
        """
    @allowOneMismatch.setter
    def allowOneMismatch(self, arg0: bool) -> None:
        pass
    @property
    def canStop(self) -> bool:
        """
        :type: bool
        """
    @canStop.setter
    def canStop(self, arg0: bool) -> None:
        pass
    @property
    def debugLog(self) -> bool:
        """
        :type: bool
        """
    @debugLog.setter
    def debugLog(self, arg0: bool) -> None:
        pass
    @property
    def genome(self) -> str:
        """
        :type: str
        """
    @genome.setter
    def genome(self, arg0: str) -> None:
        pass
    @property
    def genomeDataDir(self) -> str:
        """
        :type: str
        """
    @genomeDataDir.setter
    def genomeDataDir(self, arg0: str) -> None:
        pass
    @property
    def indexFile(self) -> str:
        """
        :type: str
        """
    @indexFile.setter
    def indexFile(self, arg0: str) -> None:
        pass
    @property
    def ipLog(self) -> bool:
        """
        :type: bool
        """
    @ipLog.setter
    def ipLog(self, arg0: bool) -> None:
        pass
    @property
    def log(self) -> str:
        """
        :type: str
        """
    @log.setter
    def log(self, arg0: str) -> None:
        pass
    @property
    def logFacility(self) -> str:
        """
        :type: str
        """
    @logFacility.setter
    def logFacility(self, arg0: str) -> None:
        pass
    @property
    def mask(self) -> bool:
        """
        :type: bool
        """
    @mask.setter
    def mask(self, arg0: bool) -> None:
        pass
    @property
    def maxAaSize(self) -> int:
        """
        :type: int
        """
    @maxAaSize.setter
    def maxAaSize(self, arg0: int) -> None:
        pass
    @property
    def maxDnaHits(self) -> int:
        """
        :type: int
        """
    @maxDnaHits.setter
    def maxDnaHits(self, arg0: int) -> None:
        pass
    @property
    def maxGap(self) -> int:
        """
        :type: int
        """
    @maxGap.setter
    def maxGap(self, arg0: int) -> None:
        pass
    @property
    def maxNtSize(self) -> int:
        """
        :type: int
        """
    @maxNtSize.setter
    def maxNtSize(self, arg0: int) -> None:
        pass
    @property
    def maxTransHits(self) -> int:
        """
        :type: int
        """
    @maxTransHits.setter
    def maxTransHits(self, arg0: int) -> None:
        pass
    @property
    def minMatch(self) -> int:
        """
        :type: int
        """
    @minMatch.setter
    def minMatch(self, arg0: int) -> None:
        pass
    @property
    def noSimpRepMask(self) -> bool:
        """
        :type: bool
        """
    @noSimpRepMask.setter
    def noSimpRepMask(self, arg0: bool) -> None:
        pass
    @property
    def perSeqMax(self) -> str:
        """
        :type: str
        """
    @perSeqMax.setter
    def perSeqMax(self, arg0: str) -> None:
        pass
    @property
    def repMatch(self) -> int:
        """
        :type: int
        """
    @repMatch.setter
    def repMatch(self, arg0: int) -> None:
        pass
    @property
    def seqLog(self) -> bool:
        """
        :type: bool
        """
    @seqLog.setter
    def seqLog(self, arg0: bool) -> None:
        pass
    @property
    def stepSize(self) -> int:
        """
        :type: int
        """
    @stepSize.setter
    def stepSize(self, arg0: int) -> None:
        pass
    @property
    def syslog(self) -> bool:
        """
        :type: bool
        """
    @syslog.setter
    def syslog(self, arg0: bool) -> None:
        pass
    @property
    def threads(self) -> int:
        """
        :type: int
        """
    @threads.setter
    def threads(self, arg0: int) -> None:
        pass
    @property
    def tileSize(self) -> int:
        """
        :type: int
        """
    @tileSize.setter
    def tileSize(self, arg0: int) -> None:
        pass
    @property
    def timeout(self) -> int:
        """
        :type: int
        """
    @timeout.setter
    def timeout(self, arg0: int) -> None:
        pass
    @property
    def trans(self) -> bool:
        """
        :type: bool
        """
    @trans.setter
    def trans(self, arg0: bool) -> None:
        pass
    pass

def buildIndex(
    gfxFile: str, fileCount: int, seqFiles: typing.List[str], options: ServerOption
) -> None:
    """
    C++: cppbinding::buildIndex(std::string &, int, class std::vector<std::string >, const struct cppbinding::ServerOption &) --> void
    """

@typing.overload
def faToTwoBit(inFiles: typing.List[str], outFile: str) -> int:
    """
    C++: cppbinding::faToTwoBit(class std::vector<std::string > &, std::string &, bool, bool, bool, bool) --> int
    """

@typing.overload
def faToTwoBit(inFiles: typing.List[str], outFile: str, noMask: bool) -> int:
    pass

@typing.overload
def faToTwoBit(
    inFiles: typing.List[str], outFile: str, noMask: bool, stripVersion: bool
) -> int:
    pass

@typing.overload
def faToTwoBit(
    inFiles: typing.List[str],
    outFile: str,
    noMask: bool,
    stripVersion: bool,
    ignoreDups: bool,
) -> int:
    pass

@typing.overload
def faToTwoBit(
    inFiles: typing.List[str],
    outFile: str,
    noMask: bool,
    stripVersion: bool,
    ignoreDups: bool,
    useLong: bool,
) -> int:
    pass

def genoFindDirect(
    probeName: str, fileCount: int, seqFiles: typing.List[str], options: ServerOption
) -> None:
    """
    C++: cppbinding::genoFindDirect(std::string &, int, class std::vector<std::string > &, const struct cppbinding::ServerOption &) --> void
    """

def genoPcrDirect(
    fPrimer: str,
    rPrimer: str,
    fileCount: int,
    seqFiles: typing.List[str],
    options: ServerOption,
) -> None:
    """
    C++: cppbinding::genoPcrDirect(std::string &, std::string &, int, class std::vector<std::string > &, const struct cppbinding::ServerOption &) --> void
    """

def getFileList(hostName: str, portName: str) -> None:
    """
    C++: cppbinding::getFileList(std::string &, std::string &) --> void
    """

def getPortIx(portName: str) -> int:
    """
    C++: cppbinding::getPortIx(char *) --> int
    """

def gfServer(options: ServerOption) -> None:
    """
    C++: cppbinding::gfServer(struct cppbinding::ServerOption &) --> void
    """

def pcrServer(
    hostName: str, portName: str, fPrimer: str, rPrimer: str, maxSize: int
) -> None:
    """
    C++: cppbinding::pcrServer(std::string &, std::string &, std::string &, std::string &, int) --> void
    """

def pygetFileList(hostName: str, portName: str) -> str:
    """
    C++: cppbinding::pygetFileList(std::string &, std::string &) --> std::string
    """

def pygfClient(option: ClientOption) -> bytes:
    """
    C++: cppbinding::pygfClient(struct cppbinding::ClientOption &) --> std::string
    """

def pygfClient2(arg0: ClientOption) -> str:
    pass

def pygfClient_no_gil(option: ClientOption) -> None:
    """
    C++: cppbinding::pygfClient(struct cppbinding::ClientOption &) --> std::string
    """

def pyqueryServer(
    type: str, hostName: str, portName: str, faName: str, complex: bool, isProt: bool
) -> str:
    """
    C++: cppbinding::pyqueryServer(std::string &, std::string &, std::string &, std::string &, bool, bool) --> std::string
    """

def pystartServer(
    hostName: str,
    portName: str,
    fileCount: int,
    seqFiles: typing.List[str],
    options: ServerOption,
    stats: UsageStats,
) -> int:
    """
    C++: cppbinding::pystartServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::ServerOption &, struct cppbinding::UsageStats &) --> int
    """

def pystartServer_no_gil(
    hostName: str,
    portName: str,
    fileCount: int,
    seqFiles: typing.List[str],
    options: ServerOption,
    stats: UsageStats,
) -> int:
    """
    C++: cppbinding::pystartServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::ServerOption &, struct cppbinding::UsageStats &) --> int
    """

def pystatusServer(hostName: str, portName: str, options: ServerOption) -> str:
    """
    C++: cppbinding::pystatusServer(std::string &, std::string &, struct cppbinding::ServerOption &) --> std::string
    """

def queryServer(
    type: str, hostName: str, portName: str, faName: str, complex: bool, isProt: bool
) -> None:
    """
    C++: cppbinding::queryServer(std::string &, std::string &, std::string &, std::string &, bool, bool) --> void
    """

def startServer(
    hostName: str,
    portName: str,
    fileCount: int,
    seqFiles: typing.List[str],
    options: ServerOption,
    stats: UsageStats,
) -> None:
    """
    C++: cppbinding::startServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::ServerOption &, struct cppbinding::UsageStats &) --> void
    """

def statusServer(hostName: str, portName: str, options: ServerOption) -> int:
    """
    C++: cppbinding::statusServer(std::string &, std::string &, struct cppbinding::ServerOption &) --> int
    """

def stopServer(hostName: str, portName: str) -> None:
    """
    C++: cppbinding::stopServer(std::string &, std::string &) --> void
    """

def test(arg0: int, arg1: IntStruct) -> None:
    pass

def test_add(a: int) -> None:
    """
    C++: cppbinding::test_add(int &) --> void
    """

def test_exception() -> None:
    """
    C++: cppbinding::test_exception() --> void
    """

def test_no_gil(arg0: int, arg1: IntStruct) -> None:
    pass

def test_stat(stats: UsageStats) -> None:
    """
    C++: cppbinding::test_stat(struct cppbinding::UsageStats &) --> void
    """

def test_stdout() -> None:
    """
    C++: cppbinding::test_stdout() --> void
    """

def test_with_gil(arg0: int, arg1: IntStruct) -> None:
    pass

def twoBitToFa(inName: str, outName: str, option: TwoBitToFaOption) -> None:
    """
    C++ cppbinding::twoBitToFa(std::string cppinName, std::string cppoutName, TwoBitToFaOption option)
    """
